# urls.py

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^partner/register', views.ChannelPartnerRegistration.as_view()),
    url(r'^driver/', views.DriverManagement.as_view()),
    url(r'^order/', views.OrderManagement.as_view()),
    url(r'^vehical/', views.VehicleManagement.as_view()),
    url(r'^asset/', views.AssetManagement.as_view()),
    url(r'^user/register', views.Register.as_view()),
    url(r'^user/order', views.UserOrders.as_view()),
    url(r'^partner/order', views.ChannelPartnerOrder.as_view()),
]
