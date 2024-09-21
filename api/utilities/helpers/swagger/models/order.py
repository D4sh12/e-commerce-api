""" Module for Swagger order models """

from flask_restplus import fields
from ..collections import (user_namespace)

# order_model = user_namespace.model('Order', {
#     'id': fields.Integer(required=True, description='The order ID'),
#     'user_id': fields.Integer(required=True, description='The ID of the user who placed the order'),
#     'total_amount': fields.Float(required=True, description='The total amount of the order'),
#     'status': fields.String(required=True, description='The status of the order', enum=['Pending', 'Shipped', 'Delivered', 'Cancelled']),
#     'created_at': fields.DateTime(required=True, description='The timestamp when the order was created'),
#     'updated_at': fields.DateTime(required=True, description='The timestamp when the order was last updated')
# })

order_item_model = user_namespace.model('OrderItem', {
    'id': fields.Integer(required=True, description='The ID of the order item'),
    'order_id': fields.Integer(required=True, description='The ID of the order that this item belongs to'),
    'product_id': fields.Integer(required=True, description='The ID of the product'),
    'quantity': fields.Integer(required=True, description='The quantity of the product in the order'),
    'created_at': fields.DateTime(required=True, description='The timestamp when the order item was created'),
    'updated_at': fields.DateTime(required=True, description='The timestamp when the order item was last updated')
})

