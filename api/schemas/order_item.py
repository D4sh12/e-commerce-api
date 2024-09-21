""" Module for the Order Item Schema """

from marshmallow import fields
from .base import BaseSchema
from .product import ProductSchema

class OrderItemSchema(BaseSchema):
    """ OrderItem Schema Class """

    quantity = fields.Integer(required=True)
    product = fields.Nested(ProductSchema(exclude=['quantity', 'brand_id', 'description', 'category_id', 'images']))

