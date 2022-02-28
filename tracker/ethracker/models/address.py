from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.utils import timezone
from .mixins import CoreModel

address_validator = RegexValidator(r'^[a-fA-F0-9]*$',
                                   'Only hexadecimal characters are allowed.')


class Address(models.Model, CoreModel):
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
    # todo: validate address
    return cls.objects.create(address=address)

  @classmethod
  def list_all(cls):
    return cls.objects.all().order_by('id')

  @classmethod
  def get_by_ethaddr(cls, ethaddr):
    try:
      return cls.objects.get(address=ethaddr)
    except Exception as e:
      print(e)

  def update_current_balance(self, balance):
    self.set('current_balance', balance)
    self.set('last_updated', timezone.now())

  def update_confirmed_balance(self, balance, no_blocks):
    #fixme: must be confirmed balance
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
