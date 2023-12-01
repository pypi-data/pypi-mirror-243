__version__ = "0.6.0-alpha.5"
__all__ = [
    "__version__",
    "SVN2GitOptions",
    "GitMigrationHelper",
    "GitBranches",
    "svn_setup_authentication_plain",
    "svn_setup_authentication_cache",
    "svn_test_authentication",
]

from svn2git.git import GitBranches, GitMigrationHelper
from svn2git.options import SVN2GitOptions
from svn2git.svn import svn_setup_authentication_cache, svn_setup_authentication_plain, svn_test_authentication
