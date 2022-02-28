from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import resolve, reverse
from django.views.generic import View
from ..forms import *

class AddressLogic:
  def status(self, request, *args, **kwargs):
    try:
      ethaddr = kwargs['ethaddr'] if 'ethaddr' in kwargs else None
      address = Address.get_by_ethaddr(ethaddr)
      context = {'address': address}
      return render(request, 'details.html', context)
    except Exception as e:
      print(e)
      return render(request, '500.html', {})

  def track_get(self, request, *args, **kwargs):
    try:
      context = {}
      form = TrackForm()
      context['form'] = form
      return render(request, 'form.html', context)
    except Exception as e:
      print(e)
      return render(request, '500.html', {})

  def track_post(self, request, *args, **kwrags):
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
