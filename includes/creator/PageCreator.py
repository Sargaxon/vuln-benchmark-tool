# -*- coding: utf-8 -*-
from includes.creator import Generator, Page, ParamCreator


class PageCreator:
    def __init__(self):
        self.pages = {}

    def generate_n_pages(self, n, params=None, status=0, headers=None):
        for i in range(0, n):
            identifier = Generator.random_string(6, "lowercase")

            if params == 0:
                param_creator = ParamCreator()
                page_params = param_creator.generate_n_params(Generator.random_number(0, 5))
            else:
                page_params = params

            self.pages[identifier] = Page(
                    identifier,
                    params=page_params,
                    status=Generator.random_status() if status == 0 else status,
                    headers=headers
                )

        return self.pages
