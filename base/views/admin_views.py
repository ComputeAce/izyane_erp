from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from base.models import SalaryAdvance, LeaveApplication
from notification.views import VetSalaryAdvanceNotification, VetLeaveNotification
from django.contrib import messages

@login_required(login_url='frontend:login')
def vett_salary_advc_request(request, id):
    action = request.GET.get('status')

    if action not in ['Approved', 'Rejected']:  
        messages.warning(request, "Invalid action.")
        return redirect('frontend:salary_advance')

    salary_adv = get_object_or_404(SalaryAdvance, id=id)
    salary_adv.approval_status = action
    salary_adv.save()

    vett_salary_advc =  VetSalaryAdvanceNotification(id, action)
    vett_salary_advc.send_mail_application()
    messages.success(request, f"Salary advance Application has been {action.lower()}.")
    return redirect('frontend:salary_advance')


@login_required(login_url='frontend:login')
def vett_leave_request(request, id):
    status = request.GET.get('status') 
    
    if status not in ['Approved', 'Rejected']:  
        messages.warning(request, "Invalid action.")
        return redirect('frontend:leaves')

    leave_req = get_object_or_404(LeaveApplication, id=id)
    leave_req.status = status
    leave_req.save() 
    leave_obj = VetLeaveNotification(id, action=status)
    leave_obj.send_mail_application()
    messages.success(request, f"Leave request {status.lower()} successfully.")
    return redirect('frontend:leaves')

