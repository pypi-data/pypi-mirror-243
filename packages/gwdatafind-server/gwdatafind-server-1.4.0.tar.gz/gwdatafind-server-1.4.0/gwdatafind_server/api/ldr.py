# -*- coding: utf-8 -*-
# Copyright (2023) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""Compatibility API for old LDR datafind routes.

The routes themselves are defined by the v1 API,
this module exists only to allow the LDR compatibility
blueprint to be independently registered (or not) with
the app.
"""

from .v1 import ldr_compat as blueprint  # noqa: F401
