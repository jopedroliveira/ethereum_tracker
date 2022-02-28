from django.shortcuts import render
from django.urls import resolve
from django.views.generic import View
from ethracker.models import Address
from ethracker.forms import TrackForm


class HomeLogic:
  def addresses_list(self, request, *args, **kwargs):
    try:
      # from .tasks import fetch_from_api
      # fetch_from_api()
      context = {'addresses': Address.list_all()}
      return render(request, 'home.html', context)
    except Exception as e:
      print(e)
      return render(request, '500.html', {})



class HomeController(View, HomeLogic):
  def get(self, request, *args, **kwargs):
    url_name = resolve(request.path_info).url_name

    if url_name == 'home':
      return self.addresses_list(request, *args, **kwargs)
