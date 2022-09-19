from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password, make_password,
)
from django.utils.translation import gettext_lazy as _
from os.path import splitext
from time import time

def handle_upload_logo(instance, filename):
    _, extension = splitext(filename.lower())
    date = str(time())

    date = date[:date.index('.')]
    # date_string = f"{date.year}_{date.month}_{date.day}_{}"
    return f"logo/{date}{extension}".lower()

def handle_upload_passport(instance, filename):
    _, extension = splitext(filename.lower())
    date = str(time())

    date = date[:date.index('.')]
    # date_string = f"{date.year}_{date.month}_{date.day}_{}"
    return f"passport/{date}{extension}".lower()

# Create your models here.


class AssociationModelBase(models.Model):
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    is_active = True

    REQUIRED_FIELDS = []

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)


class AssociationManager(BaseUserManager):
    # username, email, password=None,firstname="user", lastname="user"):
    def create_association(self, **data):

        email = data.pop('email', None)
        password = data.pop('password', None)

        if email is None:
            raise TypeError('Association email is required')

        association = self.model(email=self.normalize_email(email), **data)

        association.set_password(password)

        association.save()
        return association

    def authenticate(self, **data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise TypeError('Association email is required')

        if password is None:
            raise TypeError('Association password is required')

        try:
            association = self.model.objects.get(
                email=self.normalize_email(email))
            # association = Association.objects.get(
            #     email=email, password=password)
        except self.model.DoesNotExist:
            return None

        valid_password = association.check_password(password)

        if not valid_password:
            return None

        return association
