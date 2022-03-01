import unittest
from django.test import TestCase
from ethracker.forms import TrackForm
from ethracker.models import Address


class TestAddressForm(TestCase):

  def test_eth_address(self):
    form = TrackForm(data={"eth_address": "uuuuuu"})

    self.assertEqual(
      form.errors["eth_address"], ["Only hexadecimal characters are allowed.",
                                   "Ensure this value has at least 40 characters (it has 6)."]
    )

    form = TrackForm(data={"eth_address": "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"})
    self.assertEqual(
      form.errors["eth_address"], ["Only hexadecimal characters are allowed.",
                                   "Ensure this value has at most 40 characters (it has 41)."]
    )

    form = TrackForm(data={"eth_address": "11111111111111111111111111111111111111111"})
    self.assertEqual(
      form.errors["eth_address"], ["Ensure this value has at most 40 characters (it has 41)."])

    form = TrackForm(
      data={"eth_address": "1111111111111111111111111111111111111111"})
    self.assertTrue(form.is_valid())
    form.save(commit=True)

    self.assertEqual(Address.objects.count(), 1)

