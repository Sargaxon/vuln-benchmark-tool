# -*- coding: utf-8 -*-
from includes.creator import Param
from includes.creator import Generator


class ParamCreator:
    def __init__(self, method):
        self.method = method
        self.params = dict()

    def add_param(self, name, value):
        self.params[name] = Param(name, value, self.method)

    def add_random_param(self):
        self.params[Generator.random_string(5, "letters")] = Generator.random_string(7)

    def generate_n_params(self, n):
        for i in range(0, n):
            self.add_random_param()

    def add_n_params(self, params):
        for (name, value) in params:
            self.add_param(name, value)
