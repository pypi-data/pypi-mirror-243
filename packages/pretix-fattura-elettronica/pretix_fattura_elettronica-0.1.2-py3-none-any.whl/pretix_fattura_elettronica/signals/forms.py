from __future__ import annotations

from typing import Any

from pretix_fattura_elettronica.forms import ElectronicInvoiceForm

from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from codicefiscale import codicefiscale
from pretix.presale.signals import contact_form_fields


def validate_sdi_number(value: str):
    if not value.isdigit() or len(value) != 7:
        raise ValidationError(
            _("SDI number must be 7 digits long and contain only numbers.")
        )


def validate_cf(value: str):
    if not codicefiscale.is_valid(value):
        raise ValidationError(_("Codice fiscale is not valid."))


@receiver(contact_form_fields, dispatch_uid="fattura_elt")
def add_fields_to_contact_form_fields(sender: Any, **kwargs: Any):
    return ElectronicInvoiceForm.declared_fields
