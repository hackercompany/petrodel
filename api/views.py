from rest_framework.views import APIView
from rest_framework.response import Response
from models import *
from methods import Methods
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class ChannelPartnerRegistration(APIView):
    @csrf_exempt
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
        return Response(resp, status=200)


class UserLogin(APIView):
    def post(self, request):
        resp = {'status': 'failed'}
        username = request.data.get('username')
        password = request.data.get('password')
        user = Users.objects.filter(username=username, password=password)
        if user:
            resp['status'] = 'success'
        return Response(resp, status=200)


class Register(APIView):
    @csrf_exempt
    def post(self, request):
        resp = {'status': 'failed'}
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        u = Users(username=username, password=password, name=name)
        u.save()
        resp['status'] = 'success'
        return Response(resp, status=200)

    @csrf_exempt
    def get(self, request):
        resp = {'status': 'failed'}
        u = Users.objects.all()
        resp['data'] = []
        resp['meta'] = {'total_order': 0, 'total_users': 0, 'total_assets': 0}
        for user in u:
            temp_data = {}
            temp_data['name'] = user.name
            temp_data['username'] = user.username
            temp_data['assets'] = UserAssets.objects.filter(user=user).count()
            temp_data['orders'] = Orders.objects.filter(user=user).count()
            resp['meta']['total_order'] += temp_data['orders']
            resp['meta']['total_users'] += 1
            resp['meta']['total_assets'] += temp_data['assets']
            resp['data'].append(temp_data)
            resp['status'] = 'success'
        return Response(resp, status=200)


class PartnerOrderAction(APIView):
    def __init__(self):
        self.m = Methods()

    @csrf_exempt
    def post(self, request):
        client = self.m.get_redis_client()
        resp = {'status': 'failed'}
        action_type = request.data.get('action_type')
        order_id = request.data.get('order_id')
        o = Orders.objects.filter(order_id=order_id)
        if o:
            o = o[0]
            if action_type == "accept":
                o.status = "ACCEPTED"
                o.save()
                resp['status'] = 'success'
            elif action_type == "ass_driver":
                driver_id = client.get('driveronline')
                if driver_id:
                    driver = Driver.objects.get(id=driver_id)
                    o.driver = driver
                    o.status = "DRVR_ASS"
                    o.save()
                    resp['status'] = 'success'
        return Response(resp, status=200)


class PartnerDriverAction(APIView):
    def post(self, request):
        resp = {'status': 'failed'}
        driver_name = request.data.get('driver_name')
        action_type = request.data.get('action_type')
        driver = Driver.objects.filter(name=driver_name)
        if driver:
            driver = driver[0]
            if action_type == "disable":
                driver.status = "disable"
                driver.save()
                resp['status'] = 'success'
        return Response(resp, status=200)


class PartnerVehicalAction(APIView):
    def post(self, request):
        resp = {'status': 'failed'}
        action_type = request.data.get('action_type')
        reg_no = request.data.get('reg_no')
        v = Vehicals.objects.filter(reg_no=reg_no)
        if v:
            v = v[0]
            if action_type == "disable":
                v.status = "disable"
                v.save()
                resp["status"] = "success"
        return Response(resp, status=200)


class Rating(APIView):
    def post(self, request):
        resp = {'status': 'failed'}
        order_id = request.data.get('order_id')
        rating = request.data.get('rating')
        o = Orders.objects.filter(order_id=order_id)
        if o:
            o = o[0]
            o.rating = float(rating)
            resp['status'] = 'success'
            o.save()
        return Response(resp, status=200)


