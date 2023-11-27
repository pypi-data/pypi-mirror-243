from collections import UserString

from django import forms
from django.core.validators import EMPTY_VALUES
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from trix_widget.widgets import TrixWidget


class TrixFormField(forms.CharField):
    widget = TrixWidget


class TrixString(UserString):

    @property
    def as_html(self):
        return format_html(self.data)


def to_python(value):
    if value in EMPTY_VALUES:
        return TrixString('')

    return TrixString(value)


class TrixDescriptor:
    """Descriptor class to allow accessing the 'as_html' property of the field.

    """

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # The instance dict contains whatever was originally assigned in
        # __set__.
        if self.field.name in instance.__dict__:
            value = instance.__dict__[self.field.name]
        else:
            instance.refresh_from_db(fields=[self.field.name])
            value = getattr(instance, self.field.name)
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = to_python(value)


class TrixField(models.TextField):
    descriptor_class = TrixDescriptor

    description = _("Trix-editor field")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, *args, **kwargs):
        super().contribute_to_class(cls, name, *args, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))

    def formfield(self, **kwargs):
        defaults = {
            "form_class": TrixFormField,
            "error_messages": self.error_messages,
            "widget": TrixWidget
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
