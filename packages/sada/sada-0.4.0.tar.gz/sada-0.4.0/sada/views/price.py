from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ..models import Price


@method_decorator(staff_member_required, name="dispatch")
class PriceCreateView(CreateView):
    model = Price
    template_name = "sada/price/price_form.html"
    fields = [
        "active",
        "interval",
        "interval_count",
        "metadata",
        "product",
        "type",
        "unit_amount",
    ]


@method_decorator(staff_member_required, name="dispatch")
class PriceListView(ListView):
    model = Price
    template_name = "sada/price/price_list.html"


@method_decorator(staff_member_required, name="dispatch")
class PriceDetailView(DetailView):
    model = Price
    template_name = "sada/price/price_detail.html"


@method_decorator(staff_member_required, name="dispatch")
class PriceUpdateView(UpdateView):
    model = Price
    template_name = "sada/price/price_form.html"
    fields = [
        "active",
        "interval",
        "interval_count",
        "metadata",
        "product",
        "type",
        "unit_amount",
    ]


@method_decorator(staff_member_required, name="dispatch")
class PriceDeleteView(DeleteView):
    model = Price
    template_name = "sada/price/price_confirm_delete.html"
    success_url = reverse_lazy("price_list")
