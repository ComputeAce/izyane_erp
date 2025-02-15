from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from base.models import LeaveApplication, SalaryAdvance, Employee
from django.shortcuts import render



@login_required(login_url='frontend:login')
def home(request):

    return render(request, 'frontend/base/home.html')


@login_required(login_url='frontend:login')
def profile(request, id):
    get_employee = Employee.objects.get(id = id)
    get_emp_leaves = LeaveApplication.objects.filter(employee = get_employee)
    get_emp_sal_advcs = SalaryAdvance.objects.filter(employee = get_employee)

    print(get_employee, get_emp_leaves, get_emp_sal_advcs)

    context = {
        'get_employee': get_employee,
        'get_emp_leaves': get_emp_leaves,
        'get_emp_sal_advcs': get_emp_sal_advcs,

    }
    return render(request, 'frontend/base/profile.html', context)



def login(request):
    return render(request, 'frontend/base/login.html')


@login_required(login_url='frontend:login')
def leave_view(request, id):
    user_leave = get_object_or_404(LeaveApplication, id=id)
    
    context = {
        'user_leave': user_leave
    }
    return render(request, 'frontend/base/leave-view.html', context)


@login_required(login_url='frontend:login')
def salary_advance_view(request, id):
    user_salary_advc = get_object_or_404(SalaryAdvance, id = id)

    context = {
        'user_salary_advc': user_salary_advc
    }
    return render(request, 'frontend/base/salary-advance-view.html', context)

@login_required(login_url='frontend:login')
def user_profile(request):
    user = request.user.id
    get_employee = Employee.objects.get(user_id = user)
    context = {
        'get_employee': get_employee
    }

    return render(request, 'frontend/base/user-profile.html', context)

def error_404(request, exception):
        data = {}
        return render(request,'base/error_404.html', data)

def error_500(request):
        data = {}
        return render(request,'base/error_500.html', data)