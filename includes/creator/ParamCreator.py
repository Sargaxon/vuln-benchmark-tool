# -*- coding: utf-8 -*-
from includes.creator import Param, Generator


class ParamCreator:
    def __init__(self):
        self.params = dict()

    def add_param(self, name, value):
        self.params[name] = Param(name, value)

    def add_random_param(self):
        name = Generator.random_string(5, "letters")
        self.params[name] = Param(name, Generator.random_string(7))

    def generate_n_params(self, n):
        for i in range(0, n):
            self.add_random_param()

        print(self.params)

        return self.params

    def add_n_params(self, params):
        for (name, value) in params:
            self.add_param(name, value)
