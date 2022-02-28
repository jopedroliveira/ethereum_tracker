from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.utils import timezone
from .mixins import CoreModel

address_validator = RegexValidator(r'^[a-fA-F0-9]*$',
                                   'Only hexadecimal characters are allowed.')


class Address(models.Model, CoreModel):
  """
  Django model to store data from ethereum address
  """
  address = models.CharField(max_length=40, blank=False, null=False, unique=True)
  current_balance = models.BigIntegerField(default=None, null=True, blank=True)
  confirmed_balance = models.BigIntegerField(default=None, null=True, blank=True)
  confirmed_blocks_no = models.IntegerField(default=None, null=True, blank=True)
  total_deduced = models.BigIntegerField(default=0, null=False, blank=False)
  total_deposit = models.BigIntegerField(default=0, null=False, blank=False)
  last_updated = models.DateTimeField(default=timezone.now)
  creation_date = models.DateTimeField(default=timezone.now)

  @classmethod
  def create(cls, address):
    """
    Create an Address object and commits to database
    :param address:
    :return:
    """
    # todo: validate address
    new_address = cls.objects.create(address=address)
    new_address.force_update()
    return new_address

  @classmethod
  def list_all(cls):
    """
    List of Addresses on database
    :return:
    """
    return cls.objects.all().order_by('-creation_date')

  @classmethod
  def get_by_ethaddr(cls, ethaddr):
    """
    Find an address object on database by ethereum address
    :param ethaddr:
    :return:
    """
    try:
      return cls.objects.get(address=ethaddr)
    except Exception as e:
      print(e)

  def update_current_balance(self, balance):
    """
    Updates the current balance of an ethereum address
    :param balance:
    :return:
    """
    self.set('current_balance', int(balance))
    self.set('last_updated', timezone.now())

  def update_confirmed_balance(self, balance, no_blocks):
    """
    Updates the confirmed balance and number of confirm blocks of an ethereum address
    :param balance:
    :param no_blocks:
    :return:
    """
    #fixme: must be confirmed balance
    balance = int(balance)
    current_balance = self.current_balance if self.current_balance else 0
    diff = balance - current_balance
    if diff > 0:
      deposit = self.total_deposit + diff
      self.set('total_deposit', deposit)
    elif diff < 0:
      deduced = self.total_deduced + abs(diff)
      self.set('total_deduced', deduced)

    self.set('confirmed_balance', balance)
    self.set('confirmed_blocks_no', no_blocks)

  def force_update(self):
    """
    Triggers a celery task to update the Address data
    :return:
    """
    from ..tasks import fetch_force_update_api
    fetch_force_update_api.delay(self)

