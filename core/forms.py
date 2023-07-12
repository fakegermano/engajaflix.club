from django import forms
from django.utils.translation import gettext as _

class EmailReserveForm(forms.Form):
    email = forms.EmailField(help_text=_("um email valido se parece com 'teste@exemplo.com'"), label=_("email"))
    social = forms.URLField(
        help_text=_("um link valido se parece com 'instagram.com/juliagtr'"), 
        label=_("link de sua rede social principal"),
    )

class EmailUnreserveForm(forms.Form):
    confirm = forms.BooleanField()