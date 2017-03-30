# -*- coding: utf-8 -*-
from wtforms import *
from wtforms.form import BaseForm


class FormCreator:
    def __init__(self):
        self.form = None
        self.elements = dict()

    def build_form(self):
        self.form = BaseForm(self.elements)

    def add_text_field(self, name, required):
        try:
            self.elements[name] = StringField(name, validators.input_required if required else None)
        except KeyError as exception:
            print(exception)

    def add_number_field(self, name, required):
        try:
            self.elements[name] = IntegerField(name, validators.input_required if required else None)
        except KeyError as exception:
            print(exception)

    def add_select_field(self, name, required, options):
        try:
            self.elements[name] = SelectField(
                name,
                validators.input_required if required else None,
                choices=options
            )
        except KeyError as exception:
            print(exception)

    def add_checkbox_field(self, name, required):
        try:
            self.elements[name] = BooleanField(
                name,
                validators.input_required if required else None,
            )
        except KeyError as exception:
            print(exception)

    def add_radio_field(self, name, required):
        try:
            self.elements[name] = RadioField(
                name,
                validators.input_required if required else None,
            )
        except KeyError as exception:
            print(exception)

