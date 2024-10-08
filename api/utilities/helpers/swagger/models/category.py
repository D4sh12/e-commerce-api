""" Module for Swagger category models """

from flask_restx import fields
from ..collections import (category_namespace)

category_model = category_namespace.model('Category', {
    'name': fields.String(required=True, description='Category name'),
    'description': fields.String(required=False, description='Category description'),
    'parent_id': fields.String(required=False, description='Category parent ID'),
})
