from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import resolve, reverse
from django.views.generic import View
from ..forms import *
import json
import requests


class AddressLogic:
  """
  Logic class to Address requests
  """
  def status(self, request, *args, **kwargs):
    """
    Yields the status of a given eth address
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    try:
      page = request.GET.get('page', 1)
      items_per_page = request.GET.get('items', 7)
      ethaddr = kwargs['ethaddr'] if 'ethaddr' in kwargs else None
      address = Address.get_by_ethaddr(ethaddr)

      url = f"{settings.ETHSCAN_HOST}?" \
            f"module=account&" \
            f"action=txlist&" \
            f"address=0x{address.address}&" \
            f"startblock=0&" \
            f"endblock=99999999&" \
            f"page={page}&" \
            f"offset={items_per_page}&" \
            f"sort=asc&" \
            f"apikey={settings.ETHSCAN_API_KEY}"

      response = requests.get(url)
      response_data = {}
      if response.status_code == 200:
        response_data = response.json()

      context = {'address': address,
                 'transactions': response_data['result'],
                 'page': page,
                 'next_page': int(page)+1,
                 'previous_page': int(page)-1 if int(page) > 1 else 1}

      return render(request, 'details.html', context)
    except Exception as e:
      print(e)
      return render(request, '500.html', {})


  def track_get(self, request, *args, **kwargs):
    """
    Yields an empty form for registering an ethereum address
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    try:
      context = {}
      form = TrackForm()
      context['form'] = form
      return render(request, 'form.html', context)
    except Exception as e:
      print(e)
      return render(request, '500.html', {})


  @csrf_exempt
  def track_post(self, request, *args, **kwrags):
    """
    Register an ethereum address to start tracking
    :param request:
    :param args:
    :param kwrags:
    :return:
    """
    try:
      context = {}
      form = TrackForm(request.POST)
      if form.is_valid():
        # add message
        a = form.save(commit=True)
        messages.add_message(request, messages.SUCCESS,
                             f"New ETH Address {a.address} added")
        return redirect(reverse('home'))
      context['form'] = form
      return render(request, 'form.html', context)
    except Exception as e:
      print(e)
      return render(request, '500.html', {})


class AddressController(View, AddressLogic):
  """
  Address Page controller
  """
  def get(self, request, *args, **kwargs):
    url_name = resolve(request.path_info).url_name

    if url_name == 'address_status':
      return self.status(request, *args, **kwargs)
    elif url_name == 'address_track':
      return self.track_get(request, *args, **kwargs)
    else:
      # todo: unknown
      return None

  def post(self, request, *args, **kwargs):
    url_name = resolve(request.path_info).url_name

    if url_name == 'address_track':
      return self.track_post(request, *args, **kwargs)
    else:
      # todo: unknown
      return None
