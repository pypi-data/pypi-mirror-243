from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Product


@method_decorator(staff_member_required, name="dispatch")
class IndexView(TemplateView):
    template_name = "sada/index.html"


@method_decorator(staff_member_required, name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    template_name = "sada/product_form.html"
    fields = ["name", "description", "active", "metadata"]


@method_decorator(staff_member_required, name="dispatch")
class ProductListView(ListView):
    model = Product


@method_decorator(staff_member_required, name="dispatch")
class ProductDetailView(DetailView):
    model = Product


@method_decorator(staff_member_required, name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    template_name = "sada/product_form.html"
    fields = ["name", "description", "active", "metadata"]


@method_decorator(staff_member_required, name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "sada/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")
