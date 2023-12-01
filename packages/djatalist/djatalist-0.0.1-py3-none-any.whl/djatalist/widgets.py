from django.http import QueryDict
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class DatalistSelect(forms.Widget):
    def __init__(self, choices, attrs=None):
        self.choices = choices
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        for choice in self.choices:
            if value == choice[0]:
                value = f"{choice[1]} # {value}"
                break
        final_attrs = self.build_attrs(self.attrs, extra_attrs={"name": name})
        output = [
            forms.widgets.TextInput(
                attrs={
                    "list": f"id_{final_attrs['name']}_datalist",
                    "autocomplete": "off",
                }
            ).render(name, value, final_attrs, renderer)
        ]
        output.append(f'<datalist id="id_{final_attrs["name"]}_datalist">')

        for option_value, option_label in self.choices:
            output.append(f'<option value="{option_label} # {option_value}"></option>')

        output.append("</datalist>")
        return mark_safe("\n".join(output))

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if value:
            value = value.split(" # ")[-1]
        return value


class DatalistMultiple(forms.Widget):
    def __init__(self, attrs=None):
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        final_attrs = self.build_attrs(self.attrs, extra_attrs={"name": name, "id": f"id_{name}_input"})
        text_input = forms.widgets.TextInput(
            attrs={
                "list": f"id_{final_attrs['name']}_datalist",
                "autocomplete": "off",
            }
        ).render(None, None, final_attrs, renderer)

        datalist = [f'<datalist id="id_{final_attrs["name"]}_datalist">']

        for option_value, option_label in self.choices:
            datalist.append(f'<option value="{option_label} # {option_value}"></option>')

        datalist.append("</datalist>")
        context = {'text_input': text_input, 'datalist': mark_safe('\n'.join(datalist)), 'name': name, 'value': value}
        
        output = render_to_string('multiple.html', context)
        return mark_safe(output)

    def value_from_datadict(self, data: QueryDict, files, name):
        return [value.split(' # ')[-1] for value in data.getlist(name, None)]
