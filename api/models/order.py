""" Module for Order Model """

from .database import db
from .base import BaseModel

class Order(BaseModel):
    """ Order Model class """

    __tablename__ = 'orders'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    user = db.relationship('User', backref='orders', lazy='joined')
    items = db.relationship('OrderItem', backref='order', lazy='joined', cascade='all, delete-orphan')