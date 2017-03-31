# -*- coding: utf-8 -*-
from includes.creator import Link
import random


class LinkCreator:
    def __init__(self):
        self.links = []

    def generate_links_for_pages(self, pages, status=200, headers=None):
        for page in pages:
            page.status = LinkCreator.random_status() if status == 0 else 200
            self.links.append(Link(page, headers))

        return self.links

    @staticmethod
    def random_status():
        status_codes = [
            101,
            200,
            302,
            400,
            403,
            404,
            405,
        ]

        return random.choice(status_codes)
