# django-trix-widget

Django form widget for [Trix](https://trix-editor.org/).

## Rationale

Integrate Trix editor with Django forms framework.

## Support

Supports: Python 3.10.

Supports Django Versions: 3.2

## Installation

```shell
$ pip install django-trix-widget
```

## Usage

Add `trix_widget` to `INSTALLED_APPS`.

Run migrations:

Import the widget from the package:

```python
from django import forms
from trix_widget.widgets import TrixWidget


class MyForm(forms.Form):
    
    text = forms.CharField(widget=TrixWidget())


```