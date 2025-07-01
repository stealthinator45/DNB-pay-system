from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dnb_app.models import Employee, Attendance, PayBill
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with DNB employee data from credentials document'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data first')

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            PayBill.objects.all().delete()
            Attendance.objects.all().delete()
            Employee.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write('Data cleared.')

        self.create_admin_users()
        self.create_employees()
        self.create_attendance_payroll()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated DNB employee data'))

    def create_admin_users(self):
        admin_users = [
            {'username': 'admin_dnb', 'password': 'admin123', 'role': 'MAST'},
            {'username': 'finance_head', 'password': 'fin123', 'role': 'FIN'},
            {'username': 'hr_manager', 'password': 'hr123', 'role': 'ATT'},
        ]
        
        for admin_data in admin_users:
            if not User.objects.filter(username=admin_data['username']).exists():
                # Fixed: Use admin_data instead of emp_data
                user = User.objects.create_user(
                    username=admin_data['username'],  # CORRECTED
                    password=admin_data['password'],  # CORRECTED
                    email=f"{admin_data['username']}@sail.in"  # CORRECTED
                )
                user.is_active = True
                user.save()

                Employee.objects.create(
                    user=user,
                    emp_id=9000 + len(Employee.objects.all()),
                    name=admin_data['username'].replace('_', ' ').title(),
                    dob='1980-01-01',
                    doj='2020-01-01',
                    emp_status=1,
                    stipend_rate=50000,
                    daily_rate=1667,
                    sex_code='M',
                    bank_cd='SBI00001',
                    bank_acno=f"9876543210{admin_data['username'][-3:]}",
                    pan=f"ADMIN{random.randint(1000,9999)}A",
                    catg=1,
                    catg_desc='Admin',
                    speciality='Administration',
                    trg_duration=0,
                    stop_pay_ind=0,
                    tuition_fee_ind=0,
                    dnb_type='Admin',
                    role=admin_data['role'],
                    is_online=False,
                    last_login_time=None,
                    last_logout_time=None
                )
                self.stdout.write(f'Created admin user: {admin_data["username"]}')

    def create_employees(self):
        employees_data = [
            # Engineering Department - DNB Junior Category
            {'username': 'raj_kumar', 'name': 'Raj Kumar Singh', 'emp_id': 1001, 'dept': 'Engineering', 'salary': 25000, 'catg': 1, 'catg_desc': 'DNB Junior', 'sex': 'M'},
            {'username': 'priya_sharma', 'name': 'Priya Sharma', 'emp_id': 1002, 'dept': 'Engineering', 'salary': 25000, 'catg': 1, 'catg_desc': 'DNB Junior', 'sex': 'F'},
            {'username': 'amit_verma', 'name': 'Amit Verma', 'emp_id': 1003, 'dept': 'Engineering', 'salary': 25000, 'catg': 1, 'catg_desc': 'DNB Junior', 'sex': 'M'},
            {'username': 'sneha_patel', 'name': 'Sneha Patel', 'emp_id': 1004, 'dept': 'Engineering', 'salary': 25000, 'catg': 1, 'catg_desc': 'DNB Junior', 'sex': 'F'},
            {'username': 'vikash_singh', 'name': 'Vikash Singh', 'emp_id': 1005, 'dept': 'Engineering', 'salary': 25000, 'catg': 1, 'catg_desc': 'DNB Junior', 'sex': 'M'},
            
            # Medical Department - DNB Senior Category
            {'username': 'dr_anita_roy', 'name': 'Dr. Anita Roy', 'emp_id': 1006, 'dept': 'Medical', 'salary': 35000, 'catg': 2, 'catg_desc': 'DNB Senior', 'sex': 'F'},
            {'username': 'dr_rohit_gupta', 'name': 'Dr. Rohit Gupta', 'emp_id': 1007, 'dept': 'Medical', 'salary': 35000, 'catg': 2, 'catg_desc': 'DNB Senior', 'sex': 'M'},
            {'username': 'dr_kavita_jain', 'name': 'Dr. Kavita Jain', 'emp_id': 1008, 'dept': 'Medical', 'salary': 35000, 'catg': 2, 'catg_desc': 'DNB Senior', 'sex': 'F'},
            {'username': 'dr_suresh_kumar', 'name': 'Dr. Suresh Kumar', 'emp_id': 1009, 'dept': 'Medical', 'salary': 35000, 'catg': 2, 'catg_desc': 'DNB Senior', 'sex': 'M'},
            {'username': 'dr_meera_singh', 'name': 'Dr. Meera Singh', 'emp_id': 1010, 'dept': 'Medical', 'salary': 35000, 'catg': 2, 'catg_desc': 'DNB Senior', 'sex': 'F'},
            
            # Operations Department - Contract Workers Category
            {'username': 'ramesh_yadav', 'name': 'Ramesh Yadav', 'emp_id': 1011, 'dept': 'Operations', 'salary': 20000, 'catg': 3, 'catg_desc': 'Contract', 'sex': 'M'},
            {'username': 'sunita_devi', 'name': 'Sunita Devi', 'emp_id': 1012, 'dept': 'Operations', 'salary': 20000, 'catg': 3, 'catg_desc': 'Contract', 'sex': 'F'},
            {'username': 'manoj_kumar', 'name': 'Manoj Kumar', 'emp_id': 1013, 'dept': 'Operations', 'salary': 20000, 'catg': 3, 'catg_desc': 'Contract', 'sex': 'M'},
            {'username': 'ravi_prasad', 'name': 'Ravi Prasad', 'emp_id': 1014, 'dept': 'Operations', 'salary': 20000, 'catg': 3, 'catg_desc': 'Contract', 'sex': 'M'},
            {'username': 'deepak_tiwari', 'name': 'Deepak Tiwari', 'emp_id': 1015, 'dept': 'Operations', 'salary': 20000, 'catg': 3, 'catg_desc': 'Contract', 'sex': 'M'},
            
            # Administration Department - CSR Staff Category
            {'username': 'anjali_mishra', 'name': 'Anjali Mishra', 'emp_id': 1016, 'dept': 'Administration', 'salary': 30000, 'catg': 4, 'catg_desc': 'CSR', 'sex': 'F'},
            {'username': 'rahul_sharma', 'name': 'Rahul Sharma', 'emp_id': 1017, 'dept': 'Administration', 'salary': 30000, 'catg': 4, 'catg_desc': 'CSR', 'sex': 'M'},
            {'username': 'pooja_agarwal', 'name': 'Pooja Agarwal', 'emp_id': 1018, 'dept': 'Administration', 'salary': 30000, 'catg': 4, 'catg_desc': 'CSR', 'sex': 'F'},
            {'username': 'sanjeev_dubey', 'name': 'Sanjeev Dubey', 'emp_id': 1019, 'dept': 'Administration', 'salary': 30000, 'catg': 4, 'catg_desc': 'CSR', 'sex': 'M'},
            {'username': 'kavita_singh', 'name': 'Kavita Singh', 'emp_id': 1020, 'dept': 'Administration', 'salary': 30000, 'catg': 4, 'catg_desc': 'CSR', 'sex': 'F'},
        ]

        for emp_data in employees_data:
            if not User.objects.filter(username=emp_data['username']).exists():
                try:
                    # Create Django User with properly hashed password
                    user = User.objects.create_user(
                        username=emp_data['username'],
                        password='emp123',  # Django automatically hashes this
                        email=f"{emp_data['username']}@sail.in",
                        first_name=emp_data['name'].split()[0],
                        last_name=' '.join(emp_data['name'].split()[1:]) if len(emp_data['name'].split()) > 1 else ''
                    )
                    user.is_active = True
                    user.save()

                    # Create Employee record with complete data
                    Employee.objects.create(
                        user=user,
                        emp_id=emp_data['emp_id'],
                        name=emp_data['name'],
                        dob=f"199{random.randint(0,5)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                        doj=f"202{random.randint(0,3)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                        emp_status=1,
                        stipend_rate=emp_data['salary'],
                        daily_rate=emp_data['salary'] // 30,
                        sex_code=emp_data['sex'],
                        bank_cd='SBI00001',
                        bank_acno=f"1234567890{emp_data['emp_id']}",
                        pan=f"ABCDE{emp_data['emp_id']}F",
                        catg=emp_data['catg'],
                        catg_desc=emp_data['catg_desc'],
                        speciality=emp_data['dept'],
                        trg_duration=0,
                        stop_pay_ind=0,
                        tuition_fee_ind=0,
                        dnb_type='TypeA',
                        role='EMP',
                        is_online=False,
                        last_login_time=None,
                        last_logout_time=None
                    )
                    self.stdout.write(f'Created employee: {emp_data["username"]} ({emp_data["name"]})')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating {emp_data["username"]}: {str(e)}'))

    def create_attendance_payroll(self):
        """Create attendance and payroll records for the last 6 months"""
        self.stdout.write('Creating attendance and payroll data...')
        
        employees = Employee.objects.filter(role='EMP')
        
        for employee in employees:
            for month_ago in range(6):
                # Calculate year-month for each of the last 6 months
                target_date = datetime.now() - timedelta(days=30 * month_ago)
                yymm = int(target_date.strftime('%y%m'))
                
                # Create Attendance record
                if not Attendance.objects.filter(employee=employee, yymm=yymm).exists():
                    attendance = Attendance.objects.create(
                        yymm=yymm,
                        employee=employee,
                        duty=random.randint(20, 28),
                        al=random.randint(0, 2),
                        cl=random.randint(0, 1),
                        abs=random.randint(0, 2),
                        pl=0,
                        ml=0
                    )
                    
                # Create PayBill record
                if not PayBill.objects.filter(employee=employee, yymm=yymm).exists():
                    PayBill.objects.create(
                        yymm=yymm,
                        employee=employee,
                        stipend=employee.stipend_rate,
                        adj=random.randint(-2000, 2000),  # Random adjustment
                        itaxrec=0,
                        cessrec=0,
                        cessaddl=0,
                        gpay=employee.stipend_rate,
                        npay=employee.stipend_rate,
                        higher_tax_ind=0
                    )
                    
        self.stdout.write(f'Created attendance and payroll data for {employees.count()} employees')
