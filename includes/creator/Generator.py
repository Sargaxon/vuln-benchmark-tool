# -*- coding: utf-8 -*-
import random, string


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
