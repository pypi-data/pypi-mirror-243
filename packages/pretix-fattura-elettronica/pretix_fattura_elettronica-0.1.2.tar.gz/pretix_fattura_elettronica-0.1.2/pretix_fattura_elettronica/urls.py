# django urls
from __future__ import annotations

from pretix.api.urls import router

from .views import ElectronicInvoiceViewSet

router.register("orders", ElectronicInvoiceViewSet, basename="orders")
