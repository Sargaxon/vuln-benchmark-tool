# -*- coding: utf-8 -*-


class Link:
    def __init__(self, page):
        self.page = page

    def href(self, absolute=True):
        return ("/" if absolute else "") + "browse/" + self.page.identifier + self.url_params()

    def url_params(self):
        url_params = ""

        for name, param in self.page.params.items():
            url_params += (("?" if url_params == "" else "&") + param.name + "=" + param.value)

        return url_params
