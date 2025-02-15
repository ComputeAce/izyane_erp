from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from base.models import Employee
from django.contrib import messages


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('frontend:home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('frontend:login')

    return redirect('frontend:login')  


def user_logout(request):
    auth_logout(request)
    messages.warning(request, 'You have been logged out!')
    return redirect('frontend:login')


@login_required(login_url='frontend:login')
def update_profile(request):
    if request.method == 'POST':
        user_obj = request.user
        errors = []

        get_first_name = request.POST.get('first_name')
        get_last_name = request.POST.get('last_name')
        get_email = request.POST.get('email')
        get_address = request.POST.get('address')
        get_phone_number = request.POST.get('phone_number')
        get_id_type = request.POST.get('id_type')
        get_identity_number = request.POST.get('identity_number')
        get_ssn = request.POST.get('ssn')
        get_tpin = request.POST.get('tpin')
        get_nhima_number = request.POST.get('nhima_number')

        if not get_first_name:
            errors.append("First name is required.")
        if not get_last_name:
            errors.append("Last name is required.")
        if not get_email:
            errors.append("Email is required.")
        if not get_address:
            errors.append("Address is required.")
        if not get_phone_number:
            errors.append("Phone number is required.")

        try:
            validate_email(get_email)
        except ValidationError:
            errors.append("Invalid email format.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('base:user_profile')
        
        get_user_prof = Employee.objects.filter(user=user_obj).first()
        
        if get_user_prof:  
            get_user_prof.first_name = get_first_name
            get_user_prof.last_name = get_last_name
            get_user_prof.email = get_email
            get_user_prof.address = get_address
            get_user_prof.phone_number = get_phone_number
            get_user_prof.identification_type = get_id_type
            get_user_prof.identification_number = get_identity_number
            get_user_prof.ss_number = get_ssn
            get_user_prof.t_pin = get_tpin
            get_user_prof.nhima_number = get_nhima_number

            if 'id_front' in request.FILES:
                get_user_prof.id_front = request.FILES['id_front']
            if 'id_back' in request.FILES:
                get_user_prof.id_back = request.FILES['id_back']

            get_user_prof.save()
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(request, "Profile not found.")

        return redirect('frontend:user_profile')

    return redirect('frontend:user_profile')


@login_required
def submit_change_password(request):
    if request.method == "POST":
        user = request.user

        get_new_password = request.POST.get('new_password')
        get_current_password = request.POST.get('current_password') 
        
        if not get_new_password:
            return JsonResponse({'error': 'New password is required'}, status=400)
        
        if get_current_password:
        
            user = authenticate(username=user.username, password=get_current_password)
            if not user:
                return JsonResponse({'error': 'Current password is incorrect'}, status=400)

        user.set_password(get_new_password)
        user.save()

        return JsonResponse({'message': 'Password updated successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)



@login_required
def update_password(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        username = request.user.username

        user = authenticate(username=username, password=current_password)
        if user:
            return JsonResponse({
                'status': 'success',
                'message': 'Password is correct',
                'current_password': current_password
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid password',
                'current_password': current_password
            })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def update_profile_pic(request):
    if request.method == 'POST':
        user = request.user.id
        profile_picture = request.POST.get('profile_picture')
        get_empl = Employee.objects.get(user_id = user)

        if get_empl:
            get_empl.profile_picture = profile_picture
            get_empl.save()

            messages.info(request, 'Profile Picture Updated Successfully.')
            return redirect('frontend:user_profile')

        else:
            
            messages.info(request, 'Error Updating Profile Picture.')
            return redirect('frontend:user_profile')