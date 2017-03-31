# -*- coding: utf-8 -*-
from wtforms import *
from wtforms.form import BaseForm
from wtforms.validators import DataRequired


class FormCreator:
    def __init__(self, method, action):
        self.form = None
        self.method = method
        self.elements = {}
        self.action = action

    def build_form(self, request, csrf=False):
        base_form = BaseForm(self.elements)

        if csrf:
            base_form._csrf = None

        base_form.process(request.form)

        return base_form

    def add_text_field(self, name, required=False):
        try:
            self.elements[name] = StringField(name, [DataRequired()] if required else [])
        except KeyError as exception:
            print(exception)

    def add_number_field(self, name, required=False):
        try:
            self.elements[name] = IntegerField(name, [DataRequired()] if required else [])
        except KeyError as exception:
            print(exception)

    def add_select_field(self, name, options, required=False):
        try:
            self.elements[name] = SelectField(
                name,
                [DataRequired()] if required else [],
                choices=options
            )
        except KeyError as exception:
            print(exception)

    def add_checkbox_field(self, name, required=False):
        try:
            self.elements[name] = BooleanField(
                name,
                [DataRequired()] if required else []
            )
        except KeyError as exception:
            print(exception)

    def add_radio_field(self, name, required=False):
        try:
            self.elements[name] = RadioField(
                name,
                [DataRequired()] if required else []
            )
        except KeyError as exception:
            print(exception)
