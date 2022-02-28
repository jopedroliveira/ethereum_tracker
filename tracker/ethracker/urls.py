import ethracker.views as views
from django.urls import path

urlpatterns = [
  path('', views.HomeController.as_view(), name='home'),
  path('track', views.AddressController.as_view(), name='address_track'),
  path('status/<ethaddr>/', views.AddressController.as_view(),
       name='address_status')
]
