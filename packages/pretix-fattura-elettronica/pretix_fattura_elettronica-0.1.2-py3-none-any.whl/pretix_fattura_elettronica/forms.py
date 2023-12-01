from __future__ import annotations

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from codicefiscale import codicefiscale


def validate_cf(value: str):
    if not codicefiscale.is_valid(value):
        raise ValidationError(_("Codice fiscale is not valid."))


class ElectronicInvoiceForm(forms.Form):
    pec = forms.EmailField(
        label=_("PEC"),
        help_text=_("Your PEC address. It will be used to send you the invoice."),
        required=False,
    )
    sdi = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "data-display-dependency": "#id_is_business_1",
                "data-required-if": "#id_is_business_1",
            }
        ),
        label=_("SDI"),
        help_text=_("Your SDI code."),
        max_length=7,
        min_length=7,
        required=False,
    )
    codice_fiscale = forms.CharField(
        widget=forms.TextInput(attrs={"data-display-dependency": "#id_is_business_0"}),
        label=_("Codice fiscale"),
        help_text=_("Your Codice fiscale."),
        max_length=16,
        min_length=16,
        required=False,
        validators=[validate_cf],
    )
