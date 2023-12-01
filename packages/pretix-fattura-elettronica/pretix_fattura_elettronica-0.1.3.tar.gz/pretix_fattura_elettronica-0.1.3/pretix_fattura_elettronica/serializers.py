from __future__ import annotations

from datetime import datetime

from django.db.models import Count

from pydantic import BaseModel, model_validator

from .enums import DOC_TYPE as DT
from .enums import SETTINGS


class DettaglioLinea(BaseModel):
    numero_linea: int
    descrizione: str
    quantita: str | None = None
    unita_misura: str | None = None
    prezzo_unitario: str
    prezzo_totale: str
    aliquota_iva: str
    ritenuta: str | None = None
    natura: str | None = None


class DatiRiepilogo(BaseModel):
    aliquota_iva: str
    imponibile_importo: str
    imposta: str


class DatiBeniServizi(BaseModel):
    dettaglio_linee: list[DettaglioLinea]
    dati_riepilogo: list[DatiRiepilogo]


class IdFiscaleIVA(BaseModel):
    id_paese: str
    id_codice: str


class Anagrafica(BaseModel):
    """Denominazione or Nome and Cognome should be filled"""

    denominazione: str | None = None
    nome: str | None = None
    cognome: str | None = None
    titolo: str | None = None
    cod_eori: str | None = None

    @model_validator(mode="after")
    def check_valid_data(self) -> Anagrafica:
        if self.denominazione is None:
            if self.cognome is None and self.nome is None:
                raise ValueError(
                    "Necessaria denominazione oppure nome e cognome del destinatario."
                )
            if self.cognome is None or self.nome is None:
                raise ValueError(
                    "In mancanza di Ragione Sociale, nome e cognome non possono essere vuoti."
                )
        return self


class DatiAnagraficiCedente(BaseModel):
    id_fiscale_iva: IdFiscaleIVA
    codice_fiscale: str | None = None
    anagrafica: Anagrafica
    regime_fiscale: str


class DatiAnagraficiCessionario(BaseModel):
    id_fiscale_iva: IdFiscaleIVA | None = None
    codice_fiscale: str | None = None
    anagrafica: Anagrafica


class Sede(BaseModel):
    indirizzo: str
    numero_civico: str | None = None
    cap: str
    comune: str
    provincia: str | None = None
    nazione: str


class Contatti(BaseModel):
    telefono: str | None = None
    fax: str | None = None
    email: str | None = None


class DatiTrasmissione(BaseModel):
    id_trasmittente: IdFiscaleIVA | None = None
    codice_destinatario: str
    pec_destinatario: str | None = None


class CedentePrestatore(BaseModel):
    dati_anagrafici: DatiAnagraficiCedente
    sede: Sede
    contatti: Contatti | None = None


class CessionarioCommittente(BaseModel):
    dati_anagrafici: DatiAnagraficiCessionario
    sede: Sede


class DatiGeneraliDocumento(BaseModel):
    tipo_documento: str
    divisa: str
    data: datetime
    numero: str


class DatiGenerali(BaseModel):
    dati_generali_documento: DatiGeneraliDocumento


class FatturaElettronicaBody(BaseModel):
    dati_generali: DatiGenerali
    dati_beni_servizi: DatiBeniServizi


class FatturaElettronicaHeader(BaseModel):
    dati_trasmissione: DatiTrasmissione
    cedente_prestatore: CedentePrestatore
    cessionario_committente: CessionarioCommittente


class FatturaElettronica(BaseModel):
    fattura_elettronica_header: FatturaElettronicaHeader
    fattura_elettronica_body: list[FatturaElettronicaBody]


class OrderSerializer:
    def __init__(self, order) -> None:
        self._order = order

    @classmethod
    def serialize_invoices(cls, order) -> list[FatturaElettronica]:
        return cls(order)._serialize_invoices()

    def _serialize_invoices(self) -> list[FatturaElettronica]:
        return [InvoiceSerializer.serialize(invoice) for invoice in self._invoices]

    @property
    def _invoices(self):
        return self._order.invoices.all()


