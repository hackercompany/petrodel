from __future__ import unicode_literals

from mongoengine import *

# Create your models here.


class Users(Document):
    username = StringField(max_length=100, unique=True)
    password = StringField(max_length=250)
    name = StringField(max_length=200)


class UserAssets(Document):
    user = ReferenceField(Users)
    name = StringField(max_length=200)
    latitude = StringField(max_length=20)
    longitude = StringField(max_length=20)
    sap_id = StringField(max_length=12, unique=True)
    tag_id = StringField(max_length=20)
    address = StringField(max_length=200)
    capacity = IntField()


class ChannelPartner(Document):
    user = StringField(max_length=50, unique=True)
    name = StringField(max_length=200)
    address = StringField(max_length=200)
    latitude = StringField(max_length=20)
    longitude = StringField(max_length=20)


class Vehicals(Document):
    channel_partner = ReferenceField(ChannelPartner)
    reg_no = StringField(max_length=15, unique=True)
    make = StringField(max_length=50)
    capacity = StringField(max_length=10)
    status = StringField(max_length=10)


class Driver(Document):
    name = StringField(max_length=200)
    address = StringField(max_length=200)
    mobile = StringField(max_length=10, unique=True)
    rating = IntField()
    status = StringField(max_length=10)
    vehical = ReferenceField(Vehicals)
    latitude = StringField(max_length=20)
    longitude = StringField(max_length=20)
    password = StringField(max_length=100)


class Orders(Document):
    created_at = DateTimeField()
    user = ReferenceField(Users)
    order_id = StringField(max_length=50)
    product = StringField(max_length=50)
    quantity = FloatField()
    rate = FloatField()
    amount = FloatField()
    status = StringField(max_length=50)
    channel_partner = ReferenceField(ChannelPartner)
    driver = ReferenceField(Driver)
    rating = IntField()
    asset = ReferenceField(UserAssets)
