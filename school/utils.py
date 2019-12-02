

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import random

def get_if_exists(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:  # Be explicit about exceptions
        obj = None
    return obj