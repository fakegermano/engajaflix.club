from django import forms

class EmailReserveForm(forms.Form):
    email = forms.EmailField()
    social = forms.URLField()

class EmailUnreserveForm(forms.Form):
    confirm = forms.BooleanField()