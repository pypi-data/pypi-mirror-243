import bleach
from django import forms


class TrixWidget(forms.Widget):

    template_name = "trix_widget.html"

    class Media:
        css = {
            "all": ["trix/trix.css"],
        }
        js = ["trix/trix.min.js"]

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return bleach.clean(value, tags={'strong', 'em', 'del', 'ul', 'li', 'br', 'a'}, strip=True)
