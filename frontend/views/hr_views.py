from django.shortcuts import render
from base.models import Employee, LeaveApplication, SalaryAdvance



def employees(request):

    get_employees = Employee.objects.all()

    print(get_employees)

    context = {
        'get_employees': get_employees
    }
    return render(request, 'frontend/hrm/employees.html', context)

def add_employee(request):
    return render(request, 'frontend/hrm/add_employee.html')


