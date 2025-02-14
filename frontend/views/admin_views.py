from django.shortcuts import render
from base.models import Employee, SalaryAdvance, LeaveApplication


def users(request):
    users = Employee.objects.all().exclude(role = "Employee")
    
    context = {
        'users': users
    }
    return render(request, 'frontend/admin/users.html', context)


def roles(request):
    return render(request, 'frontend/admin/roles.html')


def salary_advance(request):
    advances = SalaryAdvance.objects.all()

    context = {
        'advances': advances
    }
    return render(request, 'frontend/hrm/salary_advance.html', context)

def leaves(request):
    leaves = LeaveApplication.objects.all()

    context = {
        'leaves': leaves
    }
    return render(request, 'frontend/hrm/leaves.html', context)
