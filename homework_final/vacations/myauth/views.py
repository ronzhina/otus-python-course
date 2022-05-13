from django.views.generic import CreateView

from .forms import EmployeeCreateForm
from .models import Employee


class EmployeeCreateView(CreateView):
    model = Employee
    success_url = '/'
    form_class = EmployeeCreateForm
