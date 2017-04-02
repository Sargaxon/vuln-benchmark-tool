# -*- coding: utf-8 -*-
from includes.creator import Page


class RedirectPage(Page):
    def __init__(self, identifier, redirect, status=302):
        Page.__init__(self, identifier=identifier, status=status)
        self.redirect = redirect
