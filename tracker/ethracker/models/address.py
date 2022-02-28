from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.utils import timezone
from .mixins import CoreModel

address_validator = RegexValidator(r'^[a-fA-F0-9]*$',
                                   'Only hexadecimal characters are allowed.')


class Address(models.Model, CoreModel):
  address = models.CharField(max_length=40, blank=False, null=False, unique=True)
  current_balance = models.DecimalField(max_digits=19, decimal_places=18,
                                        default=None, null=True, blank=True)
  confirmed_balance = models.DecimalField(max_digits=19, decimal_places=18,
                                          default=None, null=True, blank=True)
  confirmed_blocks_no = models.IntegerField(default=None, null=True, blank=True)
  total_deduced = models.DecimalField(max_digits=19, decimal_places=18,
                                      default=None, null=True, blank=True)
  total_deposit = models.DecimalField(max_digits=19, decimal_places=18,
                                      default=None, null=True, blank=True)
  last_updated = models.DateTimeField(default=timezone.now)
  creation_date = models.DateTimeField(default=timezone.now)

  @classmethod
  def create(cls, address):
    # todo: validate address
    return cls.objects.create(address=address)

  @classmethod
  def list_all(cls):
    return cls.objects.all()

  @classmethod
  def get_by_ethaddr(cls, ethaddr):
    try:
      return cls.objects.get(address=ethaddr)
    except Exception as e:
      print(e)


  def update_current_balance(self, balance):
    address.set('current_balance', balance)
    address.set('last_updated', timezone.now())


  def update_confirmed_balance(self, balance, no_blocks):
    diff = balance - self.current_balance
    if diff > 0:
      deposit = address.total_deposit + diff
      address.set('total_deposit', deposit)
    elif diff < 0:
      deduced = address.total_deduced + abs(diff)
      address.set('total_deduced', deduced)

    address.set('confirmed_balance', balance)
    address.set('confirmed_blocks_no', no_blocks)
