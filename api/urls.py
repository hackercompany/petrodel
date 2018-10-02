# urls.py

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^order/', views.OrderManagement.as_view()),
    url(r'^user/order', views.UserOrders.as_view()),
    url(r'^partner/order', views.ChannelPartnerOrder.as_view()),
]
