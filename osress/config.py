from pathlib import Path
import json
import appdirs
import os


class Config:

    __slots__ = ['app_name','app_author','filename','name']

    def __init__(self, app_name, app_author, filename=None, suffix='.conf'):
        self.app_name = app_name
        self.app_author = app_author
        self.filename = filename

        self.name = Path(app_name + suffix)

    @property
    def site_path(self):
        return Path(appdirs.site_config_dir(appname=self.app_name, appauthor=self.app_author))

    @property
    def site_file(self):
        return Path(self.site_path, self.name)

    @property
    def site(self):
        return self._read(self.site_file)

    @property
    def user_path(self):
        return Path(appdirs.user_config_dir(appname=self.app_name, appauthor=self.app_author))

    @property
    def user_file(self):
        return Path(self.user_path, self.name)

    @property
    def user(self):
        return self._read(self.user_file)

    @property
    def current_path(self):
        return Path(os.getcwd())

    @property
    def current_file(self):
        return Path(self.current_path, self.name)

    @property
    def current(self):
        return self._read(self.current_file)

    @property
    def explicit_path(self):
        return self.explicit_file.parent

    @property
    def explicit_file(self):
        return Path(self.filename)

    @property
    def explicit(self):
        return self._read(self.explicit_file)

    @staticmethod
    def _read(filepath):
        with filepath.open() as f:
            return json.load(f)

    def get(self):
        return 0
