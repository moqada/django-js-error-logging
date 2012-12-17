# -*- coding: utf-8 -*-
from .settings import STATIC_URL


def static(request):
    """ Add static js file root
    """
    return {
        'JSERRORLOGGING_STATIC_URL': STATIC_URL
    }
