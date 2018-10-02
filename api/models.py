from __future__ import unicode_literals

from mongoengine import *

# Create your models here.


class ChannelPartner(Document):
    user = StringField(max_length=50)
    name = StringField(max_length=200)
    address = StringField(max_length=200)


class Driver(Document):
    name = StringField(max_length=200)
    address = StringField(max_length=200)
    mobile = StringField(max_length=10)
    rating = IntField()


class Orders(Document):
    created_at = DateTimeField()
    user = StringField(max_length=50)
    order_id = StringField(max_length=50)
    product = StringField(max_length=50)
    quantity = FloatField()
    rate = FloatField()
    amount = FloatField()
    status = StringField(max_length=50)
    address = StringField(max_length=200)
    channel_partner = ReferenceField(ChannelPartner)
    driver = ReferenceField(Driver)
