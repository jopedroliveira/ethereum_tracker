import unittest
from django.test import TestCase
from django.utils import timezone
from django.urls import resolve, reverse
from ethracker.forms import TrackForm
from ethracker.models import Address


class TestHomeView(TestCase):

  def setUp(self):
    self.creation_date = timezone.now()
    ad1 = Address.objects.create(address="0123456789012345678901234567890123456789",
                                 creation_date=self.creation_date,
                                 last_updated=self.creation_date)

    ad2 = Address.objects.create(address="0123456789012345678901234567890123456799",
                                 creation_date=self.creation_date,
                                 last_updated=self.creation_date)

    self.ad1 = ad1
    self.ad2 = ad2

  def test_get_home(self):
    response = self.client.get(reverse('home'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['addresses'], Address.objects.all().order_by('id'),
                             transform=lambda x: x)


class TestAddressView(TestCase):

  def setUp(self):
    self.creation_date = timezone.now()
    ad1 = Address.objects.create(address="0123456789012345678901234567890123456789",
                                 creation_date=self.creation_date,
                                 last_updated=self.creation_date)
    self.ad1 = ad1

  def test_track_post(self):
    response = self.client.post(reverse('address_track'),
                                data={"eth_address":"0123456789012345678901234567890123456790"})
    self.assertRedirects(response, reverse('home'),
                         status_code=302,
                         target_status_code=200,
                         fetch_redirect_response=True)
    self.assertEqual(Address.objects.count(), 2)
    response = self.client.post(reverse('address_track'),
                                data={"eth_address": "012345678901234567890123456789012345679"})
    self.assertEqual(response.status_code, 200)

    self.assertEqual(response.context['form'].errors, {'eth_address': ['Ensure this value has at least 40 characters (it has 39).']})
