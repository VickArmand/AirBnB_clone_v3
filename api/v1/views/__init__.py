#!/usr/bin/python3
"""
create a variable app_views which is an instance of Blueprint
(url prefix must be /api/v1)
"""
from flask import Blueprint
from api.v1.views.index import *
app_views = Blueprint(
        'app_views',
        __name__,
        static_folder='static',
        template_folder='templates'
        )
