from __future__ import annotations

from typing import Any, TypedDict
from typing_extensions import Unpack

from django.dispatch import receiver

from pretix.base.models import Order
from pretix.base.signals import order_paid

API_BASE_URL = "https://common-sandbox.api.acubeapi.com/"  # SANDBOX


class OrderPaidSignalKwargs(TypedDict):
    order: Order


@receiver(order_paid, dispatch_uid="fattura_elt")
def fattura_elettronica_sender(sender: Any, **kwargs: Unpack[OrderPaidSignalKwargs]):
    return _send_invoice_via_api(kwargs["order"])


def _send_invoice_via_api(order: Order) -> str:
    # TODO: do the real implementation here
    return "Fattura Elettronica"
