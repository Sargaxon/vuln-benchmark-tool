# -*- coding: utf-8 -*-


class Page:
    def __init__(self, identifier, links=None, form=None, params=None):
        self.identifier = identifier
        self.links = links
        self.form = form
        self.params = params
