import logging

from svn2git.svn_store_plaintext_password import svn_store_plaintext_password
from svn2git.utils import run_command

logger = logging.getLogger(__name__)


def svn_setup_authentication_plain(realm: str, username: str, password: str) -> None:
    """Setup plain authentication for SVN.

    Args:
        realm (str): Authentication realm for SVN.
        username (str): Username for SVN.
        password (str): Password for SVN.
    """

    logger.debug("Storing SVN password in plaintext")
    svn_store_plaintext_password(realm, username, password)


def svn_setup_authentication_cache(url: str, username: str, password: str) -> None:
    """Setup cached authentication for SVN.

    Args:
        url (str): URL of the SVN repository.
        username (str): Username for SVN.
        password (str): Password for SVN.
    """

    logger.debug("Storing SVN password in cache")
    run_command(f"svn log --revision HEAD --username {username} --password {password} --non-interactive {url}")
