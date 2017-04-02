# -*- coding: utf-8 -*-
import random
import string
import numpy


class Generator:
    @staticmethod
    def random_string(length, chars="letters+digits"):
        options = {"letters": string.ascii_letters,
                   "lowercase": string.ascii_lowercase,
                   "uppercase": string.ascii_uppercase,
                   "digits": string.digits,
                   "letters+digits": string.ascii_letters+string.digits,
                   }

        if chars in options:
            characters = options[chars]
        else:
            characters = chars

        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def random_number(a, b):
        return numpy.random.randint(low=a, high=b)

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
