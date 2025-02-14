from django.contrib import admin

from .models import LeaveApplication, LeaveCommutation, SalaryAdvance, Employee
# Register your models here.

admin.site.register(LeaveCommutation)
admin.site.register(LeaveApplication)
admin.site.register(SalaryAdvance)
admin.site.register(Employee)

