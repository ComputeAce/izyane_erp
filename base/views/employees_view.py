from django.contrib.auth.decorators import login_required
from notification.views import NewLeaveNotification, NewSalaryAdvcNotification
from base.models import LeaveApplication, SalaryAdvance, Employee
from django.shortcuts import redirect
from django.contrib import messages



@login_required(login_url='frontend:login')
def leave_request(request):
    if request.method == 'POST':
        user = request.user.employee
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        leave_type = request.POST.get('leave_type')
        employee = request.user.employee
        existing_leave = LeaveApplication.objects.filter(employee=employee, status='pending').first()

        if existing_leave:
            messages.warning(request, 'You already have a pending leave request. Please wait for it to be processed before submitting a new request.')
            return redirect('frontend:leave_request')

        leave = LeaveApplication(
            employee=employee, 
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            leave_type=leave_type
        )
        leave.save()

        get_leave = LeaveApplication.objects.get(status = 'pending', employee = employee)
        leave_id = get_leave.pk

        new_leave_obj = NewLeaveNotification(leave_id)
        new_leave_obj.send_mail_to_applicant()
        new_leave_obj.send_mail_to_manager()

        messages.info(request, 'Leave request submitted successfully.')
        return redirect('frontend:leave_request')
    

@login_required(login_url='frontend:login')
def salary_advance_request(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')

        employee = request.user.employee

        check = SalaryAdvance.objects.filter(employee = employee, approval_status = 'pending')
        print('Found')
        if check.exists:
            messages.warning(request, 'You already have a salary advance request. Please wait for it to be processed before submitting a new request.')
            return redirect('frontend:salary_advance_request')
        create = SalaryAdvance.objects.create(employee = employee, amount = amount, reason = reason)
        create.save()
        get_employee = SalaryAdvance.objects.filter(employee = employee, approval_status = 'pending')
        advc_id = get_employee.id
        salary_advc = NewSalaryAdvcNotification(advc_id)
        salary_advc.send_mail_to_applicant()
        salary_advc.send_mail_to_manager()
        messages.info(request,  'Salary Advance request submitted successfully.')
        return redirect('frontend:salary_advance_request')
    
    
    messages.info(request,  'Invalid Request.')
    return redirect('frontend:salary_advance_request')


@login_required(login_url='frontend:login')
def home_leave_request(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        leave_type = request.POST.get('leave_type')
        employee = request.user.employee
        existing_leave = LeaveApplication.objects.filter(employee=employee, status='pending').first()

        if existing_leave:
            messages.warning(request, 'You already have a pending leave request. Please wait for it to be processed before submitting a new request.')
            return redirect('frontend:home')

        leave = LeaveApplication(
            employee=employee, 
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            leave_type=leave_type
        )
        leave.save()

        messages.info(request, 'Leave request submitted successfully.')
        return redirect('frontend: home')
    

@login_required(login_url='frontend:login')
def home_salary_advance_request(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')

        employee = request.user.employee

        check = SalaryAdvance.objects.filter(employee = employee, approval_status = 'pending')
        if check.exists:
            messages.warning(request, 'You already have a salary advance request. Please wait for it to be processed before submitting a new request.')
            return redirect('frontend:home')
        create = SalaryAdvance.objects.create(employee = employee, amount = amount, reason = reason)
        create.save()
        
        messages.info(request,  'Salary Advance request submitted successfully.')
        return redirect('frontend:home')
    
    
    messages.info(request,  'Invalid Request.')
    return redirect('frontend: home')
    


