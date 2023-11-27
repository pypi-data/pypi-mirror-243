from django.db.models import Model
from django.db.models.deletion import PROTECT
from django.db.models.enums import TextChoices
from django.db.models.fields import (
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    IntegerField,
    TextField,
)
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey
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


class Price(Model):
    class Recurring(TextChoices):
        WEEK = "week", "Week"
        MONTH = "month", "Month"
        YEAR = "year", "Year"

    class Type(TextChoices):
        ONE_TIME = "one_time", "One Time"
        RECURRING = "recurring", "Recurring"

    active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    interval = CharField(
        max_length=255, choices=Recurring.choices, blank=True, null=True
    )
    interval_count = IntegerField(default=1, blank=True, null=True)
    metadata = JSONField(default=dict, blank=True)
    product = ForeignKey(Product, on_delete=PROTECT, related_name="prices")
    type = CharField(max_length=255, choices=Type.choices)
    unit_amount = DecimalField(max_digits=10, decimal_places=2)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        interval_display = (
            self.interval if self.interval_count == 1 else f"{self.interval}s"
        )
        return f"{self.product.name} ({self.interval_count} {interval_display}) - {self.unit_amount}"

    def get_absolute_url(self):
        return reverse("price_detail", args=[str(self.id)])
