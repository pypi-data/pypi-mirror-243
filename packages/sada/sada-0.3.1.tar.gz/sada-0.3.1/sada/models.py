from django.db.models import Model
from django.db.models.fields import BooleanField, CharField, DateTimeField, TextField
from django.db.models.fields.json import JSONField
from django.urls import reverse


class Product(Model):
    active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    description = TextField(null=True, blank=True)
    metadata = JSONField(default=dict, blank=True)
    name = CharField(max_length=255)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])
