from __future__ import annotations

import json

from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from pretix.base.models import Order
from rest_framework import status, viewsets
from rest_framework.decorators import action  # type: ignore
from rest_framework.response import Response

from .forms import ElectronicInvoiceForm


class ElectronicInvoiceViewSet(viewsets.ViewSet):
    permission = "can_edit_orders"

    lookup_field = "order_code"

    @action(methods=["POST"], detail=True)
    def update_invoice_information(
        self, request: HttpRequest, order_code: str
    ) -> Response:
        order = get_object_or_404(Order, code=order_code)

        body = request.body.decode("utf-8")
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # we use a form here instead of a serializer because we are reusing
        # the forms fields in the pretix contact form
        form = ElectronicInvoiceForm(data=body)

        if form.is_valid():
            meta_info = order.meta_info_data or {}  # type: ignore

            meta_info["pec"] = form.cleaned_data["pec"]
            meta_info["sdi"] = form.cleaned_data["sdi"]
            meta_info["codice_fiscale"] = form.cleaned_data["codice_fiscale"]

            order.meta_info = json.dumps(meta_info)  # type: ignore
            order.save(update_fields=["meta_info"])  # type: ignore

            return Response(
                {"code": order_code},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": form.errors, "other": form.non_field_errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )
