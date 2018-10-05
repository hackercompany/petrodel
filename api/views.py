from rest_framework.views import APIView
from rest_framework.response import Response
from models import *
from methods import Methods
from datetime import datetime

# Create your views here.


class ChannelPartnerRegistration(APIView):
    def post(self, request):
        resp = {'status': 'failed'}
        user = request.data.get('username')
        name = request.data.get('name')
        address = request.data.get('address')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        c = ChannelPartner(user=user, name=name, address=address,
                           latitude=latitude, longitude=longitude)
        c.save()
        resp['status'] = 'success'
        return Response(resp, status=201)


class Register(APIView):
    def post(self, request):
        resp = {'status': 'failed'}
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        u = Users(username=username, password=password, name=name)
        u.save()
        resp['status'] = 'success'
        return Response(resp, status=201)


class DriverManagement(APIView):
    def post(self, request):
        resp = {'status': 'failed'}
        name = request.data.get('name')
        address = request.data.get('address')
        mobile = request.data.get('mobile')
        d = Driver(name=name, address=address,
                   mobile=mobile, rating=5, status="online")
        d.save()
        resp['status'] = 'success'
        return Response(resp, status=201)

    def get(self, request):
        resp = {'status': 'failed'}
        resp['data'] = []
        d = Driver.objects.all()
        for driver in d:
            temp_data = {
                'name': driver.name,
                'mobile': driver.mobile,
                'status': driver.status
            }
            if driver.vehical:
                temp_data['reg_no'] = driver.vehical.reg_no
            resp['data'].append(temp_data)
        return Response(resp, status=200)


class VehicleManagement(APIView):
    def post(self, request):
        resp = {'status': 'failed'}
        channel_partner_username = request.data.get('channel_partner')
        channel_partner = ChannelPartner.objects.filter(
            user=channel_partner_username)
        if channel_partner:
            channel_partner = channel_partner[0]
            reg_no = request.data.get('reg_no')
            make = request.data.get('make')
            capacity = request.data.get('capacity')
            vehical = Vehicals(channel_partner=channel_partner,
                               reg_no=reg_no, make=make, capacity=capacity,
                               status="active")
            vehical.save()
            resp['status'] = 'success'
        return Response(resp, status=201)

    def get(self, request):
        resp = {'status': 'failed'}
        cp_name = request.GET.get('channel_partner')
        channel_partner = ChannelPartner.objects.filter(user=cp_name)
        if channel_partner:
            channel_partner = channel_partner[0]
            vehicals = Vehicals.objects.filter(channel_partner=channel_partner)
            resp['data'] = []
            for vehical in vehicals:
                temp_data = {}
                temp_data['reg_no'] = vehical.reg_no
                temp_data['make'] = vehical.make
                temp_data['status'] = vehical.status
                driver = Driver.objects.filter(vehical=vehical)
                if driver:
                    driver = driver[0]
                    temp_data['driver'] = driver.name
                    temp_data['driver_movile'] = driver.mobile
                resp['data'].append(temp_data)
                resp['status'] = 'success'
        return Response(resp, status=200)


class AssetManagement(APIView):
    def post(self, request):
        resp = {'status': 'failed'}
        username = request.data.get('username')
        user = Users.objects.filter(username=username)
        if user:
            user = user[0]
            asset_name = request.data.get('assetname')
            asset = UserAssets(user=user, name=asset_name)
            asset.save()
            resp['status'] = 'success'
        return Response(resp, status=201)

    def get(self, request):
        resp = {'status': 'failed'}
        username = request.GET.get('username')
        user = Users.objects.filter(username=username)
        if user:
            resp['data'] = []
            user = user[0]
            assets = UserAssets.objects.filter(user=user)
            for asset in assets:
                temp_data = {
                    'asset_name': asset.name
                }
                resp['data'].append(temp_data)
                resp['status'] = 'success'
        return Response(resp, status=200)


