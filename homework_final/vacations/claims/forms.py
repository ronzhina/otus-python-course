from claims.models import Claim
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button, Field
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput


class ClaimCreateForm(ModelForm):
    class Meta:
        model = Claim
        fields = '__all__'
        exclude = ('employee',)
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(ClaimCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('type', css_class='col-md-8 mb-0'),
            Row(
                Column('start_date', css_class='form-group col-md-4 mb-0'),
                Column('end_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Field('is_pay_now', css_class='col-md-8 mb-0'),
            Field('agreed_with', css_class='col-md-8 mb-0'),
            Field('comment', css_class='col-md-8 mb-0', rows='2'),
            Field('status', css_class='col-md-8 mb-0', disabled=True, value="OA"),
            FormActions(
                Submit('save', 'Отправить'),
                Button('cancel', 'Отменить', onclick="javascript:history.back();")
            )
        )

    def clean(self):
        cleaned_data = super(ClaimCreateForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise ValidationError("Дата окончания должна быть позже даты начала отпуска")
        return cleaned_data

    def save(self, commit=True):
        self.instance.employee = self._user
        return super().save(commit)


class ClaimUpdateForm(ModelForm):
    class Meta:
        model = Claim
        fields = '__all__'
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('employee', css_class='col-md-8 mb-0', disabled=True),
            Field('type', css_class='col-md-8 mb-0'),
            Row(
                Column('start_date', css_class='form-group col-md-4 mb-0'),
                Column('end_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Field('is_pay_now', css_class='col-md-8 mb-0'),
            Field('agreed_with', css_class='col-md-8 mb-0'),
            Field('comment', css_class='col-md-8 mb-0', rows='2'),
            Field('status', css_class='col-md-8 mb-0', disabled=True),
            FormActions(
                Submit('save', 'Сохранить'),
                Button('cancel', 'Отменить', onclick="javascript:history.back();")
            )
        )
