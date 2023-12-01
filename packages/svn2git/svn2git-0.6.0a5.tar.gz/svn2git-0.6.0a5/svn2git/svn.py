import logging
from typing import Optional

from svn2git.svn_store_plaintext_password import svn_store_plaintext_password
from svn2git.utils import run_command

logger = logging.getLogger(__name__)


def svn_test_authentication(url: str, username: Optional[str] = None, password: Optional[str] = None) -> None:
    """Test SVN authentication.

    Args:
        url (str): URL of the SVN repository.
        username (Optional[str], optional): Username for SVN. Defaults to None.
        password (Optional[str], optional): Password for SVN. Defaults to None.
    """

    logger.debug("Testing SVN authentication")
    username_arg = f" --username {username}" if username is not None else ""
    password_arg = f" --password {password}" if password is not None else ""
    run_command(f"svn log --revision HEAD{username_arg}{password_arg} --non-interactive {url}")


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
