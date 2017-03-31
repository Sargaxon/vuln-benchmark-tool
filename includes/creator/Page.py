# -*- coding: utf-8 -*-


class Page:
    def __init__(self, identifier, status=200, links=None, form=None, params=None):
        self.identifier = identifier
        self.status = status
        self.links = links if links else []
        self.form = form
        self.params = params if params else dict()
