from __future__ import annotations

import datetime
from decimal import Decimal
from unittest import mock

from pretix_fattura_elettronica.enums import SETTINGS
from pretix_fattura_elettronica.models import DestinatarioFatturaElettronica

import pytest
from django_countries.fields import Country
from django_scopes import scopes_disabled
from pretix.base.models import (
    Event,
    InvoiceAddress,
    Order,
    OrderFee,
    OrderPosition,
    Organizer,
)

from .utils import generate_invoice


@pytest.fixture(autouse=True)
def disable_scopes():
    with scopes_disabled() as sd:
        yield sd


@pytest.fixture
@scopes_disabled()
def organizer():
    return Organizer.objects.create(name="Dummy", slug="dummy")


@pytest.fixture
@scopes_disabled()
def meta_prop(organizer):
    return organizer.meta_properties.create(name="type", default="Concert")


@pytest.fixture
@scopes_disabled()
def event(organizer, meta_prop):
    e = Event.objects.create(
        organizer=organizer,
        name="Dummy",
        slug="dummy",
        date_from=datetime.datetime(
            2017, 12, 27, 10, 0, 0, tzinfo=datetime.timezone.utc
        ),
        plugins="pretix.plugins.banktransfer,pretix.plugins.ticketoutputpdf",
        is_public=True,
    )
    e.meta_values.create(property=meta_prop, value="Conference")
    e.item_meta_properties.create(name="day", default="Monday")
    e.settings.timezone = "Europe/Berlin"
    return e


@pytest.fixture
@scopes_disabled()
def event2(organizer, meta_prop):
    e = Event.objects.create(
        organizer=organizer,
        name="Dummy2",
        slug="dummy2",
        date_from=datetime.datetime(
            2017, 12, 27, 10, 0, 0, tzinfo=datetime.timezone.utc
        ),
        plugins="pretix.plugins.banktransfer,pretix.plugins.ticketoutputpdf",
    )
    e.meta_values.create(property=meta_prop, value="Conference")
    return e


@pytest.fixture
def item(event):
    tax_rule = event.tax_rules.create(rate=Decimal("22.00"))
    return event.items.create(name="Budget Ticket", default_price=23, tax_rule=tax_rule)


@pytest.fixture
def item2(event2):
    tax_rule = event2.tax_rules.create(rate=Decimal("22.00"))
    return event2.items.create(
        name="Budget Ticket", default_price=23, tax_rule=tax_rule
    )


@pytest.fixture
def taxrule(event):
    return event.tax_rules.create(rate=Decimal("19.00"))


@pytest.fixture
def question(event, item):
    q = event.questions.create(question="T-Shirt size", type="S", identifier="ABC")
    q.items.add(item)
    q.options.create(answer="XL", identifier="LVETRWVU")
    return q


@pytest.fixture
def question2(event2, item2):
    q = event2.questions.create(question="T-Shirt size", type="S", identifier="ABC")
    q.items.add(item2)
    return q


@pytest.fixture
def quota(event, item):
    q = event.quotas.create(name="Budget Quota", size=200)
    q.items.add(item)
    return q


