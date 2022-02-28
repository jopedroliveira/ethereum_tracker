from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

from .models import Address

address_validator = RegexValidator(r'^[a-fA-F0-9]*$',
                                   'Only hexadecimal characters are allowed.')
class TrackForm(forms.Form):
  """
  Form object to handle new eth address tracking requests
  """

  def __init__(self, *args, **kwargs):
    super(TrackForm, self).__init__(*args, **kwargs)

    self.fields['eth_address'] = forms.CharField(
                             validators=[address_validator, MinLengthValidator(40),
                                         MaxLengthValidator(40)],
      required=True)  # todo: attributes

  def clean_eth_address(self):
    pre_address = self.data['eth_address']
    a = Address.objects.filter(address=pre_address)
    if a.count() > 0:
      self.add_error("eth_address", "This address is already being tracked")
    return pre_address

  def save(self, commit=False):
    eth_address = self.cleaned_data['eth_address']

    if commit:
      try:
        address = Address.create(eth_address)
        return address
      except ValidationError as e:
        raise forms.ValidationError(e)
