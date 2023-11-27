from django.forms.models import ModelForm

from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["active", "description", "metadata", "name"]
