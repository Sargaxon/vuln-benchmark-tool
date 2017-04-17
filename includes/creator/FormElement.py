# -*- coding: utf-8 -*-


class FormElement:
    def __init__(self, element_type, identifier, validators, choices=None):
        self.element_type = element_type
        self.identifier = identifier
        self.validators = validators
        self.choices = [] if not choices else choices
