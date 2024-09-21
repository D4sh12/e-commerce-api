""" Module for Order Items Model """

from .database import db
from .base import BaseModel

class OrderItem(BaseModel):
    """ OrderItem Model class """

    __tablename__ = 'order_items'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship('Product', backref='order_items', lazy='joined')

