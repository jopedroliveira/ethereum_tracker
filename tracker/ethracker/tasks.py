import time
from datetime import timedelta
import requests

# Celery
from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.utils import timezone
from django.core.mail import EmailMessage

# Django
from django.core.mail import send_mail
from django.conf import settings

# Project
from .models import Address

# @periodic_task(run_every=timedelta(seconds=60))
def fetch_balance_from_api():
   addresses = Address.list_all()
   for address in addresses:
      try:
         # todo: multiple
         url = f"{settings.ETHSCAN_HOST}?" \
               f"module=account&action=balance&" \
               f"address=0x{address.address}&" \
               f"tag=latest&" \
               f"apikey={settings.ETHSCAN_API_KEY}"
         response = requests.get(url)
         if response.status_code == 200:
           eth_data = response.json()
           current_blc = eth_data['result']
           address.update_current_balance(current_blc)
           # todo: not correct
           address.update_confirmed_balance(current_blc, 0)
      except Exception as e:
         print(e)

# @periodic_task(run_every=timedelta(seconds=180))
def fetch_confirmed_balance_from_api():
  addresses = Address.list_all()
  for address in addresses:
    try:
      # todo: call API
      # todo: multiple
      # url = f"{settings.ETHSCAN_HOST}?" \
      #       f"module=account&action=balance&" \
      #       f"address=0x{address.address}&" \
      #       f"tag=latest&" \
      #       f"apikey={settings.ETHSCAN_API_KEY}"
      # response = requests.get(url)
      # if response.status_code == 200:
      #   eth_data = response.json()
      #   current_blc = eth_data['result']
      #   current_no_blocks = eth_data['blocks']
      #   address.update_confirmed_balance(current_blc, current_no_blocks)
      # else:
      #   pass
      pass
    except Exception as e:
      print(e)