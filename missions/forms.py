from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button, HTML, Row, Column, Field
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import MissionSubmission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = MissionSubmission
        fields = ["name", "email", "description", "attachment"]

    def clean(self):
        data = self.cleaned_data
        if not data.get("description") and not data.get("attachment"):
            raise ValidationError(_("You must fill in either the description or send an attachment"))
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-submissions-form'
        self.helper.form_class = 'form-submission'
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            FloatingField('name', required="true", wrapper_class="required"),
            FloatingField('email', required="true", wrapper_class="required"),
            FloatingField('description', css_class="rows-3"),
            Row(
                Column(
                    Field('attachment', template="file_input.html"),
                    css_class="col-sm-10 col-xs-12"
                ),
                Column(
                    FormActions(
                        Submit('send', _("Send")),
                        css_class="float-end"
                    ),
                    css_class="col-sm-2 col-xs-12",
                )
            ),

        )