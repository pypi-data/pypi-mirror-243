from __future__ import annotations

import datetime
from decimal import Decimal
from unittest import mock

from pretix_fattura_elettronica.enums import DOC_TYPE as DT
from pretix_fattura_elettronica.enums import SETTINGS
from pretix_fattura_elettronica.models import DestinatarioFatturaElettronica
from pretix_fattura_elettronica.serializers import InvoiceSerializer, OrderSerializer

from django.db.models import Count

import pytest
from django_countries.fields import Country
from pretix.base.models import InvoiceAddress, Order, OrderFee, OrderPosition

from .utils import generate_invoice


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
        country=Country("NZ"),
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


@pytest.mark.django_db
class TestOrderSerializer:
    def test_serialize_business_order(self, business_order, invoice3):
        ser_invoices = [
            invoice.model_dump(exclude_none=True)
            for invoice in OrderSerializer.serialize_invoices(business_order)
        ]
        assert ser_invoices == [
            {
                "fattura_elettronica_header": {
                    "dati_trasmissione": {
                        "id_trasmittente": {
                            "id_paese": "IT",
                            "id_codice": "02053290630",
                        },
                        "codice_destinatario": "1234567",
                    },
                    "cedente_prestatore": {
                        "dati_anagrafici": {
                            "id_fiscale_iva": {
                                "id_paese": "IT",
                                "id_codice": "02053290630",
                            },
                            "anagrafica": {"denominazione": "Python Italia APS"},
                            "regime_fiscale": SETTINGS.REGIME_FISCALE,
                            "codice_fiscale": SETTINGS.CF,
                        },
                        "sede": {
                            "indirizzo": "Via Roma 11",
                            "cap": "123456",
                            "comune": "Firenze",
                            "nazione": "Italy",
                        },
                        "contatti": {"email": SETTINGS.EMAIL},
                    },
                    "cessionario_committente": {
                        "dati_anagrafici": {
                            "id_fiscale_iva": {"id_paese": "NZ", "id_codice": "DE123"},
                            "anagrafica": {"denominazione": "Sample company"},
                        },
                        "sede": {
                            "indirizzo": "Sample company\nNew Zealand\nVAT-ID: DE123",
                            "cap": "",
                            "comune": "",
                            "nazione": "New Zealand",
                        },
                    },
                },
                "fattura_elettronica_body": [
                    {
                        "dati_generali": {
                            "dati_generali_documento": {
                                "tipo_documento": DT.TD01,
                                "divisa": "EUR",
                                "data": datetime.datetime(2017, 12, 10, 0, 0),
                                "numero": "DUMMY2-00001",
                            }
                        },
                        "dati_beni_servizi": {
                            "dettaglio_linee": [
                                {
                                    "numero_linea": 0,
                                    "descrizione": "Budget Ticket<br />Attendee: Peter",
                                    "prezzo_unitario": "18.85",
                                    "prezzo_totale": "23.00",
                                    "aliquota_iva": "22.00",
                                },
                                {
                                    "numero_linea": 1,
                                    "descrizione": "Payment fee",
                                    "prezzo_unitario": "0.20",
                                    "prezzo_totale": "0.25",
                                    "aliquota_iva": "19.00",
                                },
                            ],
                            "dati_riepilogo": [
                                {
                                    "aliquota_iva": "19.00",
                                    "imponibile_importo": "0.25",
                                    "imposta": "0.05",
                                },
                                {
                                    "aliquota_iva": "22.00",
                                    "imponibile_importo": "23.00",
                                    "imposta": "4.15",
                                },
                            ],
                        },
                    }
                ],
            }
        ]

    def test_serialize_private_order(self, private_order, invoice, invoice2):
        ser_invoices = [
            invoice.model_dump(exclude_none=True)
            for invoice in OrderSerializer.serialize_invoices(private_order)
        ]
        assert ser_invoices == [
            {
                "fattura_elettronica_header": {
                    "dati_trasmissione": {
                        "id_trasmittente": {
                            "id_paese": "IT",
                            "id_codice": "02053290630",
                        },
                        "codice_destinatario": SETTINGS.CODICE_DESTINATARIO_DEFAULT,
                        "pec_destinatario": "ciccio@gmail.com",
                    },
                    "cedente_prestatore": {
                        "dati_anagrafici": {
                            "id_fiscale_iva": {
                                "id_paese": "IT",
                                "id_codice": "02053290630",
                            },
                            "anagrafica": {"denominazione": "Python Italia APS"},
                            "regime_fiscale": SETTINGS.REGIME_FISCALE,
                            "codice_fiscale": SETTINGS.CF,
                        },
                        "sede": {
                            "indirizzo": "Via Roma 11",
                            "cap": "123456",
                            "comune": "Firenze",
                            "nazione": "Italy",
                        },
                        "contatti": {"email": SETTINGS.EMAIL},
                    },
                    "cessionario_committente": {
                        "dati_anagrafici": {
                            "codice_fiscale": "COD_FISCALE",
                            "anagrafica": {"nome": "John", "cognome": "Doe"},
                        },
                        "sede": {
                            "indirizzo": "John Doe\nNew Zealand",
                            "cap": "",
                            "comune": "",
                            "nazione": "New Zealand",
                        },
                    },
                },
                "fattura_elettronica_body": [
                    {
                        "dati_generali": {
                            "dati_generali_documento": {
                                "tipo_documento": DT.TD01,
                                "divisa": "EUR",
                                "data": datetime.datetime(2017, 12, 10, 0, 0),
                                "numero": "DUMMY-00001",
                            }
                        },
                        "dati_beni_servizi": {
                            "dettaglio_linee": [
                                {
                                    "numero_linea": 0,
                                    "descrizione": "Budget Ticket<br />Attendee: Peter",
                                    "prezzo_unitario": "18.85",
                                    "prezzo_totale": "23.00",
                                    "aliquota_iva": "22.00",
                                },
                                {
                                    "numero_linea": 1,
                                    "descrizione": "Payment fee",
                                    "prezzo_unitario": "0.20",
                                    "prezzo_totale": "0.25",
                                    "aliquota_iva": "19.00",
                                },
                            ],
                            "dati_riepilogo": [
                                {
                                    "aliquota_iva": "19.00",
                                    "imponibile_importo": "0.25",
                                    "imposta": "0.05",
                                },
                                {
                                    "aliquota_iva": "22.00",
                                    "imponibile_importo": "23.00",
                                    "imposta": "4.15",
                                },
                            ],
                        },
                    }
                ],
            },
            {
                "fattura_elettronica_header": {
                    "dati_trasmissione": {
                        "id_trasmittente": {
                            "id_paese": "IT",
                            "id_codice": "02053290630",
                        },
                        "codice_destinatario": SETTINGS.CODICE_DESTINATARIO_DEFAULT,
                        "pec_destinatario": "ciccio@gmail.com",
                    },
                    "cedente_prestatore": {
                        "dati_anagrafici": {
                            "id_fiscale_iva": {
                                "id_paese": "IT",
                                "id_codice": "02053290630",
                            },
                            "codice_fiscale": SETTINGS.CF,
                            "anagrafica": {"denominazione": "Python Italia APS"},
                            "regime_fiscale": SETTINGS.REGIME_FISCALE,
                        },
                        "sede": {
                            "indirizzo": "Via Roma 11",
                            "cap": "123456",
                            "comune": "Firenze",
                            "nazione": "Italy",
                        },
                        "contatti": {"email": SETTINGS.EMAIL},
                    },
                    "cessionario_committente": {
                        "dati_anagrafici": {
                            "codice_fiscale": "COD_FISCALE",
                            "anagrafica": {"nome": "John", "cognome": "Doe"},
                        },
                        "sede": {
                            "indirizzo": "John Doe\nNew Zealand",
                            "cap": "",
                            "comune": "",
                            "nazione": "New Zealand",
                        },
                    },
                },
                "fattura_elettronica_body": [
                    {
                        "dati_generali": {
                            "dati_generali_documento": {
                                "tipo_documento": DT.TD01,
                                "divisa": "EUR",
                                "data": datetime.datetime(2017, 12, 10, 0, 0),
                                "numero": "DUMMY-00002",
                            }
                        },
                        "dati_beni_servizi": {
                            "dettaglio_linee": [
                                {
                                    "numero_linea": 0,
                                    "descrizione": "Budget Ticket<br />Attendee: Peter",
                                    "prezzo_unitario": "18.85",
                                    "prezzo_totale": "23.00",
                                    "aliquota_iva": "22.00",
                                },
                                {
                                    "numero_linea": 1,
                                    "descrizione": "Payment fee",
                                    "prezzo_unitario": "0.20",
                                    "prezzo_totale": "0.25",
                                    "aliquota_iva": "19.00",
                                },
                            ],
                            "dati_riepilogo": [
                                {
                                    "aliquota_iva": "19.00",
                                    "imponibile_importo": "0.25",
                                    "imposta": "0.05",
                                },
                                {
                                    "aliquota_iva": "22.00",
                                    "imponibile_importo": "23.00",
                                    "imposta": "4.15",
                                },
                            ],
                        },
                    }
                ],
            },
        ]

    def test_retrieve_all_order_invoices(self, private_order):
        ser = OrderSerializer(private_order)

        for left, right in zip(ser._invoices, private_order.invoices.all()):
            assert left == right

    def test_wrong_private_customer_order_data(self, private_order, invoice, invoice2):
        private_order.invoice_address.internal_reference = None  # DELETING Cod Fiscale
        private_order.save()
        with pytest.raises(ValueError) as e:
            OrderSerializer.serialize_invoices(private_order)

        assert str(e.value) == "Codice fiscale is required."

    def test_wrong_business_customer_vat_id(self, business_order, invoice3):
        invoice3.invoice_to_vat_id = None  # DELETING vat id
        invoice3.save()
        with pytest.raises(ValueError) as e:
            OrderSerializer.serialize_invoices(business_order)

        assert str(e.value) == "For a business invoice VAT ID is required."

    def test_wrong_business_customer_recipient_codice_dest(
        self, business_order, invoice3
    ):
        invoice3.order.dest_fattura_elettronica_order.codice_destinatario = None
        invoice3.save()
        with pytest.raises(ValueError) as e:
            OrderSerializer.serialize_invoices(business_order)

        assert str(e.value) == "For a business invoice codice dest is required."

    @pytest.mark.parametrize(
        "company, name_parts, msg",
        (
            (
                None,
                {},
                "Necessaria denominazione oppure nome e cognome del destinatario.",
            ),
            (
                None,
                {"a": "b", "c": "e"},
                "Necessaria denominazione oppure nome e cognome del destinatario.",
            ),
            (
                None,
                {"_scheme": "given_family", "given_name": "John"},
                "In mancanza di Ragione Sociale, nome e cognome non possono esser",
            ),
            (
                None,
                {"_scheme": "given_family", "family_name": "John"},
                "In mancanza di Ragione Sociale, nome e cognome non possono esser",
            ),
        ),
    )
    def test_wrong_recipient_name_or_company_name(
        self, business_order, invoice3, company, name_parts, msg
    ):
        invoice3.invoice_to_company = company
        invoice3.order.invoice_address.name_parts = name_parts
        invoice3.save()
        with pytest.raises(ValueError) as e:
            OrderSerializer.serialize_invoices(business_order)

        assert msg in str(e.value)