class ChannelPartnerOrder(APIView):
    def __init__(self):
        self.m = Methods()

    def get(self, request):
        resp = {'status': 'failed'}
        username = request.GET.get('channel_partner')
        channel_partner = ChannelPartner.objects.filter(user=username)
        if channel_partner:
            channel_partner = channel_partner[0]
        else:
            return Response(resp, status=200)
        orders = Orders.objects.filter(channel_partner=channel_partner)
        if orders:
            resp['status'] = 'success'
            resp['orders'] = []
            resp['meta'] = {'order_bookings': len(
                orders), 'canceled_bookings': 0, 'total_km': 2318,
                'gmv': 0, 'online_gmv': 0}
            for order in orders:
                data = {}
                data['order_id'] = order.order_id
                data['username'] = order.user
                data['p_type'] = order.product
                data['quantity'] = order.quantity
                data['rate'] = order.rate
                data['amount'] = order.amount
                data['status'] = order.status
                data['address'] = order.address
                data['created_at'] = order.created_at.date()
                data['channel_partner'] = order.channel_partner.name
                if order.driver:
                    data['driver_name'] = order.driver.name
                    data['driver_mobile'] = order.driver.mobile
                if order.status == "cancelled":
                    resp['meta']['canceled_bookings'] += 1
                resp['orders'].append(data)
                resp['meta']['gmv'] += order.amount
                resp['meta']['online_gmv'] = resp['meta']['gmv']
        return Response(resp, status=200)

    def post(self, request):
        resp = {'status': 'failed'}
        username = request.data.get('username')
        user = Users.objects.get(username=username)
        order_id = self.m.get_txn_id()
        product_type = request.data.get('p_type')
        address = request.data.get('address')
        quantity = float(request.data.get('quantity', '0'))
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        rate = 79.72
        amount = quantity * rate
        status = 'pending'
        created_at = datetime.now()
        channel_partner = ChannelPartner.objects.all().first()
        if amount > 0:
            order = Orders(product=product_type, quantity=quantity,
                           rate=rate, amount=amount, status=status,
                           channel_partner=channel_partner, user=user,
                           order_id=order_id, address=address,
                           created_at=created_at, latitude=latitude,
                           longitude=longitude)
            order.save()
            resp['status'] = 'success'
            resp['order_id'] = order_id
            resp['latitude'] = channel_partner.latitude
            resp['longitude'] = channel_partner.longitude
            resp['channel_partner'] = channel_partner.name
        return Response(resp, status=200)


class OrderManagement(APIView):
    def __init__(self):
        self.m = Methods()

    def post(self, request):
        resp = {'status': 'failed'}
        user = request.data.get('username')
        order_id = self.m.get_txn_id()
        product_type = request.data.get('p_type')
        address = request.data.get('address')
        quantity = float(request.data.get('quantity', '0'))
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        rate = 79.72
        amount = quantity * rate
        status = 'pending'
        created_at = datetime.now()
        channel_partner = ChannelPartner.objects.all().first()
        if amount > 0:
            order = Orders(product=product_type, quantity=quantity,
                           rate=rate, amount=amount, status=status,
                           channel_partner=channel_partner, user=user,
                           order_id=order_id, address=address,
                           created_at=created_at, latitude=latitude,
                           longitude=longitude)
            order.save()
            resp['status'] = 'success'
            resp['order_id'] = order_id
            resp['latitude'] = channel_partner.latitude
            resp['longitude'] = channel_partner.longitude
            resp['channel_partner'] = channel_partner.name
        return Response(resp, status=200)

    def get(self, request):
        resp = {'status': 'failed'}
        order_id = request.GET.get('order_id')
        order = Orders.objects.filter(order_id=order_id)
        if order:
            order = order[0]
            resp['order_id'] = order_id
            resp['username'] = order.user.username
            resp['p_type'] = order.product
            resp['quantity'] = order.quantity
            resp['rate'] = order.rate
            resp['amount'] = order.amount
            resp['status'] = order.status
            resp['address'] = order.address
            resp['latitude'] = order.latitude
            resp['longitude'] = order.longitude
            resp['created_at'] = order.created_at.date()
            resp['channel_partner'] = order.channel_partner.name
            resp['channel_partner_latitude'] = order.channel_partner.latitude
            resp['channel_partner_longitude'] = order.channel_partner.longitude
            resp['rating'] = order.rating
            if order.driver:
                resp['driver_name'] = order.driver.name
                resp['driver_mobile'] = order.driver.mobile
        return Response(resp, status=200)


class UserOrders(APIView):
    def get(self, request):
        resp = {'status': 'failed'}
        user = Users.objects.filter(username=request.GET.get('username'))
        if not user:
            return Response(resp, status=403)
        user = user[0]
        orders = Orders.objects.filter(user=user)
        if orders:
            resp['status'] = 'success'
            resp['data'] = []
            for order in orders:
                data = {}
                data['order_id'] = order.order_id
                data['username'] = order.user.username
                data['p_type'] = order.product
                data['quantity'] = order.quantity
                data['rate'] = order.rate
                data['amount'] = order.amount
                data['status'] = order.status
                data['address'] = order.address
                data['latitude'] = order.latitude
                data['longitude'] = order.longitude
                data['created_at'] = order.created_at.date()
                data['channel_partner'] = order.channel_partner.name
                data['channel_partner_latitude'] = order.channel_partner.latitude
                data['channel_partner_longitude'] = order.channel_partner.longitude
                data['rating'] = order.rating
                if order.driver:
                    data['driver_name'] = order.driver.name
                    data['driver_mobile'] = order.driver.mobile
                resp['data'].append(data)
        return Response(resp, status=200)
