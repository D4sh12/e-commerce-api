""" Module for order endpoints """

from flask import request
from flask_restplus import Resource
from api.models.order import Order
from api.models.order_item import OrderItem
from api.schemas.order import OrderSchema
from api.middlewares.token_required import token_required
from api.utilities.helpers.swagger.collections import user_namespace
from api.utilities.helpers.swagger.models.order import order_item_model
from api.utilities.pagination_handler import paginate_resource
from api.utilities.helpers.responses import success_response, error_response
from api.utilities.helpers import request_data_strip
from api.utilities.validators.order import OrderValidators

@user_namespace.route('/orders')
class OrderResource(Resource):
    """ Resource class for order endpoints """

    @token_required
    def get(self):
        """ Endpoint to get user orders """
        order_schema = OrderSchema(many=True)
        user_id = request.decoded_token['user']['id']
        orders = Order.query.filter_by(user_id=user_id)
        
        # Paginate orders
        orders_data, meta = paginate_resource(orders, order_schema)
        
        # Calculate total amount for each order
        for order in orders:
            total_amount = sum(item.product.price * item.quantity for item in order.items)
            order.total_amount = total_amount

        orders_data = order_schema.dump(orders)

        success_response['message'] = 'Orders successfully fetched'
        success_response['data'] = {
            'orders': orders_data,
            'meta': meta
        }
        return success_response, 200

    @token_required
    @user_namespace.expect(order_item_model)
    def post(self):
        """ Endpoint to create a new order """
        request_data = request.get_json()
        OrderValidators.validate_order(request_data)
        request_data = request_data_strip(request_data)
        user_id = request.decoded_token['user']['id']

        # Extract items from request data
        items_data = request_data.pop('items', [])
        request_data.update({'user_id': user_id})

        # Create the new order
        new_order = Order(**request_data)
        new_order.save()

        # Create order items
        for item_data in items_data:
            item_data.update({'order_id': new_order.id})
            new_order_item = OrderItem(**item_data)
            new_order_item.save()

        order_schema = OrderSchema()
        success_response['message'] = 'Order successfully created'
        success_response['data'] = {'order': order_schema.dump(new_order)}
        return success_response, 201

@user_namespace.route('/orders/<int:order_id>')
class SingleOrderResource(Resource):
    """ Resource class for single order endpoints """

    @token_required
    def get(self, order_id):
        """ Endpoint to get a single order """
        order_schema = OrderSchema()
        user_id = request.decoded_token['user']['id']
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()

        if not order:
            error_response['message'] = 'Order not found'
            return error_response, 404

        success_response['message'] = 'Order successfully fetched'
        success_response['data'] = {'order': order_schema.dump(order)}
        return success_response, 200

    @token_required
    def delete(self, order_id):
        """ Endpoint to delete an order """
        user_id = request.decoded_token['user']['id']
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()

        if not order:
            error_response['message'] = 'Order not found'
            return error_response, 404
        
        if order.status != "Pending":
            error_response['message'] = 'Order cannot be deleted'
            return error_response, 400

        order.delete()
        success_response['message'] = 'Order successfully deleted'
        return success_response, 200

