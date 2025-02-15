from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from base.utils import generate_username, generate_password
from notification.views import send_mail_new_employee
from django.contrib.auth.models import User
from django.contrib import messages
from base.models import Employee

@login_required(login_url='frontend:login')
def create_employee(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        middle_name = request.POST.get("middle_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        province = request.POST.get("province", "")
        city = request.POST.get("city", "")
        phone_number = request.POST.get("phone_number", "")
        address = request.POST.get("address", "")
        work_type = request.POST.get("work_type", "")
        department = request.POST.get("department", "")
        position = request.POST.get("position", "")
        employee_id = request.POST.get("employee_id", "")

        identification_type = request.POST.get("identification_type")  
        identification_number = request.POST.get("identification_number") 
        nhima_number = request.POST.get("nhima_number")  
        t_pin = request.POST.get("t_pin") 
        ss_number = request.POST.get("ssn")  

        id_front = request.FILES.get("id_front", None)
        id_back = request.FILES.get("id_back", None)

        if Employee.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken.")
            return redirect("frontend:add_employee")
        
        check_employee_id = Employee.objects.filter(employee_id = employee_id)
        if check_employee_id.exists():
            messages.warning(request, f'User with {employee_id} already exists')
            return redirect("frontend:add_employee")
        
        if not t_pin:
            t_pin = None

        if not nhima_number:
            nhima_number = None

        if ss_number:
            ss_number = None

        if not id_back:
            id_back = None

        username = generate_username()
        while User.objects.filter(username=username).exists():
            username = generate_username()

        password = generate_password(8)


        user = User.objects.create_user(username=username, password=password)
        user.save()

        print('Paasword: ', password, 'Username :', username, 'position: ', position)
        employee = Employee.objects.create(
            user=user,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            province=province,
            city=city,
            phone_number=phone_number,
            address=address,
            work_type=work_type,
            department=department,
            position=position,
            employee_id=employee_id,
            identification_type=identification_type, 
            identification_number=identification_number, 
            nhima_number=nhima_number, 
            t_pin=t_pin,
            ss_number=ss_number, 
            id_front=id_front,  
            id_back=id_back
        )
        
        send_mail_new_employee(email, username, password)
        messages.success(request, "Employee created successfully!")
        return redirect("frontend:add_employee")

    return redirect("frontend:add_employee")