class DriverOrderManagement(APIView):
    def post(self, request):
        resp = {'status': 'failed'}
        order_id = request.data.get('order_id')
        action_type = request.data.get('action_type')
        o = Orders.objects.filter(order_id=order_id)
        if o:
            o = o[0]
            o.driver.status = "active"
            if action_type == "onway":
                o.status = "DISPATCHED"
            elif action_type == "accept":
                o.status = "ARR_PP"
            elif action_type == "reject":
                o.status = "REJECTED"
            elif action_type == "delivered":
                o.status = "DELIVERED"
            resp['status'] = 'success'
            o.save()
            o.driver.save()
        return Response(resp, status=200)

    def get(self, request):
        resp = {'status': 'failed'}
        driver_name = request.GET.get('driver_name')
        driver = Driver.objects.filter(name=driver_name)
        if driver:
            resp['status'] = 'success'
            resp['data'] = []
            driver = driver[0]
            orders = Orders.objects.filter(driver=driver)
            for order in orders:
                temp_data = {}
                temp_data['status'] = 'success'
                temp_data['order_id'] = order.order_id
                temp_data['username'] = order.user.username
                temp_data['name'] = order.user.name
                temp_data['p_type'] = order.product
                temp_data['quantity'] = order.quantity
                temp_data['rate'] = order.rate
                temp_data['amount'] = order.amount
                temp_data['status'] = order.status
                temp_data['address'] = order.asset.address
                temp_data['latitude'] = order.asset.latitude
                temp_data['longitude'] = order.asset.longitude
                temp_data['tag_id'] = order.asset.tag_id
                temp_data['created_at'] = order.created_at.date()
                temp_data['channel_partner'] = order.channel_partner.name
                temp_data['channel_partner_latitude'] = order.channel_partner.latitude
                temp_data['channel_partner_longitude'] = order.channel_partner.longitude
                temp_data['rating'] = order.rating
                resp['data'].append(temp_data)
        return Response(resp, status=200)


class DriverManagement(APIView):
    @csrf_exempt
    def post(self, request):
        resp = {'status': 'failed'}
        name = request.data.get('name')
        address = request.data.get('address')
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        if not password:
            password = 'relpetrodel'
        vehical = Vehicals.objects.all().first()
        d = Driver(name=name, address=address,
                   mobile=mobile, rating=5, status="online",
                   vehical=vehical, password=password)
        d.save()
        resp['status'] = 'success'
        return Response(resp, status=200)

    @csrf_exempt
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


class DriverLogin(APIView):
    def __init__(self):
        self.m = Methods()

    def post(self, request):
        resp = {'status': 'failed'}
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        driver = Driver.objects.filter(mobile=mobile, password=password)
        if driver:
            client = self.m.get_redis_client()
            client.set('driveronline', driver[0].id)
            resp['status'] = 'success'
            resp['driver_name'] = driver[0].name
        return Response(resp, status=200)


class DriverLogout(APIView):
    def __init__(self):
        self.m = Methods()

    def post(self, request):
        resp = {'status': 'failed'}
        mobile = request.data.get('mobile')
        client = self.m.get_redis_client()
        client.delete('driveronline')
        resp['status'] = 'success'
        return Response(resp, status=200)


class VehicleManagement(APIView):
    @csrf_exempt
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
        return Response(resp, status=200)

    @csrf_exempt
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
    @csrf_exempt
    def post(self, request):
        resp = {'status': 'failed'}
        username = request.data.get('username')
        user = Users.objects.filter(username=username)
        if user:
            user = user[0]
            asset_name = request.data.get('assetname')
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')
            sap_id = request.data.get('sap_id')
            tag_id = request.data.get('tag_id')
            address = request.data.get('address')
            capacity = request.data.get('capacity')
            asset = UserAssets(user=user, name=asset_name, latitude=latitude,
                               longitude=longitude, sap_id=sap_id,
                               tag_id=tag_id, address=address,
                               capacity=capacity, status="active")
            try:
                asset.save()
                resp['status'] = 'success'
            except Exception:
                resp['reason'] = 'Sap id already registred'
        return Response(resp, status=200)

    @csrf_exempt
    def get(self, request):
        resp = {'status': 'failed'}
        username = request.GET.get('username')
        user = Users.objects.filter(username=username)
        if user:
            resp['data'] = []
            user = user[0]
            assets = UserAssets.objects.filter(user=user, status="active")
            for asset in assets:
                temp_data = {
                    'asset_name': asset.name,
                    'sap_id': asset.sap_id,
                    'address': asset.address,
                    'tag_id': asset.tag_id,
                    'latitude': asset.latitude,
                    'longitude': asset.longitude,
                    'capacity': asset.capacity
                }
                resp['data'].append(temp_data)
                resp['status'] = 'success'
        return Response(resp, status=200)


