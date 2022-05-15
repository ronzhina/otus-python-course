from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Employee, Department, Position


class ClaimsAdmin(UserAdmin):
    pass


admin.site.register(Employee, ClaimsAdmin)
admin.site.register(Department)
admin.site.register(Position)
