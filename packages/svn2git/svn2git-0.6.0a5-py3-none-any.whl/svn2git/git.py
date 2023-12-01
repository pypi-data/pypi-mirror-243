import logging
import os
from collections import namedtuple
from typing import Optional

from svn2git.utils import escape_quotes, run_command

logger = logging.getLogger(__name__)

GitBranches = namedtuple("GitBranches", ["locals", "remotes", "tags"])


class GitMigrationHelper:
    """
    Git migration helper

    :arg svn_remote_prefix: The prefix of the remote branches (Default: svn)
    :arg initial_branch_name: The name of the initial branch (Default: main)
    :arg git_remote: The name of the git remote to push to. (Default: origin)
    :arg cwd: The current working directory to run the command in. (Default: None)
    """

    _svn_remote_prefix: str
    _initial_branch_name: str
    _git_remote: str
    _cwd: Optional[str] = None

    def __init__(
        self,
        svn_remote_prefix: str = "svn",
        initial_branch_name: str = "main",
        git_remote: str = "origin",
        cwd: Optional[str] = None,
    ) -> None:
        self._svn_remote_prefix = svn_remote_prefix
        self._initial_branch_name = initial_branch_name
        self._git_remote = git_remote
        self._cwd = cwd

    def clone(
        self,
        svn_url: str,
        trunk_branch: str = "trunk",
        branches: Optional[list[str]] = None,
        tags: Optional[list[str]] = None,
        include_metadata: bool = False,
        no_minimize_url: bool = False,
        root_is_trunk: bool = False,
        authors_file_path: Optional[str] = None,
        exclude: Optional[list[str]] = None,
        revision: Optional[str] = None,
        username: Optional[str] = None,
    ) -> None:
        """
        Clone the SVN repository to be usable with Git.

        :param svn_url: The SVN repository URL.
        :param trunk_branch: The trunk branch (Default: trunk).
        :param branches: The branches (Default: ['branches'].
        :param tags: The tags (Default: ['tags']).
        :param include_metadata: Include metadata in git logs (git-svn-id).
        :param no_minimize_url: Accept URLs as-is without attempting to connect to a higher level directory.
        :param root_is_trunk: Use this if the root level of the repo is
            equivalent to the trunk and there are no tags or branches.
        :param authors_file_path: Path to file containing svn-to-git authors mapping.
        :param exclude: Specify a Perl regular expression to filter paths when fetching; can be used multiple times.
        :param revision: Start importing from SVN revision START_REV; optionally end at END_REV.
        :param username: Username for transports that needs it (http(s), svn).
        :return:
        """
        if exclude is None:
            exclude = []
        if tags is None:
            tags = ["tags"]
        if branches is None:
            branches = ["branches"]

        logger.info(f"Cloning {svn_url}...")

        # Create directory if it does not exist
        if self._cwd is not None and not os.path.exists(self._cwd):
            os.makedirs(self._cwd)

        # Set correct initial branch name
        run_command(f"git config --global init.defaultBranch {self._initial_branch_name}", cwd=self._cwd)

        # Initialize repository
        logger.info("Initializing repository...")
        init_command = f"git svn init --prefix={self._svn_remote_prefix}/ "
        if username:
            init_command += f"--username={username} "
        if not include_metadata:
            init_command += "--no-metadata "
        if no_minimize_url:
            init_command += "--no-minimize-url "

        if root_is_trunk:
            # Non-standard repository layout. The repository root is effectively 'trunk'.
            init_command += f"--trunk='{svn_url}'"
        else:
            if trunk_branch:
                init_command += f"--trunk='{trunk_branch}' "

            if branches:
                for branch_name in branches:
                    init_command += f"--branches='{branch_name}' "

            if tags:
                for tag_name in tags:
                    init_command += f"--tags='{tag_name}' "

            init_command += svn_url

        run_command(init_command, cwd=self._cwd)

        # Trust current working directory as repository
        run_command(f"git config --global --add safe.directory {os.getcwd()}", cwd=self._cwd)

        # Setup authors mapping
        if authors_file_path:
            logger.info(f"Setting up authors mapping from {authors_file_path}...")
            run_command(f'{self.get_config_command()} svn.authorsfile "{authors_file_path}"', cwd=self._cwd)

        # Fetch SVN repository
        logger.info("Fetching SVN repository...")
        fetch_command = "git svn fetch "

        if revision:
            revision_range = revision.split(":")
            if len(revision_range) == 1:
                fetch_command += f"-r {revision_range[0]}:HEAD "
            else:
                fetch_command += f"-r {revision_range[0]}:{revision_range[1]} "

        if exclude and len(exclude) > 0:
            regex = []
            if not root_is_trunk:
                if trunk_branch:
                    regex.append(f"{trunk_branch}[/]")
                if tags and len(tags) > 0:
                    regex.append("[/][^/]+[/]".join(tags))
                if branches and len(branches) > 0:
                    regex.append("[/][^/]+[/]".join(branches))

            regex_str = f"^(?:{'|'.join(regex)})(?:{'|'.join(exclude)})"
            fetch_command += f'--ignore-paths="{regex_str}" '

        run_command(fetch_command, cwd=self._cwd)

    def get_branches(self, tags_base: str = "tags") -> GitBranches:
        """
        Get local, remote and tag branches from the repository.

        :param tags_base: The tags base (Default: tags).
        :return: The branches.
        """

        logger.info("Getting local, remote and tag branches")

        # Get the local and remote branches taking care to ignore console color codes and ignore the '*'
        # used to indicate the currently selected branch
        result_local = run_command(
            "git branch -l --no-color --format='%(refname:short)'",
            exit_on_error=True,
            return_stdout=True,
            cwd=self._cwd,
        )
        local_branches = result_local.replace("'", "").splitlines()
        result_remote = run_command(
            "git branch -r --no-color --format='%(refname:short)'",
            exit_on_error=True,
            return_stdout=True,
            cwd=self._cwd,
        )
        remote_branches = result_remote.replace("'", "").splitlines()

        # Tags are remote branches that start with the tags prefix
        tags = [tag for tag in remote_branches if tag.startswith(f"{self._svn_remote_prefix}/{tags_base}/")]

        branches = GitBranches(local_branches, remote_branches, tags)
        logger.debug(f"Local branches: {branches.locals}")
        logger.debug(f"Remote branches: {branches.remotes}")
        logger.debug(f"Tags: {branches.tags}")

        return branches

    def get_rebase_branch(self, branch_name: str, tags_base: str = "tags") -> GitBranches:
        """
        Get the local and remote branches for the rebase branch.

        :param branch_name: The rebase branch.
        :param tags_base: The tags base (Default: tags).
        :return: The branches.
        """
        branches = self.get_branches(tags_base=tags_base)

        logger.info(f"Getting local and remote branches for rebase branch {branch_name}")

        # Filter the local and remote branches
        local_branches = [local_branch for local_branch in branches.locals if local_branch == branch_name]
        remote_branches = [remote_branch for remote_branch in branches.remotes if remote_branch == branch_name]

        if len(local_branches) > 1:
            logger.error(f"To many matching branches found locally for branch {branch_name}.")
            exit(1)
        elif len(local_branches) == 0:
            logger.error(f"No matching branches found locally for branch {branch_name}.")
            exit(1)

        if len(remote_branches) > 2:  # 1 if remote is not pushed; 2 if it's pushed to remote
            logger.error(f"To many matching branches found remotely for branch {branch_name}.")
            exit(1)
        elif len(remote_branches) == 0:
            logger.error(f"No matching branches found remotely for branch {branch_name}.")
            exit(1)

        logger.debug(f'Local branches "{local_branches}" found')
        logger.debug(f'Remote branches "{remote_branches}" found')

        branches = GitBranches(local_branches, remote_branches, tags=[])
        logger.debug(f"Local branches: {branches.locals}")
        logger.debug(f"Remote branches: {branches.remotes}")
        logger.debug(f"Tags: {branches.tags}")

        return branches

    def fix_tags(self, branches: GitBranches, tags_base: str = "tags") -> None:
        """
        Convert svn tag branches to git tags.

        :param branches: The branches.
        :param tags_base: The tags base (Default: tags).
        """
        logger.info("Fixing tags...")
        # Save current git user and reset to this value later on
        possible_user_name = run_command(
            "git config user.name", exit_on_error=False, return_stdout=True, cwd=self._cwd
        ).splitlines()
        possible_user_email = run_command(
            "git config user.email", exit_on_error=False, return_stdout=True, cwd=self._cwd
        ).splitlines()
        current: dict[str, str] = {
            "user.name": possible_user_name[0] if len(possible_user_name) > 0 else "",
            "user.email": possible_user_email[0] if len(possible_user_email) > 0 else "",
        }

        for tag in branches.tags:
            logger.info(f"Fixing tag {tag}...")
            clean_tag = tag.strip()
            tag_id = clean_tag.replace(f"{self._svn_remote_prefix}/{tags_base}/", "").strip()
            logger.debug(f"Tag ID: {tag_id}")
            subject = (
                run_command(
                    f"git log -1 --pretty=format:'%s' \"{escape_quotes(clean_tag)}\"",
                    exit_on_error=True,
                    return_stdout=True,
                    cwd=self._cwd,
                )
                .splitlines()[0]
                .strip("'")
            )
            logger.debug(f"Subject: {subject}")
            date = (
                run_command(
                    f"git log -1 --pretty=format:'%ci' \"{escape_quotes(clean_tag)}\"",
                    exit_on_error=True,
                    return_stdout=True,
                    cwd=self._cwd,
                )
                .splitlines()[0]
                .strip("'")
            )
            logger.debug(f"Date: {date}")
            author = (
                run_command(
                    f"git log -1 --pretty=format:'%an' \"{escape_quotes(clean_tag)}\"",
                    exit_on_error=True,
                    return_stdout=True,
                    cwd=self._cwd,
                )
                .splitlines()[0]
                .strip("'")
            )
            logger.debug(f"Author: {author}")
            email = (
                run_command(
                    f"git log -1 --pretty=format:'%ae' \"{escape_quotes(clean_tag)}\"",
                    exit_on_error=True,
                    return_stdout=True,
                    cwd=self._cwd,
                )
                .splitlines()[0]
                .strip("'")
            )
            logger.debug(f"Email: {email}")

            run_command(f'{self.get_config_command()} user.name "{escape_quotes(author)}"', cwd=self._cwd)
            run_command(f'{self.get_config_command()} user.email "{escape_quotes(email)}"', cwd=self._cwd)

            original_git_comitter_date = os.environ.get("GIT_COMMITTER_DATE")
            os.environ["GIT_COMMITTER_DATE"] = escape_quotes(date)
            run_command(
                f'git tag -a -m "{escape_quotes(subject)}" "{escape_quotes(tag_id)}" "{escape_quotes(tag)}"',
                cwd=self._cwd,
            )
            if original_git_comitter_date:
                os.environ["GIT_COMMITTER_DATE"] = original_git_comitter_date

            run_command(f'git branch -d -r "{escape_quotes(tag)}"', cwd=self._cwd)

        # Change back user.name and user.email if we had to reconfigure it for the tag creation process
        if len(branches.tags) > 0:
            for name, value in current.items():
                if value.strip() != "":
                    run_command(f'{self.get_config_command()} {name} "{value.strip()}"', cwd=self._cwd)
                else:
                    run_command(f"{self.get_config_command()} --unset {name}", cwd=self._cwd)

    def fix_branches(self, branches: GitBranches, rebase: bool = False, trunk_branch: str = "trunk") -> None:
        """
        Fix or rebase all branches.

        :param branches: The branches.
        :param rebase: Whether to rebase the branches.
        :param trunk_branch: The trunk branch (Default: trunk).
        """
        logger.info(f"Fixing branches (rebase: {rebase})...")
        svn_branches = list(set(branches.remotes) - set(branches.tags))
        logger.debug(f"Svn branches found (without tags): {svn_branches}")
        svn_branches = [branch for branch in svn_branches if branch.find(f"{self._svn_remote_prefix}/") != -1]
        logger.debug(f"Svn branches found (without tags and with prefix): {svn_branches}")

        if rebase:
            logger.info("Fetching latest changes from SVN server...")
            run_command("git svn fetch", cwd=self._cwd)

        for svn_branch in svn_branches:
            logger.info(f"Fixing branch {svn_branch}...")
            branch = svn_branch.replace(f"{self._svn_remote_prefix}/", "")
            # Rebase branch if we should rebase it
            if rebase and (branch in branches.locals or branch == trunk_branch):
                local_branch = self._initial_branch_name if branch == trunk_branch else branch
                logger.info(f"Rebasing branch {local_branch}...")
                run_command(f'git checkout -f "{local_branch}"', cwd=self._cwd)
                run_command(f'git rebase "remotes/{self._svn_remote_prefix}/{branch}"', cwd=self._cwd)
                continue

            # Ignore branch if already exists as local branch or is the trunk branch
            if branch in branches.locals or branch == trunk_branch:
                logger.info(f"Ignoring branch {branch} as it already exists as local branch or is the trunk branch")
                continue

            # Create the local branch
            self.checkout_svn_branch(branch)

    def fix_trunk(self, branches: GitBranches, rebase: bool = False, trunk_branch: str = "trunk") -> None:
        """
        Fix or rebase the trunk branch.

        :param branches: The branches.
        :param rebase: Whether to rebase the trunk.
        :param trunk_branch: The trunk branch (Default: trunk).
        """
        logger.info(f"Fixing trunk branch {trunk_branch} (rebase: {rebase})...")
        trunk = True in (branch.strip() == f"{self._svn_remote_prefix}/{trunk_branch}" for branch in branches.remotes)
        logger.debug(f"Trunk branch found: {trunk}")
        if trunk and not rebase:
            logger.info("Trunk branch found -> so fix it")
            run_command(f"git checkout {self._svn_remote_prefix}/{trunk_branch}", cwd=self._cwd)
            run_command(f"git branch -D {self._initial_branch_name}", cwd=self._cwd)
            run_command(f"git checkout -f -b {self._initial_branch_name}", cwd=self._cwd)
        else:
            logger.debug("Trunk branch not found -> so create it")
            run_command(f"git checkout -f {self._initial_branch_name}", cwd=self._cwd)

    def push_branches(
        self, branches: GitBranches, large_repository_mode: bool = False, push_commit_limit: int = 1000
    ) -> None:
        """
        Push all branches to a configured remote repository.
        :param branches: The branches to use as base
        :param large_repository_mode: Whether to use large repository mode and split
        the push command into multiple pushes
        :param push_commit_limit: The number of commits to push per push command when large repository mode is enabled
        """

        logger.info("Pushing branches...")

        if large_repository_mode:
            # Split the push command into multiple pushes
            # We start with the main branch
            logger.info(f"Pushing branch {self._initial_branch_name}...")
            commits = self.get_batched_commits(self._initial_branch_name, push_commit_limit)
            commits_len = len(commits)
            for idx, commit in enumerate(commits):
                logger.debug(f"Pushing commit {commit} ({idx + 1}/{commits_len})...")
                stdout = run_command(
                    f'git push origin "{commit}:refs/heads/{self._initial_branch_name}"',
                    exit_on_error=False,
                    return_stdout=True,
                    cwd=self._cwd,
                )
                if stdout.find("git pull") != -1:
                    logger.warning(f"Commit {commit} already pushed. Skipping...")
                    continue
                if stdout.find("error") != -1:
                    logger.error(f"Error while pushing commit {commit}. Exiting...")
                    exit(1)

            # Next all other branches except the main
            for branch in branches.locals:
                if branch == self._initial_branch_name:
                    continue

                logger.info(f"Pushing branch {branch}...")
                commits = self.get_batched_commits(branch, push_commit_limit)
                commits_len = len(commits)
                for idx, commit in enumerate(commits):
                    logger.debug(f"Pushing commit {commit} ({idx + 1}/{commits_len})...")
                    stdout = run_command(
                        f'git push origin "{commit}:refs/heads/{branch}"',
                        exit_on_error=False,
                        return_stdout=True,
                        cwd=self._cwd,
                    )
                    if stdout.find("git pull") != -1:
                        logger.warning(f"Commit {commit} already pushed. Skipping...")
                        continue
                    if stdout.find("error") != -1:
                        logger.error(f"Error while pushing commit {commit}. Exiting...")
                        exit(1)

        # Last step -> try to push everything
        run_command(f"git push -u {self._git_remote} --all", cwd=self._cwd)

    def push_tags(self) -> None:
        """
        Push all tags to a configured remote repository.
        """
        logger.info("Pushing tags...")
        run_command(f"git push -u {self._git_remote} --tags", cwd=self._cwd)

    def get_batched_commits(self, local_branch: str, batch_limit: int = 1000) -> list[str]:
        """
        Get the batched commits for a local branch.

        :param local_branch: The local branch.
        :param batch_limit: The batch limit.
        :return: The batched commits.
        """
        logger.debug(f"Getting batched commits for local branch {local_branch}...")
        result = run_command(
            f"git log --oneline --reverse \"refs/heads/{local_branch}\" | awk 'NR % {batch_limit} == 0'",
            exit_on_error=True,
            return_stdout=True,
            cwd=self._cwd,
        )
        list_commit_message = result.splitlines()
        # Split each line into a list of the commit hash and omit the commit message
        list_commit_message = [commit_message.split(" ")[0] for commit_message in list_commit_message]
        logger.debug(f"Batched commits: {list_commit_message}")
        return list_commit_message

    def checkout_svn_branch(self, branch: str) -> None:
        """
        Checkout an SVN branch.

        :param branch: The branch to check out.
        """
        logger.info(f"Checking out SVN branch {branch}...")
        run_command(f'git checkout -b "{branch}" "remotes/{self._svn_remote_prefix}/{branch}"', cwd=self._cwd)

    def optimize_repository(self) -> None:
        """
        Optimize the repository.
        """
        logger.info("Optimizing repository...")
        run_command("git gc", cwd=self._cwd)

    def verify_working_tree_is_clean(self) -> None:
        """
        Verify that the working tree is clean.
        """
        result = run_command(
            "git status --porcelain --untracked-files=no", exit_on_error=True, return_stdout=True, cwd=self._cwd
        )
        if result != "":
            logger.error("Working tree is not clean. Please commit or stash your changes.")
            exit(1)

    def get_config_command(self) -> str:
        """
        Get the correct command to set the git config.
        """
        result = run_command(
            "git config --local --get user.name", exit_on_error=False, return_stdout=True, cwd=self._cwd
        )
        if result.find("unknown option") != -1:
            return "git config"
        else:
            return "git config --local"
