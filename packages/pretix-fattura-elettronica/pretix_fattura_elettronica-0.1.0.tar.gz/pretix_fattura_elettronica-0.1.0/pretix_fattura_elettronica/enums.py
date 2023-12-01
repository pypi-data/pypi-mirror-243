from __future__ import annotations

from enum import StrEnum


class SETTINGS(StrEnum):
    # TODO: replace this with a new model and an admin view
    # https://docs.pretix.eu/en/latest/development/implementation/settings.html
    CODICE_DESTINATARIO_DEFAULT = "0000000"
    CF = "94144670489"
    REGIME_FISCALE = "RF1"
    EMAIL = "info@python.it"


class DOC_TYPE(StrEnum):
    """Enum repr for the invoice type.

    Can be one of TD01 fattura TD02 acconto/anticipo su fattura TD03 acconto/anticipo
    su parcella TD04 nota di credito TD05 nota di debito TD06 parcella TD16
    integrazione fattura reverse charge interno TD17 integrazione/autofattura per
    acquisto servizi dall'estero TD18 integrazione per acquisto di beni intracomunitari
    TD19 integrazione/autofattura per acquisto di beni ex art.17 c.2 DPR 633/72
    TD20 autofattura per regolarizzazione e integrazione delle fatture
    (ex art.6 c.8 d.lgs. 471/97 o art.46 c.5 D.L. 331/93) TD21 autofattura
    per splafonamento TD22 estrazione beni da Deposito IVA TD23 estrazione
    beni da Deposito IVA con versamento dell'IVA TD24 fattura differita di cui
    all'art. 21, comma 4, lett. a) TD25 fattura differita di cui all'art. 21,
    comma 4, terzo periodo lett. b) TD26 cessione di beni ammortizzabili e per
    passaggi interni (ex art.36 DPR 633/72) TD27 fattura per autoconsumo o per
    cessioni gratuite senza rivalsa TD28 acquisti da San Marino con
    IVA (fattura cartacea)
    """

    TD01 = "TD01"
    TD02 = "TD02"
    TD03 = "TD03"
    TD04 = "TD04"
    TD05 = "TD05"
    TD06 = "TD06"
    TD17 = "TD17"
    TD18 = "TD18"
    TD19 = "TD19"
    TD20 = "TD20"
    TD21 = "TD21"
    TD22 = "TD22"
    TD23 = "TD23"
    TD24 = "TD24"
    TD25 = "TD25"
    TD26 = "TD26"
    TD27 = "TD27"
    TD28 = "TD28"
