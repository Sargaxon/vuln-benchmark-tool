# -*- coding: utf-8 -*-
import pickle
import os.path

filename = "settings.conf"


class Settings:
    def __init__(self):
        self.tests = dict()

    def save(self):
        if not os.path.isfile(filename) or os.path.getsize(filename) == 0:
            Settings.init_settings(filename)

        with open(filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load():
        if not os.path.isfile(filename) or os.path.getsize(filename) == 0:
            Settings.init_settings(filename)

        with open(filename, 'rb') as settings:
            return pickle.load(settings)

    @staticmethod
    def init_settings(filename):
        with open(filename, 'wb') as output:
            settings = Settings()
            pickle.dump(settings, output, pickle.HIGHEST_PROTOCOL)