def _build_order(item, event, testtime, question, taxrule, is_business):
    o = Order.objects.create(
        code="FOO",
        event=event,
        email="dummy@dummy.test",
        status=Order.STATUS_PENDING,
        secret="k24fiuwvu8kxz3y1",
        datetime=datetime.datetime(2017, 12, 1, 10, 0, 0, tzinfo=datetime.timezone.utc),
        expires=datetime.datetime(2017, 12, 10, 10, 0, 0, tzinfo=datetime.timezone.utc),
        total=23,
        locale="en",
    )
    codice_destinatario = (
        "1234567" if is_business else SETTINGS.CODICE_DESTINATARIO_DEFAULT
    )
    pec_address = None if is_business else "ciccio@gmail.com"
    DestinatarioFatturaElettronica.objects.create(
        order=o, codice_destinatario=codice_destinatario, pec_address=pec_address
    )
    p1 = o.payments.create(
        provider="stripe",
        state="refunded",
        amount=Decimal("23.00"),
        payment_date=testtime,
    )
    o.refunds.create(
        provider="stripe",
        state="done",
        source="admin",
        amount=Decimal("23.00"),
        execution_date=testtime,
        payment=p1,
    )
    o.payments.create(
        provider="banktransfer",
        state="pending",
        amount=Decimal("23.00"),
    )
    o.fees.create(
        fee_type=OrderFee.FEE_TYPE_PAYMENT,
        value=Decimal("0.25"),
        tax_rate=Decimal("19.00"),
        tax_value=Decimal("0.05"),
        tax_rule=taxrule,
    )
    o.fees.create(
        fee_type=OrderFee.FEE_TYPE_PAYMENT,
        value=Decimal("0.25"),
        tax_rate=Decimal("19.00"),
        tax_value=Decimal("0.05"),
        tax_rule=taxrule,
        canceled=True,
    )
    InvoiceAddress.objects.create(
        order=o,
        company="Sample company" if is_business else "",
        name_parts={}
        if is_business
        else {
            "_scheme": "given_family",
            "given_name": "John",
            "family_name": "Doe",
        },
        country=Country("IT"),
        city="Napoli",  # mandatory
        zipcode="01020",  # mandatory
        vat_id="DE123" if is_business else "",
        vat_id_validated=True,
        is_business=is_business,
        internal_reference="" if is_business else "COD_FISCALE",
    )
    op = OrderPosition.objects.create(
        order=o,
        item=item,
        variation=None,
        price=Decimal("23"),
        attendee_name_parts={"full_name": "Peter", "_scheme": "full"},
        secret="z3fsn8jyufm5kpk768q69gkbyr5f4h6w",
        pseudonymization_id="ABCDEFGHKL",
        positionid=1,
    )
    OrderPosition.objects.create(
        order=o,
        item=item,
        variation=None,
        price=Decimal("23"),
        attendee_name_parts={"full_name": "Peter", "_scheme": "full"},
        secret="YBiYJrmF5ufiTLdV1iDf",
        pseudonymization_id="JKLM",
        canceled=True,
        positionid=2,
    )
    op.answers.create(question=question, answer="S")
    return o


@pytest.fixture
def private_order(event, item, taxrule, question):
    testtime = datetime.datetime(2017, 12, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
    event.plugins += ",pretix.plugins.stripe"
    event.save()

    with mock.patch("django.utils.timezone.now") as mock_now:
        mock_now.return_value = testtime
        return _build_order(item, event, testtime, question, taxrule, is_business=False)


@pytest.fixture
def business_order(event2, item2, taxrule, question):
    testtime = datetime.datetime(2017, 12, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)

    with mock.patch("django.utils.timezone.now") as mock_now:
        mock_now.return_value = testtime
        return _build_order(
            item2, event2, testtime, question, taxrule, is_business=True
        )


@pytest.fixture
def invoice(private_order):
    testtime = datetime.datetime(2017, 12, 10, 10, 0, 0, tzinfo=datetime.timezone.utc)

    with mock.patch("django.utils.timezone.now") as mock_now:
        mock_now.return_value = testtime
        return generate_invoice(private_order)


@pytest.fixture
def invoice2(private_order):
    testtime = datetime.datetime(2017, 12, 10, 10, 0, 0, tzinfo=datetime.timezone.utc)

    with mock.patch("django.utils.timezone.now") as mock_now:
        mock_now.return_value = testtime
        return generate_invoice(private_order)


@pytest.fixture
def invoice3(business_order):
    testtime = datetime.datetime(2017, 12, 10, 10, 0, 0, tzinfo=datetime.timezone.utc)

    with mock.patch("django.utils.timezone.now") as mock_now:
        mock_now.return_value = testtime
        return generate_invoice(business_order)
