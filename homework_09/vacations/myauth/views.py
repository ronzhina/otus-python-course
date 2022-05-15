from django.shortcuts import render
from django.views.generic import CreateView

from .models import Employee

from .forms import EmployeeCreateForm


class EmployeeCreateView(CreateView):
    model = Employee
    success_url = '/'
    form_class = EmployeeCreateForm
