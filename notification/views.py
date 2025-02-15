from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from base.models import (

    Employee,
    SalaryAdvance,
    LeaveApplication
    

) 


def send_mail_new_employee(email, username, password):
    try:
        get_user = Employee.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("User with the given email does not exist.")

    context = {
        'first_name': get_user.first_name,
        'last_name': get_user.last_name,
        'password': password,
        'email': email,
        'username': username,
        'year': datetime.now().year, 
    }

    receiver_email = email
    template_name = "notification/receiver_info.html"
    convert_to_html_content = render_to_string(
        template_name=template_name,
        context=context,
    )

    plain_message = strip_tags(convert_to_html_content)

    send_mail(
        subject="Welcome to izyane",
        message=plain_message,
        from_email="your_email@example.com",
        recipient_list=[receiver_email],
        html_message=convert_to_html_content,
        fail_silently=True,  
    )
    return HttpResponse("Email sent successfully.")


class VetLeaveNotification:
    def __init__(self, leave_id, action):
        self.leave_id = leave_id
        self.action = action
        if self.action == "Approved":
            self.message_body = "Your leave application has been granted. Enjoy your holiday!"
        else:
            self.message_body = "We regret to inform you that your leave application has been denied."

        self.applicant_email = None
        self.applicant_first_name = None
        self.applicant_last_name = None
        self.hr_email = None

        try:

            leave_obj = LeaveApplication.objects.get(id=self.leave_id)
            self.applicant_email = leave_obj.employee.email
            self.applicant_first_name = leave_obj.employee.first_name
            self.applicant_last_name = leave_obj.employee.last_name
        except ObjectDoesNotExist:
            raise ValueError("Invalid leave ID. Leave application not found.")
        self.validate_email(self.applicant_email)

    @staticmethod
    def validate_email(email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(f"Invalid email address: {email}")

    def send_mail_application(self):
        context = {
            "message": self.message_body,
            "first_name": self.applicant_first_name,
            "last_name": self.applicant_last_name,
        }

        receiver_email = self.applicant_email
        template_name = "notification/leave_application_info.html"

        
        convert_to_html_content = render_to_string(template_name=template_name, context=context)
        plain_message = strip_tags(convert_to_html_content)

        send_mail(
            subject="Your leave application",
            message=plain_message,
            from_email="your_email@example.com",
            recipient_list=[receiver_email],
            html_message=convert_to_html_content,
            fail_silently=False,  
        )
        return HttpResponse("Email sent successfully.")
    
class NewLeaveNotification:
    def __init__(self, leave_id):
        self.leave_id = leave_id

        try:
            leave = LeaveApplication.objects.get(id=self.leave_id)
            self.applicant_first_name = leave.employee.first_name
            self.applicant_last_name = leave.employee.last_name
            self.full_name = f"{self.applicant_first_name} {self.applicant_last_name}"
            self.applicant_email = leave.employee.email
        except LeaveApplication.DoesNotExist:
            raise ValueError("Invalid leave ID: Leave object does not exist")

        # Ensure HR/Admin Employee Exists
        admin = Employee.objects.filter(role="HR").first()
        if admin:
            self.first_name = admin.first_name
            self.last_name = admin.last_name
            self.email = admin.email
        else:
            self.first_name = "HR"
            self.last_name = "Department"
            self.email = "hr@example.com"  # Default email to avoid failures

        print(f'First Name: {self.first_name}, Last Name: {self.last_name}, Email: {self.email}')

    def send_email(self, receiver_email, context, subject):
        template_name = "notification/new_leave_application.html"
        convert_to_html_content = render_to_string(template_name, context)
        plain_message = strip_tags(convert_to_html_content)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email="your_email@example.com",  # Replace with actual sender email
            recipient_list=[receiver_email],
            html_message=convert_to_html_content,
            fail_silently=True,
        )

    def send_mail_to_applicant(self):
        context = {
            'first_name': self.applicant_first_name,
            'last_name': self.applicant_last_name,
            'message': 'Your leave application has been submitted and will be reviewed shortly.',
        }
        self.send_email(
            receiver_email=self.applicant_email,
            context=context,
            subject="Leave Application Submitted",
        )
        return HttpResponse("Email to applicant sent successfully.")

    def send_mail_to_manager(self):
        context = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'message': f'A new leave application has been submitted by {self.full_name}. Please review it promptly.',
        }
        self.send_email(
            receiver_email=self.email,
            context=context,
            subject="New Leave Application",
        )
        return HttpResponse("Email to manager sent successfully.")


