from django.contrib import admin

from .models import Claim, Employee, Department, Position

admin.site.register(Claim)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)
