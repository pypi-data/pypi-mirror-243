"""Functions that make mocking with pytest easier and more readable."""
from __future__ import annotations

from unittest.mock import ANY, PropertyMock, call, create_autospec, patch  # noqa

from django.utils import timezone

from django_countries.fields import Country
from pretix.base.models import Invoice, Order
from pretix.base.services.invoices import build_invoice, generate_cancellation


def class_mock(request, q_class_name, autospec=True, **kwargs):
    """Return mock patching class with qualified name *q_class_name*.

    The mock is autospec'ed based on the patched class unless the optional
    argument *autospec* is set to False. Any other keyword arguments are
    passed through to Mock(). Patch is reversed after calling test returns.
    """
    _patch = patch(q_class_name, autospec=autospec, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def function_mock(request, q_function_name, autospec=True, **kwargs):
    """Return mock patching function with qualified name *q_function_name*.

    Patch is reversed after calling test returns.
    """
    _patch = patch(q_function_name, autospec=autospec, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def initializer_mock(request, cls, autospec=True, **kwargs):
    """Return mock for __init__() method on *cls*.

    The patch is reversed after pytest uses it.
    """
    _patch = patch.object(
        cls, "__init__", autospec=autospec, return_value=None, **kwargs
    )
    request.addfinalizer(_patch.stop)
    return _patch.start()


def instance_mock(request, cls, name=None, spec_set=True, **kwargs):
    """Return mock for instance of *cls* that draws its spec from the class.

    The mock will not allow new attributes to be set on the instance. If
    *name* is missing or |None|, the name of the returned |Mock| instance is
    set to *request.fixturename*. Additional keyword arguments are passed
    through to the Mock() call that creates the mock.
    """
    name = name if name is not None else request.fixturename
    return create_autospec(cls, _name=name, spec_set=spec_set, instance=True, **kwargs)


def method_mock(request, cls, method_name, autospec=True, **kwargs):
    """Return mock for method *method_name* on *cls*.

    The patch is reversed after pytest uses it.
    """
    _patch = patch.object(cls, method_name, autospec=autospec, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def property_mock(request, cls, prop_name, **kwargs):
    """Return mock for property *prop_name* on class *cls*.

    The patch is reversed after pytest uses it.
    """
    _patch = patch.object(cls, prop_name, new_callable=PropertyMock, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def generate_invoice(order: Order):
    invoice = Invoice(
        order=order,
        event=order.event,
        organizer=order.event.organizer,
        date=timezone.now().astimezone(order.event.timezone).date(),
    )
    invoice.event.settings["invoice_address_from"] = "Via Roma 11"
    invoice.event.settings["invoice_address_from_name"] = "Python Italia APS"
    invoice.event.settings["invoice_address_from_zipcode"] = "123456"
    invoice.event.settings["invoice_address_from_city"] = "Firenze"
    invoice.event.settings["invoice_address_from_country"] = str(Country("IT"))
    invoice.event.settings["invoice_address_from_vat_id"] = "02053290630"
    invoice.save()
    invoice = build_invoice(invoice)
    if order.status == Order.STATUS_CANCELED:
        generate_cancellation(invoice, False)

    return invoice
