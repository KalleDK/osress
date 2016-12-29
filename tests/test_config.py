import pytest
import osress
import unittest.mock
import pathlib
import json
import io


APP_NAME = 'appname'
APP_AUTHOR = 'appauthor'
SUFFIX = '.conf'
EXPLICIT_SUFFIX = '.json'



NAME = pathlib.Path(APP_NAME + SUFFIX)

USER_CONFIG_FILE = pathlib.Path('valid', 'user', 'config', 'dir', NAME)
USER_CONFIG_PATH = USER_CONFIG_FILE.parent
USER_CONFIG = {'user': True}
USER_CONFIG_FP = io.StringIO(json.dumps(USER_CONFIG))

SITE_CONFIG_FILE = pathlib.Path('valid', 'site', 'config', 'dir', NAME)
SITE_CONFIG_PATH = SITE_CONFIG_FILE.parent
SITE_CONFIG = {'site': True}
SITE_CONFIG_FP = io.StringIO(json.dumps(SITE_CONFIG))

CURRENT_CONFIG_FILE = pathlib.Path('valid', 'current', 'config', 'dir', NAME)
CURRENT_CONFIG_PATH = CURRENT_CONFIG_FILE.parent
CURRENT_CONFIG = {'current': True}
CURRENT_CONFIG_FP = io.StringIO(json.dumps(CURRENT_CONFIG))

EXPLICIT_CONFIG_FILE = pathlib.Path('valid', 'explicit', 'config', 'dir', 'explicit.conf')
EXPLICIT_CONFIG_PATH = EXPLICIT_CONFIG_FILE.parent
EXPLICIT_CONFIG = {'explicit': True}
EXPLICIT_CONFIG_FP = io.StringIO(json.dumps(EXPLICIT_CONFIG))

FILENAME_STRING = 'file/name.conf'
FILENAME_PATH = pathlib.Path(FILENAME_STRING)




@pytest.fixture
def uut():
    return osress.Config(APP_NAME, APP_AUTHOR)

@pytest.fixture
def uut_exp():
    return osress.Config(APP_NAME, APP_AUTHOR, filename=str(EXPLICIT_CONFIG_FILE))



def fake_path_open(self):
    paths = {
        USER_CONFIG_FILE: USER_CONFIG_FP,
        SITE_CONFIG_FILE: SITE_CONFIG_FP,
        CURRENT_CONFIG_FILE: CURRENT_CONFIG_FP,
        EXPLICIT_CONFIG_FILE: EXPLICIT_CONFIG_FP
    }

    return paths.get(self, io.StringIO('{"invalid": false}'))


def fake_user_config_dir(appname, appauthor):

    if not appname == 'appname':
        return 'invalid_appname'

    if not appauthor == 'appauthor':
        return 'invalid_appauthor'

    return str(USER_CONFIG_PATH)


def fake_site_config_dir(appname, appauthor):

    if not appname == 'appname':
        return 'invalid_appname'

    if not appauthor == 'appauthor':
        return 'invalid_appauthor'

    return str(SITE_CONFIG_PATH)


def fake_os_getcwd():
    return str(CURRENT_CONFIG_PATH)


    


class TestAttributes:
    def test_app_name(self, uut):
        assert uut.app_name == APP_NAME

    def test_app_author(self, uut):
        assert uut.app_author == APP_AUTHOR

    def test_name(self, uut):
        assert uut.name == NAME

    def test_filename_default_None(self, uut):
        assert uut.filename == None

    def test_suffix_default(self, uut):
        assert uut.name.suffix == SUFFIX

    def test_suffix_explicit(self):
        uut = osress.Config(APP_NAME, APP_AUTHOR, suffix=EXPLICIT_SUFFIX)
        assert uut.name.suffix == EXPLICIT_SUFFIX

    def test_filename_explicit_given_path(self, uut):
        uut = osress.Config(APP_NAME, APP_AUTHOR, filename=FILENAME_PATH)
        assert uut.filename == FILENAME_PATH

    def test_filename_explicit_given_string(self, uut):
        uut = osress.Config('appname', 'appauthor', filename=FILENAME_STRING)
        assert uut.filename == FILENAME_STRING

@unittest.mock.patch('appdirs.user_config_dir', autospec=True, side_effect=fake_user_config_dir)
class TestUser:

    def test_user_path(self, mock_user_config_dir, uut):
        assert uut.user_path == USER_CONFIG_PATH

    def test_user_file(self, mock_site_config_dir, uut):
        assert uut.user_file == USER_CONFIG_FILE

    @unittest.mock.patch('pathlib.Path.open', autospec=True, side_effect=fake_path_open)
    def test_user(self, mock_path_open, mock_user_config_dir, uut):
        assert uut.user == USER_CONFIG


@unittest.mock.patch('appdirs.site_config_dir', autospec=True, side_effect=fake_site_config_dir)
class TestSite:

    def test_site_path(self, mock_site_config_dir, uut):
        assert uut.site_path == SITE_CONFIG_PATH

    def test_site_file(self, mock_site_config_dir, uut):
        assert uut.site_file == SITE_CONFIG_FILE

    @unittest.mock.patch('pathlib.Path.open', autospec=True, side_effect=fake_path_open)
    def test_site(self, mock_path_open, mock_user_config_dir, uut):
        assert uut.site == SITE_CONFIG


@unittest.mock.patch('os.getcwd', autospec=True, side_effect=fake_os_getcwd)
class TestCurrent:

    def test_current_path(self, mock_os_getcwd, uut):
        assert uut.current_path == CURRENT_CONFIG_PATH

    def test_current_file(self, mock_os_getcwd, uut):
        assert uut.current_file == CURRENT_CONFIG_FILE

    @unittest.mock.patch('pathlib.Path.open', autospec=True, side_effect=fake_path_open)
    def test_current(self, mock_path_open, mock_os_getcwd, uut):
        assert uut.current == CURRENT_CONFIG


class TestExplicit:

    def test_explicit_path(self, uut_exp):
        assert uut_exp.explicit_path == EXPLICIT_CONFIG_PATH

    def test_explicit_file(self, uut_exp):
        assert uut_exp.explicit_file == EXPLICIT_CONFIG_FILE

    @unittest.mock.patch('pathlib.Path.open', autospec=True, side_effect=fake_path_open)
    def test_explicit(self, mock_path_open, uut_exp):
        assert uut_exp.explicit == EXPLICIT_CONFIG
