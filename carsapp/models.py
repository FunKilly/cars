import uuid
from datetime import datetime

from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator

from .mixins import CICharField
from .managers import CarManager


class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = CICharField(max_length=40, blank=False, null=False)
    model = CICharField(max_length=40, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CarManager()

    class Meta:
        unique_together = ('brand', 'model',)

    def save(self, *args, **kwargs):
        for field_name in ['brand', 'model']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Car, self).save(*args, **kwargs)


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.ForeignKey(to=Car, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
