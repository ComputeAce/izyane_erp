from django.db import models
from django.contrib.auth.models import User

class Permission(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)

    PROVINCE_CHOICES = [
        ('Central', 'Central'),
        ('Copperbelt', 'Copperbelt'),
        ('Eastern', 'Eastern'),
        ('Luapula', 'Luapula'),
        ('Lusaka', 'Lusaka'),
        ('Muchinga', 'Muchinga'),
        ('Northern', 'Northern'),
        ('North-Western', 'North-Western'),
        ('Southern', 'Southern'),
        ('Western', 'Western'),
    ]
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    WORK_TYPE_CHOICES = [
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]
    work_type = models.CharField(max_length=20, choices=WORK_TYPE_CHOICES)

    DEPARTMENT_CHOICES = [
        ('Human Resources', 'Human Resources'),
        ('Information Technology', 'Information Technology'),
        ('sales/marketing', 'Sales/Marketing'),
        ('Finance', 'Finance'),
        ('Engineering', 'Engineering'),
    ]
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)

    POSITION_CHOICES = [
        ('Admin', 'Admin'),
        ('TDR', 'TDR'),
        ('developer-snr', 'Developer (Senior)'),
        ('developer-jrn', 'Developer (Junior)'),
        ('developer-intern', 'Developer (Intern)'),
        ('accountant', 'Accountant'),
    ]
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('HR', 'HR'),
        ('Accountant', 'Accountant'),
        ('Employee', 'Employee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Employee")

    employee_id = models.CharField(max_length=20, unique=True)

    IDENTIFICATION_TYPE_CHOICES = [
        ('nrc', 'National Registration Card (NRC)'),
        ('passport', 'Passport'),
    ]
    identification_type = models.CharField(max_length=20, choices=IDENTIFICATION_TYPE_CHOICES, null=True, blank=True)
    identification_number = models.CharField(max_length=50, null=True, blank=True)
    id_front = models.ImageField(upload_to='employee_ids/fronts/')
    id_back = models.ImageField(upload_to='employee_ids/backs/')
    nhima_number = models.CharField(max_length=20, null=True, blank=True)
    ss_number = models.CharField(max_length=20, null=True, blank=True)
    t_pin = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"

    def has_permission(self, permission_name):
        return permission_name in self.get_permissions()

class LeaveApplication(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status_choices = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Leave Application - {self.employee.first_name} {self.employee.last_name} ({self.leave_type})"

class SalaryAdvance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_date = models.DateField(auto_now_add=True)
    reason = models.TextField(null=True, blank=True)
    approval_status_choices = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    approval_status = models.CharField(max_length=10, choices=approval_status_choices, default='pending')


    def __str__(self):
        return f"Salary Advance - {self.employee.first_name} {self.employee.last_name} ({self.amount:.2f})"

class LeaveCommutation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_application = models.ForeignKey(LeaveApplication, on_delete=models.CASCADE)
    commutation_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commutation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Leave Commutation - {self.employee.first_name} {self.employee.last_name} ({self.commutation_amount:.2f})"
