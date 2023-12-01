from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from pretix.base.models import LoggedModel


class DestinatarioFatturaElettronica(LoggedModel):
    order = models.OneToOneField(
        "pretixbase.Order",
        verbose_name=_("Fattura Order"),
        on_delete=models.CASCADE,
        related_name="dest_fattura_elettronica_order",
    )
    codice_destinatario = models.CharField(
        max_length=7, verbose_name=_("Codice Destinatario")
    )
    pec_address = models.EmailField(
        max_length=100, verbose_name=_("PEC"), null=True, blank=True
    )

    class Meta:
        unique_together = ("order", "codice_destinatario")
