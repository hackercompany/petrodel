# urls.py

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^partner/action/vehical', views.PartnerVehicalAction.as_view()),
    url(r'^partner/action/driver', views.PartnerDriverAction.as_view()),
    url(r'^partner/action/order', views.PartnerOrderAction.as_view()),
    url(r'^partner/register', views.ChannelPartnerRegistration.as_view()),
    url(r'^partner/order', views.ChannelPartnerOrder.as_view()),
    url(r'^user/register', views.Register.as_view()),
    url(r'^user/login', views.UserLogin.as_view()),
    url(r'^user/order', views.UserOrders.as_view()),
    url(r'^user/rating', views.Rating.as_view()),
    url(r'^driver/order', views.DriverOrderManagement.as_view()),
    url(r'^driver/login', views.DriverLogin.as_view()),
    url(r'^driver/logout', views.DriverLogout.as_view()),
    url(r'^driver/', views.DriverManagement.as_view()),
    url(r'^order/', views.OrderManagement.as_view()),
    url(r'^vehical/', views.VehicleManagement.as_view()),
    url(r'^asset/delete', views.AssetDelete.as_view()),
    url(r'^asset/', views.AssetManagement.as_view()),
    url(r'^schedule/', views.AutoAssignDriver.as_view()),
    url(r'^invoice/', views.Invoice.as_view()),
]
