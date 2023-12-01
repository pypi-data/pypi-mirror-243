from __future__ import annotations

from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_fattura_elettronica"
    verbose_name = "Fattura Elettronica"

    class PretixPluginMeta:
        name = gettext_lazy("Fattura Elettronica")
        author = "Patrick Arminio & Ernesto Arbitrio"
        description = gettext_lazy("Plugin for Italian Electronic Invoices")
        visible = True
        version = __version__
        category = "INTEGRATION"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA
