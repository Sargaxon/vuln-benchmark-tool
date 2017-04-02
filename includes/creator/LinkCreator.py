# -*- coding: utf-8 -*-
from includes.creator import Link


class LinkCreator:
    def __init__(self):
        self.links = []

    def generate_links_for_page(self, pages):
        for page in pages:
            self.links.append(Link(page))

        return self.links


