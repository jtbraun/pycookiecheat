"""test_pycookiecheat.py :: Tests for pycookiecheat module."""

import os
import os.path
import shutil
import sys
from urllib.error import URLError
from uuid import uuid4

import pytest

from pycookiecheat import chrome_cookies


@pytest.fixture(scope='module')
def travis_setup(request: pytest.fixture) -> None:
    """Set up Chrome's cookies file and directory on Travis.

    Appropriately doesn't load teardown() this dir already
    exists, preventing it from getting to the teardown function which would
    otherwise risk deleting someone's ~/.config/google-chrome directory (if
    they had the TRAVIS=true environment set for some reason).

    """
    def teardown() -> None:
        """Remove the cookies directory."""
        os.remove(cookies_dest)
        try:
            os.removedirs(cookies_dest_dir)
        except OSError:
            # Directory wasn't empty, expected at '~'
            pass

    # Where the cookies file should be
    cookies_dest_dir = os.path.expanduser('~/.config/google-chrome/Default')
    cookies_dest = os.path.join(cookies_dest_dir, 'Cookies')

    # Where the test cookies file is
    cookies_dir = os.path.dirname(os.path.abspath(__file__))
    cookies_path = os.path.join(cookies_dir, 'Cookies')

    if all([os.getenv('TRAVIS') == 'true',
            sys.platform.startswith('linux'),
            not os.path.isfile(cookies_dest)]):

        os.makedirs(cookies_dest_dir)
        shutil.copy(cookies_path, cookies_dest_dir)

        # Only teardown if running on travis
        request.addfinalizer(teardown)


def test_raises_on_empty() -> None:
    """Ensure that `chrome_cookies()` raises."""
    with pytest.raises(TypeError):
        chrome_cookies()  # type: ignore


def test_raises_without_scheme() -> None:
    """Ensure that `chrome_cookies("domain.com")` raises.

    The domain must specify a scheme (http or https).

    """
    with pytest.raises(URLError):
        chrome_cookies('n8henrie.com')


def test_no_cookies(travis_setup: pytest.fixture) -> None:
    """Ensure that no cookies are returned for a fake url."""
    never_been_here = 'http://{0}.com'.format(uuid4())
    empty_dict = chrome_cookies(never_been_here)
    assert empty_dict == dict()


def test_fake_cookie(travis_setup: pytest.fixture) -> None:
    """Tests a fake cookie from the website below.

    For this to pass, you'll
    have to visit the url and put in "TestCookie" and "Just_a_test!" to set
    a temporary cookie with the appropriate values.

    """
    cookies = chrome_cookies('http://www.html-kit.com/tools/cookietester')
    assert cookies['TestCookie'] == 'Just_a_test!'


def test_raises_on_wrong_browser() -> None:
    """Passing a browser other than Chrome or Chromium raises ValueError."""
    with pytest.raises(ValueError):
        chrome_cookies('http://www.html-kit.com/tools/cookietester',
                       browser="Safari")
