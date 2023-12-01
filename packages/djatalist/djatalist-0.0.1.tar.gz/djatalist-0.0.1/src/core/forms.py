from django import forms

from djatalist import widgets

CHOICES = [
    (1, "One"),
    (2, "Two"),
    (3, "Three"),
    (4, "Four"),
    (5, "Five"),
]

class DemoWidgetsForm(forms.Form):
    select_single_example = forms.CharField(
        required=False,
        widget=widgets.DatalistSelect(
            choices=[
                ("1", "One"),
                ("2", "Two"),
                ("3", "Three"),
                ("4", "Four"),
                ("5", "Five"),
            ]
        )
    )

    select_multiple_example = forms.MultipleChoiceField(
        required=False,
        choices=CHOICES,
        widget=widgets.DatalistMultiple()
    )
