from __future__ import annotations

from unittest.mock import patch

import pytest
from pretix.base.models import Event, Order
from pretix.base.signals import order_paid

from .utils import instance_mock


class TestInvoiceSending:
    @pytest.mark.django_db
    @patch("pretix_fattura_elettronica.signals.invoices._send_invoice_via_api")
    def test_send_invoice_called(self, mock_sig, request):
        with patch(
            "pretix_fattura_elettronica.signals.fattura_elettronica_sender"
        ) as mock_send_invoice:
            event = Event(pk="pk", name="PyConIT", plugins="pretix_fattura_elettronica")
            order = instance_mock(request, Order)
            order.event = event
            order_paid.connect(mock_send_invoice, dispatch_uid="fattura_elt")
            order_paid.send(order.event, order=order)

        mock_sig.assert_called_once_with(order)
