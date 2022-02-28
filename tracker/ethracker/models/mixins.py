from django.db import models
from django.apps import apps
from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError

class CoreModel(object):

  def set(self, field, value):
    try:
      setattr(self, field, value)
      self.save(update_fields=[field])
      return True
    except:
      raise PermissionDenied(
        "{} doesn't have {} as field".format(self.__class__.__name__), field)