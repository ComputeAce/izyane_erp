from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from frontend.views.base_views import (
    login,
    home,
    profile,
    leave_view,
    user_profile,
    salary_advance_view,


)
from frontend.views.hr_views import (

    add_employee,
    employees,
    
    
)


from frontend.views.admin_views import (
    users,
    roles,
    leaves,
    salary_advance,
   
)


from frontend.views.employee_views import (
    leave_request,
    leave_commutation,
    salary_advance_request,
)

app_name = "frontend"
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('employees/', employees, name='employees'),
    path('add-add-employee/', add_employee, name='add_employee'),
    path('all-leaves/', leaves, name='leaves'),
    path('all-salary-advance/', salary_advance, name='salary_advance'),
    path('all-users/', users, name='users'),
    path('roles/', roles, name='roles'),
    path('profile/<int:id>/', profile, name='profile'),
    path('leave-request/', leave_request, name='leave_request'),
    path('leave-commutation/', leave_commutation, name='leave_commutation'),
    path('salary-advance-request/', salary_advance_request, name='salary_advance_request'),
    path('salary-advance-view/<int:id>/', salary_advance_view, name='salary_advance_view'),
    path('leave-view/<int:id>/', leave_view, name='leave_view'),
    path('user-profile/', user_profile, name='user_profile')
    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
