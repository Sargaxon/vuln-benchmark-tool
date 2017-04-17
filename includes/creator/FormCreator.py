# -*- coding: utf-8 -*-
from wtforms import *
from wtforms.form import BaseForm
from wtforms.validators import DataRequired

from includes.creator import FormElement


class FormCreator:
    def __init__(self, method, action, csrf=False):
        self.form = BaseForm({})
        self.elements = dict()
        self.method = method
        self.action = action

        if not csrf:
            self.form._csrf = None

    def set_field(self, element):
        self.form[element.identifier] = {
            "StringField": StringField(element.identifier, element.validators),
            "IntegerField": IntegerField(element.identifier, element.validators),
            "SelectField":  SelectField(element.identifier, element.validators, choices=element.choices),
            "BooleanField":  BooleanField(element.identifier, element.validators),
            "RadioField":  RadioField(element.identifier, element.validators)
        }[element.element_type]

    def build_form(self):
        for identifier, element in self.elements.items():
            self.set_field(element)

    def process_form(self, request):
        self.form.process(request.form)

        return self.form

    def add_text_field(self, name, required=False):
        try:
            self.elements[name] = FormElement("StringField", name, [DataRequired()] if required else [])
        except KeyError as exception:
            print(exception)

    def add_number_field(self, name, required=False):
        try:
            self.elements[name] = FormElement("IntegerField", name, [DataRequired()] if required else [])
        except KeyError as exception:
            print(exception)

    def add_select_field(self, name, required=False, options=None):
        if options is None:
            options = [("select", "Select")]

        try:
            self.elements[name] = FormElement(
                "SelectField",
                name,
                [DataRequired()] if required else [],
                choices=options
            )
        except KeyError as exception:
            print(exception)

    def add_checkbox_field(self, name, required=False):
        try:
            self.elements[name] = FormElement(
                "BooleanField",
                name,
                [DataRequired()] if required else []
            )
        except KeyError as exception:
            print(exception)

    def add_radio_field(self, name, required=False):
        try:
            self.elements[name] = FormElement(
                "RadioField",
                name,
                [DataRequired()] if required else []
            )
        except KeyError as exception:
            print(exception)

    def load_elements_from_form(self, base_form):
        for field in base_form:
            self.form[field.name] = field
