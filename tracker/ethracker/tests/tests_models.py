import unittest
from django.test import TransactionTestCase
from ethracker.models import Address


class TestAddressModel(TransactionTestCase):
  reset_sequences = True

  def setUp(self):
    ad1 = Address.create("0123456789012345678901234567890123456789")
    ad2 = Address.create("0123456789012345678901234567890123456799")
    self.ad1 = ad1
    self.ad2 = ad2

  def test_create(self):
    self.assertEqual(Address.objects.all().count(), 2)
    Address.create("0123456789012345678901234567890123456733")
    self.assertEqual(Address.objects.all().count(), 3)

  @unittest.expectedFailure
  def test_fails_create(self):
    Address.create("0123456789012345678901234567890123456732")
    Address.create("0123456789012345678901234567890123456732")

  def test_list_all(self):
    self.assertQuerysetEqual(Address.objects.all().order_by('id'), Address.list_all(), transform=lambda x: x)

  def test_get_by_ethaddr(self):
    self.assertEqual(Address.get_by_ethaddr('0123456789012345678901234567890123456789'), self.ad1)

  def test_update_current_balance(self):
    self.ad1.update_current_balance(321)
    self.assertEqual(self.ad1.current_balance, 321)

  def test_update_confirmed_balance(self):
    self.ad1.update_confirmed_balance(321, 32)
    self.assertEqual(self.ad1.confirmed_balance, 321)
    self.assertEqual(self.ad1.confirmed_blocks_no, 32)
