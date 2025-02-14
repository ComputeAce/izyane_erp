from django.urls import path
from .views.base_views import (
    login,
    user_logout,
    update_profile,
    update_password,
    submit_change_password,

)

from .views.human_resources import (
    create_employee,
)

from .views.employees_view import (
    leave_request,
    salary_advance_request

)

from .views.admin_views import (
    vett_salary_advc_request,
    vett_leave_request,
)
app_name = "base"
urlpatterns = [

    #base
    path('login', login, name='login'),
    path('user_logout/', user_logout, name='user_logout'),
    path('update_profile/', update_profile, name='update_profile'),
    path('submit_change_password/', submit_change_password, name='submit_change_password'),
    path('update_password/', update_password, name='update_password'),

    #HR
    path('create_employee/', create_employee, name='create_employee'),


    #Employee
    path('leave_request/', leave_request, name='leave_request'),
    path('salary_advance_request/', salary_advance_request, name='salary_advance_request'),


    #Admin
    path('vett_salary_advc_request/<int:id>/', vett_salary_advc_request, name='vett_salary_advc_request'),
    path('vett_leave_request/<int:id>/', vett_leave_request, name='vett_leave_request')
]
