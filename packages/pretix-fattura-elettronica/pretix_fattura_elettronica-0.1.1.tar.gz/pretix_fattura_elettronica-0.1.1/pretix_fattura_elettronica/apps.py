from __future__ import annotations

from importlib.metadata import version

from django.utils.translation import gettext_lazy

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
        author = "Python Italia"
        description = gettext_lazy("Plugin for Italian Electronic Invoices")
        visible = True
        version = version("pretix-fattura-elettronica")
        category = "INTEGRATION"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA
