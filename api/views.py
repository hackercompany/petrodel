from rest_framework.views import APIView
from rest_framework.response import Response
from models import *
from methods import Methods
from datetime import datetime

# Create your views here.


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
        user = request.data.get('username')
        order_id = self.m.get_txn_id()
        product_type = request.data.get('p_type')
        address = request.data.get('address')
        quantity = float(request.data.get('quantity', '0'))
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
                           created_at=created_at)
            order.save()
            resp['status'] = 'success'
            resp['order_id'] = order_id
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
                           created_at=created_at)
            order.save()
            resp['status'] = 'success'
            resp['order_id'] = order_id
        return Response(resp, status=200)

    def get(self, request):
        resp = {'status': 'failed'}
        order_id = request.GET.get('order_id')
        order = Orders.objects.filter(order_id=order_id)
        if order:
            order = order[0]
            resp['order_id'] = order_id
            resp['username'] = order.user
            resp['p_type'] = order.product
            resp['quantity'] = order.quantity
            resp['rate'] = order.rate
            resp['amount'] = order.amount
            resp['status'] = order.status
            resp['address'] = order.address
            resp['created_at'] = order.created_at.date()
            resp['channel_partner'] = order.channel_partner.name
            if order.driver:
                resp['driver_name'] = order.driver.name
                resp['driver_mobile'] = order.driver.mobile
        return Response(resp, status=200)


class UserOrders(APIView):
    def get(self, request):
        resp = {'status': 'failed'}
        orders = Orders.objects.filter(user=request.GET.get('username'))
        if orders:
            resp['status'] = 'success'
            resp['data'] = []
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
                resp['data'].append(data)
        return Response(resp, status=200)
