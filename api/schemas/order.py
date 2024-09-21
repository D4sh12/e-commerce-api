""" Module for the Order Schema """

from marshmallow import fields
from .base import BaseSchema
from .user import UserSchema
from .order_item import OrderItemSchema

class OrderSchema(BaseSchema):
    """ Order Schema Class """

    user = fields.Nested(UserSchema(exclude=['password', 'is_admin', 'is_activated']))
    items = fields.Nested(OrderItemSchema(many=True))
    total_amount = fields.Float(dump_only=True)  # Add this line
