from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
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




