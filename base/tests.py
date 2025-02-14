from django.test import TestCase
from .models import Employee, Role, LeaveApplication, SalaryAdvance, LeaveCommutation
from django.contrib.auth.models import User
from datetime import date

class LeaveApplicationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john_doe', password='password')
        self.role = Role.objects.create(name='Admin')
        self.employee = Employee.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            province="Lusaka",
            city="Lusaka",
            phone_number="0976123456",
            address="123 Test St",
            work_type="full-time",
            department="hr",
            position="developer-snr",
            employee_id="EMP1234",
            nhima_number="NHM123456",
            ss_number="SS123456",
            t_pin="T123456",
        )
        self.leave_application = LeaveApplication.objects.create(
            employee=self.employee,
            leave_type="Sick Leave",
            start_date=date(2025, 2, 1),
            end_date=date(2025, 2, 7),
            reason="Illness",
            status="pending"
        )

    def test_leave_application_creation(self):
        """Test the creation of a leave application"""
        leave_application = self.leave_application
        self.assertEqual(leave_application.leave_type, "Sick Leave")
        self.assertEqual(leave_application.status, "pending")
        self.assertEqual(str(leave_application), f"Leave Application - {self.employee.first_name} {self.employee.last_name} (Sick Leave)")


class SalaryAdvanceModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john_doe', password='password')
        self.role = Role.objects.create(name='Admin')
        self.employee = Employee.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            province="Lusaka",
            city="Lusaka",
            phone_number="0976123456",
            address="123 Test St",
            work_type="full-time",
            department="hr",
            position="developer-snr",
            employee_id="EMP1234",
            nhima_number="NHM123456",
            ss_number="SS123456",
            t_pin="T123456",
        )
        self.salary_advance = SalaryAdvance.objects.create(
            employee=self.employee,
            amount=1500.00,
            approval_status="approved",
            repayment_start_date=date(2025, 3, 1)
        )

    def test_salary_advance_creation(self):
        """Test the creation of a salary advance request"""
        salary_advance = self.salary_advance
        self.assertEqual(salary_advance.amount, 1500.00)
        self.assertEqual(salary_advance.approval_status, "approved")
        self.assertEqual(str(salary_advance), f"Salary Advance - {self.employee.first_name} {self.employee.last_name} (1500.00)")


class LeaveCommutationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john_doe', password='password')
        self.role = Role.objects.create(name='Admin')
        self.employee = Employee.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            province="Lusaka",
            city="Lusaka",
            phone_number="0976123456",
            address="123 Test St",
            work_type="full-time",
            department="hr",
            position="developer-snr",
            employee_id="EMP1234",
            nhima_number="NHM123456",
            ss_number="SS123456",
            t_pin="T123456",
        )
        self.leave_application = LeaveApplication.objects.create(
            employee=self.employee,
            leave_type="Sick Leave",
            start_date=date(2025, 2, 1),
            end_date=date(2025, 2, 7),
            reason="Illness",
            status="approved"
        )
        self.leave_commutation = LeaveCommutation.objects.create(
            employee=self.employee,
            leave_application=self.leave_application,
            commutation_amount=500.00
        )

    def test_leave_commutation_creation(self):
        """Test the creation of a leave commutation"""
        leave_commutation = self.leave_commutation
        self.assertEqual(leave_commutation.commutation_amount, 500.00)
        self.assertEqual(str(leave_commutation), f"Leave Commutation - {self.employee.first_name} {self.employee.last_name} (500.00)")
