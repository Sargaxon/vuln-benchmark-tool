#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from benchmark import app
from benchmark import PORT

if __name__ == '__main__':
    port = int(os.environ.get("PORT", PORT))
    app.run('0.0.0.0', port=port)
