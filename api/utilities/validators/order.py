""" Module for order validators """

from api.models.product import Product
from . import raise_validation_error, is_positive_integer

class OrderValidators:
    """ Order validators class """

    @classmethod
    def validate_order(cls, data: dict):
        """ Validates the order """
        items = data.get('items', [])
        if not items:
            raise_validation_error('Order must contain at least one item')

        for item in items:
            cls.validate_item(item)

    @classmethod
    def validate_item(cls, item: dict):
        """ Validates an order item """
        product_id = item.get('product_id')
        quantity = item.get('quantity')

        if product_id is None:
            raise_validation_error('The product ID is required')

        if not is_positive_integer(product_id):
            raise_validation_error('The product ID should be a positive integer')

        product = Product.find_by_id(product_id)
        if not product:
            raise_validation_error('The product ID provided doesn\'t exist')

        if quantity is None:
            raise_validation_error('The product quantity is required')

        if not is_positive_integer(quantity):
            raise_validation_error('The product quantity should be a positive integer')

        if product.quantity < quantity:
            raise_validation_error('The product is not available in the requested quantity')