class AssetDelete(APIView):
    def post(self, request):
        resp = {"status": "failed"}
        sap_id = request.data.get('sap_id')
        asset = UserAssets.objects.filter(sap_id=sap_id)
        if asset:
            asset = asset[0]
            asset.status = "inactive"
            asset.save()
            resp['status'] = 'success'
        return Response(resp)


class ChannelPartnerOrder(APIView):
    def __init__(self):
        self.m = Methods()

    @csrf_exempt
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
                data['username'] = order.user.name
                data['p_type'] = order.product
                data['quantity'] = order.quantity
                data['rate'] = order.rate
                data['amount'] = order.amount
                data['status'] = order.status
                data['address'] = order.asset.address
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

    @csrf_exempt
    def post(self, request):
        resp = {'status': 'failed'}
        username = request.data.get('username')
        user = Users.objects.get(username=username)
        order_id = self.m.get_txn_id()
        product_type = request.data.get('p_type')
        quantity = float(request.data.get('quantity', '0'))
        sap_id = request.data.get('sap_id')
        rate = 79.72
        amount = quantity * rate
        status = 'ODR_PL'
        created_at = datetime.now()
        channel_partner = ChannelPartner.objects.all().first()
        asset = UserAssets.objects.filter(sap_id=sap_id)
        if not asset:
            return Response(resp, status=200)
        asset = asset[0]
        if amount > 0:
            order = Orders(product=product_type, quantity=quantity,
                           rate=rate, amount=amount, status=status,
                           channel_partner=channel_partner, user=user,
                           order_id=order_id, address=address,
                           created_at=created_at, asset=asset)
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

    @csrf_exempt
    def post(self, request):
        resp = {'status': 'failed'}
        username = request.data.get('username')
        user = Users.objects.filter(username=username)
        if not user:
            resp['reason'] = 'User Not Found'
            return Response(resp, status=403)
        user = user[0]
        order_id = self.m.get_txn_id()
        product_type = request.data.get('p_type')
        quantity = float(request.data.get('quantity', '0'))
        sap_id = request.data.get('sap_id')
        rate = 79.72
        amount = quantity * rate
        status = 'ODR_PL'
        created_at = datetime.now()
        channel_partner = ChannelPartner.objects.all().first()
        asset = UserAssets.objects.filter(sap_id=sap_id)
        if not asset:
            return Response(resp, status=200)
        asset = asset[0]
        if amount > 0:
            order = Orders(product=product_type, quantity=quantity,
                           rate=rate, amount=amount, status=status,
                           channel_partner=channel_partner, user=user,
                           order_id=order_id, created_at=created_at,
                           asset=asset)
            order.save()
            resp['status'] = 'success'
            resp['order_id'] = order_id
            resp['latitude'] = channel_partner.latitude
            resp['longitude'] = channel_partner.longitude
            resp['channel_partner'] = channel_partner.name
        return Response(resp, status=200)

    @csrf_exempt
    def get(self, request):
        resp = {'status': 'failed'}
        order_id = request.GET.get('order_id')
        order = Orders.objects.filter(order_id=order_id)
        if order:
            order = order[0]
            resp['order_id'] = order_id
            resp['username'] = order.user.username
            resp['name'] = order.user.name
            resp['p_type'] = order.product
            resp['quantity'] = order.quantity
            resp['rate'] = order.rate
            resp['amount'] = order.amount
            resp['status'] = order.status
            resp['address'] = order.asset.address
            resp['latitude'] = order.asset.latitude
            resp['longitude'] = order.asset.longitude
            resp['tag_id'] = order.asset.tag_id
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
    @csrf_exempt
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
                data['name'] = order.user.name
                data['p_type'] = order.product
                data['quantity'] = order.quantity
                data['rate'] = order.rate
                data['amount'] = order.amount
                data['status'] = order.status
                data['address'] = order.asset.address
                data['latitude'] = order.asset.latitude
                data['longitude'] = order.asset.longitude
                data['tag_id'] = order.asset.tag_id
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
