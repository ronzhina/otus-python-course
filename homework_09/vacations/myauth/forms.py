from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, Button
from django.contrib.auth.forms import UserCreationForm
from myauth.models import Employee


class EmployeeCreateForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('username', 'email', 'name', 'surname', 'patronymic',
                  'department', 'position', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Field('surname', css_class='col-md-8 mb-0'),
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('patronymic', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Field('department', css_class='col-md-8 mb-0'),
            Field('position', css_class='col-md-8 mb-0'),
            Field('password1', css_class='col-md-8 mb-0'),
            Field('password2', css_class='col-md-8 mb-0'),

            FormActions(
                Submit('save', 'Создать'),
                Button('cancel', 'Отменить', onclick="javascript:history.back();")
            )
        )
