#!/usr/bin/python3
"""
create a variable app_views which is an instance of Blueprint
(url prefix must be /api/v1)
"""
from flask import Blueprint
app_views = Blueprint(
        'app_views',
        __name__,
        static_folder='static',
        template_folder='templates'
        )
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
#from api.v1.views.places import *
#from api.v1.views.places_reviews import *