class InvoiceSerializer:
    def __init__(self, invoice) -> None:
        self._invoice = invoice

    @classmethod
    def serialize(cls, invoice) -> FatturaElettronica:
        return cls(invoice)._serialize()

    def _serialize(self) -> FatturaElettronica:
        return FatturaElettronica(
            fattura_elettronica_header=self._invoice_header,
            fattura_elettronica_body=[self._invoice_body],
        )

    @property
    def _invoice_body(self) -> FatturaElettronicaBody:
        inv = self._invoice
        tipo_doc = DT.TD04 if inv.canceled and inv.is_cancellation else DT.TD01
        dati_generali = DatiGenerali(
            dati_generali_documento=DatiGeneraliDocumento(
                tipo_documento=tipo_doc,
                divisa=inv.event.currency,
                data=inv.date,
                numero=inv.number,
            )
        )
        lines = inv.lines.all()
        dettaglio_linee = [
            DettaglioLinea(
                numero_linea=i,
                descrizione=line.description,
                prezzo_unitario=str(line.net_value),
                prezzo_totale=str(line.gross_value),
                aliquota_iva=str(line.tax_rate),
            )
            for i, line in enumerate(lines)
        ]
        tax_summary = (
            inv.lines.all()
            .values("tax_rate", "tax_value", "gross_value")
            .annotate(count=Count("tax_rate"))
        )
        dati_riepilogo = [
            DatiRiepilogo(
                aliquota_iva=str(tax.get("tax_rate")),
                imponibile_importo=str(tax.get("gross_value")),
                imposta=str(tax.get("tax_value")),
            )
            for tax in tax_summary
        ]
        dati_beni_servizi = DatiBeniServizi(
            dettaglio_linee=dettaglio_linee, dati_riepilogo=dati_riepilogo
        )
        return FatturaElettronicaBody(
            dati_generali=dati_generali, dati_beni_servizi=dati_beni_servizi
        )

    @property
    def _invoice_header(self) -> FatturaElettronicaHeader:
        inv = self._invoice
        recipient_vat_id, recipient_cf = self._recipient_fiscal_data
        codice_dest, pec_dest = self._recipient_fe_data
        dati_trasmissione = DatiTrasmissione(
            id_trasmittente=IdFiscaleIVA(
                id_paese=inv.invoice_from_country.code,
                id_codice=inv.invoice_from_vat_id,
            ),
            codice_destinatario=codice_dest,
            pec_destinatario=pec_dest,
        )
        # Cedente Prestatore is who issue the invoice: e.g. Python Italia APS
        cedente_prestatore = CedentePrestatore(
            dati_anagrafici=DatiAnagraficiCedente(
                id_fiscale_iva=IdFiscaleIVA(
                    id_paese=inv.invoice_from_country.code,
                    id_codice=inv.invoice_from_vat_id,
                ),
                codice_fiscale=SETTINGS.CF,
                anagrafica=Anagrafica(denominazione=inv.invoice_from_name),
                regime_fiscale=SETTINGS.REGIME_FISCALE,
            ),
            sede=Sede(
                indirizzo=inv.invoice_from,
                numero_civico=None,
                cap=inv.invoice_from_zipcode,
                comune=inv.invoice_from_city,
                provincia=None,
                nazione=inv.invoice_from_country.name,
            ),
            contatti=Contatti(email=SETTINGS.EMAIL),
        )
        cessionario_committente = CessionarioCommittente(
            dati_anagrafici=DatiAnagraficiCessionario(
                id_fiscale_iva=IdFiscaleIVA(
                    id_paese=inv.invoice_to_country.code,
                    id_codice=recipient_vat_id,
                )
                if recipient_vat_id
                else None,
                codice_fiscale=recipient_cf,
                anagrafica=self._recipient_anagrafical_data,
            ),
            sede=Sede(
                indirizzo=inv.invoice_to,
                numero_civico=None,
                cap=inv.invoice_to_zipcode,
                comune=inv.invoice_to_city,
                provincia=None,
                nazione=inv.invoice_to_country.name,
            ),
        )
        return FatturaElettronicaHeader(
            dati_trasmissione=dati_trasmissione,
            cedente_prestatore=cedente_prestatore,
            cessionario_committente=cessionario_committente,
        )

    @property
    def _recipient_anagrafical_data(self) -> Anagrafica:
        inv = self._invoice
        complete_name = inv.order.invoice_address.name
        family_name = complete_name.rsplit(" ", 1)[-1] if complete_name else None
        name = (
            complete_name.rsplit(" ", 1)[0]
            if complete_name and " " in complete_name
            else None
        )
        return Anagrafica(
            denominazione=inv.invoice_to_company or None,
            nome=name,
            cognome=family_name,
        )

    @property
    def _recipient_fe_data(self) -> tuple[str, str]:
        inv = self._invoice
        is_business = inv.order.invoice_address.is_business
        if is_business:
            codice_destinatario = (
                inv.order.dest_fattura_elettronica_order.codice_destinatario
            )
            pec_destinatario = (
                inv.order.dest_fattura_elettronica_order.pec_address or None
            )
            if not codice_destinatario:
                raise ValueError("For a business invoice codice dest is required.")
        else:
            codice_destinatario = SETTINGS.CODICE_DESTINATARIO_DEFAULT
            pec_destinatario = (
                inv.order.dest_fattura_elettronica_order.pec_address or None
            )
        return codice_destinatario, pec_destinatario

    @property
    def _recipient_fiscal_data(self) -> tuple[str, str]:
        inv = self._invoice
        is_business = inv.order.invoice_address.is_business
        if is_business:
            codice_fiscale = inv.internal_reference or None
            vat_id = inv.invoice_to_vat_id
            if not vat_id:
                raise ValueError("For a business invoice VAT ID is required.")
        else:
            codice_fiscale = inv.order.invoice_address.internal_reference
            vat_id = None
            if not codice_fiscale:
                raise ValueError("Codice fiscale is required.")
        return vat_id, codice_fiscale