class NewSalaryAdvcNotification:
    def __init__(self, advc_id):
        self.advc_id = advc_id
        try:
            advc = SalaryAdvance.objects.get(id=self.advc_id)
            self.applicant_first_name = advc.user.first_name
            self.applicant_last_name = advc.user.last_name
            self.full_name = self.applicant_first_name + " " + self.applicant_last_name
            self.applicant_email = advc.user.email
        except advc.DoesNotExist:
            raise ValueError("Invalid leave ID: Leave object does not exist")

        try:
            admin = Employee.objects.filter(department='HR').first()
            self.admin_first_name = admin.first_name
            self.admin_last_name = admin.last_name
            self.admin_email = admin.email
        except Employee.DoesNotExist:
            raise ValueError("No HR employee found")

    def send_email(self, receiver_email, context, subject):
        template_name = "notification/new_leave_application.html"
        convert_to_html_content = render_to_string(template_name, context)
        plain_message = strip_tags(convert_to_html_content)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email="your_email@example.com",
            recipient_list=[receiver_email],
            html_message=convert_to_html_content,
            fail_silently=True,
        )

    def send_mail_to_applicant(self):
        
        context = {
            'first_name': self.applicant_first_name,
            'last_name': self.applicant_last_name,
            'message': 'Your salary advance application has been submitted and will be reviewed shortly.',
        }
        self.send_email(
            receiver_email=self.applicant_email,
            context=context,
            subject="Leave Application Submitted",
        )
        return HttpResponse("Email to applicant sent successfully.")

    def send_mail_to_manager(self):
        
        context = {
            'first_name': self.admin_first_name,
            'last_name': self.admin_last_name,
            'message': f'A new salary advance application has been submitted by {self.full_name}. Please review it promptly.',
        }
        self.send_email(
            receiver_email=self.admin_email,
            context=context,
            subject="New Salary advance Application",
        )
        return HttpResponse("Email to manager sent successfully.")
    

    
class VetSalaryAdvanceNotification:
    def __init__(self, advc_id, action):
        self.advc_id = advc_id
        print(f"VetSalaryAdvanceNotification initialized with ID: {self.advc_id}")
        self.action = action

        if self.action == "Approved":
            self.message_body = "Your salary advance application has been approved. Funds will be disbursed shortly!"
        else:
            self.message_body = "We regret to inform you that your salary application has been rejected."

        try:
            advc_obj = SalaryAdvance.objects.get(id=self.advc_id)
            self.applicant_email = advc_obj.employee.email
            self.applicant_first_name = advc_obj.employee.first_name
            self.applicant_last_name = advc_obj.employee.last_name
        except SalaryAdvance.DoesNotExist:
            raise ValueError(f"Salary advance with ID {self.advc_id} does not exist.")

        self.validate_email(self.applicant_email)

    @staticmethod
    def validate_email(email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(f"Invalid email address: {email}")

    def send_mail_application(self):
        context = {
            "message": self.message_body,
            "first_name": self.applicant_first_name,
            "last_name": self.applicant_last_name,
        }

        receiver_email = self.applicant_email
        template_name = "notification/salary_advance_info.html"

        convert_to_html_content = render_to_string(template_name=template_name, context=context)
        plain_message = strip_tags(convert_to_html_content)

        send_mail(
            subject="Your salary advance application",
            message=plain_message,
            from_email="your_email@example.com",
            recipient_list=[receiver_email],
            html_message=convert_to_html_content,
            fail_silently=False,  
        )
        return HttpResponse("Email sent successfully.")