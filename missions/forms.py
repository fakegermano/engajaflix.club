from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button, HTML, Row, Column, Field
from crispy_forms.bootstrap import FormActions
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import MissionSubmission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = MissionSubmission
        fields = ["name", "email", "description", "attachment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-register-form'
        self.helper.form_class = 'form-register'
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.layout = Layout(
            FloatingField('name', required="true", wrapper_class="required"),
            FloatingField('email', required="true", wrapper_class="required"),
            FloatingField('description', css_class="rows-3"),
            Field('attachment', template="file_input.html"),
            FormActions(
                Submit('send', "Send"),
            )
        )