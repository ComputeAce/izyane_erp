from django.contrib.auth.decorators import login_required
from base.models import LeaveApplication, SalaryAdvance
from django.shortcuts import render

@login_required(login_url='frontend:login')
def leave_request(request):
    employee = request.user.employee

    user_leaves = LeaveApplication.objects.filter(employee=employee)
    context = {
        'user_leaves': user_leaves
    }   
    return render(request, 'frontend/employee/leave-request.html', context)

@login_required(login_url='frontend:login')
def leave_commutation(request):
    return render(request, 'frontend/employee/leave-commutation.html')


@login_required(login_url='frontend:login') 
def salary_advance_request(request):
    employee = request.user.employee

    user_salary_advc = SalaryAdvance.objects.filter(employee=employee)
    context = {
        'user_salary_advc': user_salary_advc
    }
    return render(request, 'frontend/employee/salary-advance-request.html',  context)