@pytest.mark.django_db
class TestInvoiceSerializer:
    def test_invoice_body(self, invoice):
        ser = InvoiceSerializer(invoice)
        lines = invoice.lines.all()
        tax_summary = lines.values("tax_rate", "tax_value", "gross_value").annotate(
            count=Count("tax_rate")
        )

        assert ser._invoice_body.model_dump(exclude_none=True) == {
            "dati_generali": {
                "dati_generali_documento": {
                    "tipo_documento": DT.TD01,
                    "divisa": invoice.event.currency,
                    "data": datetime.datetime(2017, 12, 10, 0, 0),
                    "numero": invoice.number,
                }
            },
            "dati_beni_servizi": {
                "dettaglio_linee": [
                    {
                        "numero_linea": i,
                        "descrizione": line.description,
                        "prezzo_unitario": str(line.net_value),
                        "prezzo_totale": str(line.gross_value),
                        "aliquota_iva": str(line.tax_rate),
                    }
                    for i, line in enumerate(lines)
                ],
                "dati_riepilogo": [
                    {
                        "aliquota_iva": str(tax.get("tax_rate")),
                        "imponibile_importo": str(tax.get("gross_value")),
                        "imposta": str(tax.get("tax_value")),
                    }
                    for tax in tax_summary
                ],
            },
        }

    def test_invoice_header(self, invoice):
        ser = InvoiceSerializer(invoice)

        assert ser._invoice_header.model_dump(exclude_none=True) == {
            "dati_trasmissione": {
                "id_trasmittente": {
                    "id_paese": invoice.invoice_from_country.code,
                    "id_codice": invoice.invoice_from_vat_id,
                },
                "codice_destinatario": invoice.order.dest_fattura_elettronica_order.codice_destinatario,
                "pec_destinatario": invoice.order.dest_fattura_elettronica_order.pec_address,
            },
            "cedente_prestatore": {
                "dati_anagrafici": {
                    "id_fiscale_iva": {
                        "id_paese": invoice.invoice_from_country.code,
                        "id_codice": invoice.invoice_from_vat_id,
                    },
                    "anagrafica": {"denominazione": invoice.invoice_from_name},
                    "regime_fiscale": SETTINGS.REGIME_FISCALE,
                    "codice_fiscale": SETTINGS.CF,
                },
                "sede": {
                    "indirizzo": invoice.invoice_from,
                    "cap": invoice.invoice_from_zipcode,
                    "comune": invoice.invoice_from_city,
                    "nazione": invoice.invoice_from_country.name,
                },
                "contatti": {"email": SETTINGS.EMAIL},
            },
            "cessionario_committente": {
                "dati_anagrafici": {
                    "codice_fiscale": "COD_FISCALE",
                    "anagrafica": {"nome": "John", "cognome": "Doe"},
                },
                "sede": {
                    "indirizzo": invoice.invoice_to,
                    "cap": invoice.invoice_to_zipcode,
                    "comune": invoice.invoice_to_city,
                    "nazione": invoice.invoice_to_country.name,
                },
            },
        }

    def test_complete_private_invoice(self, invoice):
        lines = invoice.lines.all()
        tax_summary = lines.values("tax_rate", "tax_value", "gross_value").annotate(
            count=Count("tax_rate")
        )

        assert InvoiceSerializer.serialize(invoice).model_dump(exclude_none=True) == {
            "fattura_elettronica_header": {
                "dati_trasmissione": {
                    "id_trasmittente": {
                        "id_paese": invoice.invoice_from_country.code,
                        "id_codice": invoice.invoice_from_vat_id,
                    },
                    "codice_destinatario": invoice.order.dest_fattura_elettronica_order.codice_destinatario,
                    "pec_destinatario": invoice.order.dest_fattura_elettronica_order.pec_address,
                },
                "cedente_prestatore": {
                    "dati_anagrafici": {
                        "id_fiscale_iva": {
                            "id_paese": invoice.invoice_from_country.code,
                            "id_codice": invoice.invoice_from_vat_id,
                        },
                        "anagrafica": {"denominazione": invoice.invoice_from_name},
                        "regime_fiscale": SETTINGS.REGIME_FISCALE,
                        "codice_fiscale": SETTINGS.CF,
                    },
                    "sede": {
                        "indirizzo": invoice.invoice_from,
                        "cap": invoice.invoice_from_zipcode,
                        "comune": invoice.invoice_from_city,
                        "nazione": invoice.invoice_from_country.name,
                    },
                    "contatti": {"email": SETTINGS.EMAIL},
                },
                "cessionario_committente": {
                    "dati_anagrafici": {
                        "codice_fiscale": "COD_FISCALE",
                        "anagrafica": {"nome": "John", "cognome": "Doe"},
                    },
                    "sede": {
                        "indirizzo": invoice.invoice_to,
                        "cap": invoice.invoice_to_zipcode,
                        "comune": invoice.invoice_to_city,
                        "nazione": invoice.invoice_to_country.name,
                    },
                },
            },
            "fattura_elettronica_body": [
                {
                    "dati_generali": {
                        "dati_generali_documento": {
                            "tipo_documento": DT.TD01,
                            "divisa": invoice.event.currency,
                            "data": datetime.datetime(2017, 12, 10, 0, 0),
                            "numero": invoice.number,
                        }
                    },
                    "dati_beni_servizi": {
                        "dettaglio_linee": [
                            {
                                "numero_linea": i,
                                "descrizione": line.description,
                                "prezzo_unitario": str(line.net_value),
                                "prezzo_totale": str(line.gross_value),
                                "aliquota_iva": str(line.tax_rate),
                            }
                            for i, line in enumerate(lines)
                        ],
                        "dati_riepilogo": [
                            {
                                "aliquota_iva": str(tax.get("tax_rate")),
                                "imponibile_importo": str(tax.get("gross_value")),
                                "imposta": str(tax.get("tax_value")),
                            }
                            for tax in tax_summary
                        ],
                    },
                }
            ],
        }

    def test_complete_business_invoice(self, invoice3):
        invoice = invoice3
        lines = invoice.lines.all()
        tax_summary = lines.values("tax_rate", "tax_value", "gross_value").annotate(
            count=Count("tax_rate")
        )

        assert InvoiceSerializer.serialize(invoice).model_dump(exclude_none=True) == {
            "fattura_elettronica_header": {
                "dati_trasmissione": {
                    "id_trasmittente": {
                        "id_paese": invoice.invoice_from_country.code,
                        "id_codice": invoice.invoice_from_vat_id,
                    },
                    "codice_destinatario": invoice.order.dest_fattura_elettronica_order.codice_destinatario,
                },
                "cedente_prestatore": {
                    "dati_anagrafici": {
                        "id_fiscale_iva": {
                            "id_paese": invoice.invoice_from_country.code,
                            "id_codice": invoice.invoice_from_vat_id,
                        },
                        "anagrafica": {"denominazione": invoice.invoice_from_name},
                        "regime_fiscale": SETTINGS.REGIME_FISCALE,
                        "codice_fiscale": SETTINGS.CF,
                    },
                    "sede": {
                        "indirizzo": invoice.invoice_from,
                        "cap": invoice.invoice_from_zipcode,
                        "comune": invoice.invoice_from_city,
                        "nazione": invoice.invoice_from_country.name,
                    },
                    "contatti": {"email": SETTINGS.EMAIL},
                },
                "cessionario_committente": {
                    "dati_anagrafici": {
                        "id_fiscale_iva": {
                            "id_codice": invoice.invoice_to_vat_id,
                            "id_paese": invoice.invoice_to_country.code,
                        },
                        "anagrafica": {"denominazione": invoice.invoice_to_company},
                    },
                    "sede": {
                        "indirizzo": invoice.invoice_to,
                        "cap": invoice.invoice_to_zipcode,
                        "comune": invoice.invoice_to_city,
                        "nazione": invoice.invoice_to_country.name,
                    },
                },
            },
            "fattura_elettronica_body": [
                {
                    "dati_generali": {
                        "dati_generali_documento": {
                            "tipo_documento": DT.TD01,
                            "divisa": invoice.event.currency,
                            "data": datetime.datetime(2017, 12, 10, 0, 0),
                            "numero": invoice.number,
                        }
                    },
                    "dati_beni_servizi": {
                        "dettaglio_linee": [
                            {
                                "numero_linea": i,
                                "descrizione": line.description,
                                "prezzo_unitario": str(line.net_value),
                                "prezzo_totale": str(line.gross_value),
                                "aliquota_iva": str(line.tax_rate),
                            }
                            for i, line in enumerate(lines)
                        ],
                        "dati_riepilogo": [
                            {
                                "aliquota_iva": str(tax.get("tax_rate")),
                                "imponibile_importo": str(tax.get("gross_value")),
                                "imposta": str(tax.get("tax_value")),
                            }
                            for tax in tax_summary
                        ],
                    },
                }
            ],
        }
