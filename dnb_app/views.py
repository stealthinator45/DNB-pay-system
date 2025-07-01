import json
from .utils import get_category_desc
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction
from .models import Employee, Attendance, PayBill
from .forms import EmployeeForm, AttendanceForm, LoginForm, CombinedUserEmployeeForm, CustomUserCreationForm, UserEditForm
from django.db.models import Sum
import calendar
from django.db.models import Q, F, Max
from django.http import JsonResponse
from datetime import datetime
from .forms import UserEditForm



# Role to category description mapping - CONSISTENT NAMING
ROLE_TO_DESC = {
    'DNB': 'DNB',
    'CONTRACTUAL': 'CONTRACTUAL',
    'CSR': 'CSR'
}

@login_required
def finance_dashboard(request):
    user_role = request.session.get('user_role', 'EMP')
    if user_role != 'FIN':
        messages.error(request, "You don't have permission to access this page")
        return redirect('login')
    
    context = {
        'total_payroll': PayBill.objects.aggregate(total=Sum('gpay'))['total'] or 0,
        'pending_payments': PayBill.objects.filter(npay=0).count(),
        'recent_transactions': PayBill.objects.order_by('-yymm')[:5],
        'user_role': user_role
    }
    return render(request, 'finance_dashboard.html', context)

@login_required
def attendance_dashboard(request):
    user_role = request.session.get('user_role', 'EMP')
    context = {
        'user_role': user_role,
        'total_employees': Employee.objects.count(),
        'present_today': Attendance.objects.filter(yymm=int(datetime.now().strftime('%y%m'))).aggregate(Sum('duty'))['duty__sum'] or 0,
        'absent_today': Attendance.objects.filter(yymm=int(datetime.now().strftime('%y%m'))).aggregate(Sum('abs'))['abs__sum'] or 0,
        'recent_attendance': Attendance.objects.select_related('employee').order_by('-yymm')[:5],
    }
    return render(request, 'attendance_dashboard.html', context)

@login_required
def hr_dashboard(request):
    user_role = request.session.get('user_role', 'EMP')
    
    if user_role != 'HR':
        messages.error(request, "You don't have permission to access this page")
        return redirect('login')
    
    current_month = datetime.now().strftime('%y%m')
    context = {
        'attendance_summary': Attendance.objects.filter(yymm=current_month).aggregate(
            total_duty=Sum('duty'),
            total_abs=Sum('abs')
        ),
        'recent_attendance': Attendance.objects.order_by('-yymm')[:5],
        'user_role': user_role
    }
    return render(request, 'hr_dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            
            # Set user_role based on username
            if user.is_superuser:
                request.session['user_role'] = 'SUPER'
            elif user.username == 'DNB':
                request.session['user_role'] = 'DNB'
            elif user.username == 'CONTRACTUAL':
                request.session['user_role'] = 'CONTRACTUAL'
            elif user.username == 'CSR':
                request.session['user_role'] = 'CSR'
            elif user.is_staff:
                request.session['user_role'] = 'ADMIN'
            else:
                request.session['user_role'] = 'EMP'
            
            # Redirect based on role
            user_role = request.session['user_role']
            if user_role in ['SUPER', 'ADMIN', 'DNB', 'CONTRACTUAL', 'CSR']:
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'login.html')


def custom_logout(request):
    try:
        if hasattr(request.user, 'employee'):
            request.user.employee.is_online = False
            request.user.employee.last_logout_time = timezone.now()
            request.user.employee.save()
    except:
        pass
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard(request):
    user_role = request.session.get('user_role', 'EMP')
    context = {'user_role': user_role, 'user': request.user}
    
    if user_role in ['SUPER', 'ADMIN', 'DNB', 'CONTRACTUAL', 'CSR']:
        return redirect('admin_dashboard')
    elif user_role in ['MAST', 'FIN', 'ATT']:
        context.update({
            'total_employees': Employee.objects.count(),
            'active_employees': Employee.objects.filter(emp_status=1).count(),
            'recent_attendance': Attendance.objects.select_related('employee').order_by('-yymm')[:5],
            'recent_payroll': PayBill.objects.select_related('employee').order_by('-yymm')[:5],
        })
        return render(request, 'admin_dashboard.html', context)
    else:
        return employee_dashboard(request)



@login_required
def admin_dashboard(request):
    user_role = request.session.get('user_role', 'EMP')
    user = request.user

    # Show only total employees for the user's category, or all if superuser
    if user_role in ['DNB', 'CONTRACTUAL', 'CSR']:
        total_employees = Employee.objects.filter(catg_desc=user_role).count()
    else:
        total_employees = Employee.objects.count()

    context = {
        'user_role': user_role,
        'user': user,
        'total_employees': total_employees,
    }
    return render(request, 'admin_dashboard.html', context)



@login_required
def employee_dashboard(request):
    context = {'user_role': request.session.get('user_role', 'EMP')}
    try:
        employee = request.user.employee
        context['employee'] = employee
        attendance_records = Attendance.objects.filter(employee=employee).order_by('-yymm')[:6]
        pay_records = PayBill.objects.filter(employee=employee).order_by('-yymm')[:6]
        context['attendance_records'] = attendance_records
        context['pay_records'] = pay_records
        context['last_salary'] = pay_records[0] if pay_records else None
        
        if attendance_records:
            latest_att = attendance_records[0]
            present_days = latest_att.duty or 0
            absent_days = latest_att.abs or 0
            leave_days = (latest_att.al or 0) + (latest_att.cl or 0) + (latest_att.pl or 0) + (latest_att.ml or 0)
            context.update({
                'total_leaves': leave_days,
                'present_days': present_days,
                'absent_days': absent_days,
                'leave_days': leave_days,
                'chart_data': json.dumps([present_days, absent_days, leave_days])
            })
        else:
            context.update({
                'total_leaves': 0,
                'present_days': 0,
                'absent_days': 0,
                'leave_days': 0,
                'chart_data': json.dumps([0, 0, 0])
            })
    except AttributeError:
        context.update({
            'attendance_records': [],
            'pay_records': [],
            'last_salary': None,
            'total_leaves': 0,
            'present_days': 0,
            'absent_days': 0,
            'leave_days': 0,
            'chart_data': json.dumps([0, 0, 0])
        })
    return render(request, 'employee_dashboard.html', context)


# Map user_role to category description for filtering
ROLE_TO_DESC = {
    'DNB': 'DNB',
    'CONTRACTUAL': 'CONTRACTUAL',
    'CSR': 'CSR'
}

@login_required
def master_view(request):
    user_role = request.session.get('user_role', 'EMP')
    # Allow SUPER, ADMIN, DNB, CONTRACTUAL, CSR
    allowed_roles = ['SUPER', 'ADMIN', 'DNB', 'CONTRACTUAL', 'CSR']
    if user_role not in allowed_roles:
        messages.error(request, "You do not have permission to access Employee Master.")
        return redirect('dashboard')
    excluded_names = ['admin_dnb', 'admin_dnb4', 'finance_head', 'hr_manager']
    # Category-based filtering for DNB, CONTRACTUAL, CSR
    if user_role in ROLE_TO_DESC:
        employees = Employee.objects.filter(catg_desc=ROLE_TO_DESC[user_role]).exclude(name__in=excluded_names)
    else:
        employees = Employee.objects.exclude(name__in=excluded_names)
    context = {
        'employees': employees,
        'user_role': user_role,
        'active_tab': 'master',
        'can_create_employees': user_role in allowed_roles,
        'total_employees': employees.count(),
    }
    return render(request, 'master.html', context)



@login_required
def user_admin_view(request):
    user_role = request.session.get('user_role', 'EMP')
    if user_role not in ['SUPER', 'ADMIN', 'DNB', 'CONTRACTUAL', 'CSR']:
        messages.error(request, "Permission denied")
        return redirect('dashboard')

    # Show all staff/admin users
    admins = User.objects.filter(is_staff=True).order_by('username')

    context = {
        'admins': admins,
        'user_role': user_role,
        'active_tab': 'user_admin',
        'can_create_admins': user_role in ['SUPER', 'ADMIN'],
        'total_admins': admins.count(),
    }
    return render(request, 'user_admin.html', context)





@login_required
def attendance_view(request):
    user_role = request.session.get('user_role', 'EMP')
    now = datetime.now()
    prev_month = now.month - 1 if now.month > 1 else 12
    prev_year = now.year if now.month > 1 else now.year - 1
    prev_yymm = int(f"{str(prev_year)[2:]}{prev_month:02d}")
    prev_month_days = calendar.monthrange(prev_year, prev_month)[1]

    # Filter employees by role/category
    if user_role in ['DNB', 'CONTRACTUAL', 'CSR']:
        employees = Employee.objects.filter(catg_desc=user_role)
    else:
        employees = Employee.objects.all()

    # For each employee, get or create attendance for previous month
    attendance_records = []
    for emp in employees:
        att, created = Attendance.objects.get_or_create(
            employee=emp, yymm=prev_yymm,
            defaults={
                'duty': 0, 'al': 0, 'cl': 0, 'pl': 0, 'ml': 0,
                'abs': prev_month_days
            }
        )
        attendance_records.append(att)

    context = {
        'attendance_records': attendance_records,
        'user_role': user_role,
        'prev_yymm': prev_yymm,
        'prev_month_days': prev_month_days,  # This is critical!
    }
    return render(request, 'attendance.html', context)






@login_required
def adjustments_view(request):
    user_role = request.session.get('user_role', 'EMP')
    
    # Category-based filtering for DNB, CONTRACTUAL, CSR admins
    if user_role in ROLE_TO_DESC:
        adjustments = PayBill.objects.filter(employee__catg_desc=ROLE_TO_DESC[user_role])
    elif user_role in ['SUPER', 'ADMIN', 'FIN', 'HR']:
        adjustments = PayBill.objects.select_related('employee').all()
    else:
        try:
            employee = request.user.employee_profile
            adjustments = PayBill.objects.filter(employee=employee)
        except AttributeError:
            adjustments = PayBill.objects.none()
    
    context = {
        'adjustments': adjustments,
        'user_role': user_role
    }
    return render(request, 'adjustments.html', context)

@login_required
def processing_view(request):
    """View for payroll processing with role-based category filtering"""
    user_role = request.session.get('user_role', 'EMP')
    context = {'user_role': user_role}
    
    # Category-based filtering for DNB, CONTRACTUAL, CSR admins
    if user_role in ROLE_TO_DESC:
        context['employees'] = Employee.objects.filter(catg_desc=ROLE_TO_DESC[user_role])
        context['pay_bills'] = PayBill.objects.filter(employee__catg_desc=ROLE_TO_DESC[user_role])
    elif user_role in ['MAST', 'FIN', 'ATT', 'SUPER', 'ADMIN']:
        context['employees'] = Employee.objects.all()
        context['pay_bills'] = PayBill.objects.all()
        context['current_month'] = datetime.now().strftime('%y%m')
    else:
        context['employees'] = Employee.objects.none()
        context['pay_bills'] = PayBill.objects.none()
    
    return render(request, 'processing.html', context)

@login_required
def reports_view(request):
    user_role = request.session.get('user_role', 'EMP')
    context = {'user_role': user_role}
    current_yymm = datetime.now().strftime('%y%m')

    # Category-based filtering for DNB, CONTRACTUAL, CSR admins
    if user_role in ROLE_TO_DESC:
        context.update({
            'total_employees': Employee.objects.filter(catg_desc=ROLE_TO_DESC[user_role]).count(),
            'monthly_payroll': PayBill.objects.filter(yymm=current_yymm, employee__catg_desc=ROLE_TO_DESC[user_role]),
            'attendance_summary': Attendance.objects.filter(yymm=current_yymm, employee__catg_desc=ROLE_TO_DESC[user_role]),
            'attendance_months': json.dumps([]),
            'attendance_percentages': json.dumps([]),
        })
    elif user_role in ['MAST', 'FIN', 'ATT', 'SUPER', 'ADMIN']:
        attendance_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        attendance_percentages = [97, 88, 93, 99, 90, 95]
        context.update({
            'attendance_months': json.dumps(attendance_months),
            'attendance_percentages': json.dumps(attendance_percentages),
            'total_employees': Employee.objects.count(),
            'monthly_payroll': PayBill.objects.filter(yymm=current_yymm),
            'attendance_summary': Attendance.objects.filter(yymm=current_yymm),
        })
    else:
        try:
            employee = request.user.employee
            context.update({
                'employee': employee,
                'pay_statements': PayBill.objects.filter(employee=employee).order_by('-yymm')[:12],
                'attendance_history': Attendance.objects.filter(employee=employee).order_by('-yymm')[:12],
                'attendance_months': json.dumps([]),
                'attendance_percentages': json.dumps([]),
            })
        except Exception:
            context['employee'] = None
            context['attendance_months'] = json.dumps([])
            context['attendance_percentages'] = json.dumps([])
    
    return render(request, 'reports.html', context)

@login_required
def enquiry_view(request):
    user_role = request.session.get('user_role', 'EMP')
    search_results = []
    query = request.GET.get('q', '')

    if query:
        if user_role in ROLE_TO_DESC:
            search_results = Employee.objects.filter(
                (Q(name__icontains=query) | 
                 Q(emp_id__icontains=query) |
                 Q(catg_desc__icontains=query)) &
                Q(catg_desc=ROLE_TO_DESC[user_role])
            )
        elif user_role in ['MAST', 'FIN', 'ATT', 'SUPER', 'ADMIN']:
            search_results = Employee.objects.filter(
                Q(name__icontains=query) | 
                Q(emp_id__icontains=query) |
                Q(catg_desc__icontains=query)
            )
        else:
            try:
                employee = request.user.employee
                if query.lower() in employee.name.lower() or str(employee.emp_id) == query:
                    search_results = [employee]
            except Exception:
                search_results = []
    
    context = {'user_role': user_role, 'search_results': search_results, 'query': query}
    return render(request, 'enquiry.html', context)

@login_required
def checklist_view(request):
    user_role = request.session.get('user_role', 'EMP')
    checklist_items = []
    current_month = datetime.now().strftime('%y%m')

    if user_role in ROLE_TO_DESC:
        checklist_items = [
            {
                'item': 'Employee Data Validation',
                'status': Employee.objects.filter(emp_status=1, catg_desc=ROLE_TO_DESC[user_role]).count() > 0,
                'count': Employee.objects.filter(emp_status=1, catg_desc=ROLE_TO_DESC[user_role]).count(),
            },
            {
                'item': 'Attendance Records Current Month',
                'status': Attendance.objects.filter(yymm=current_month, employee__catg_desc=ROLE_TO_DESC[user_role]).count() > 0,
                'count': Attendance.objects.filter(yymm=current_month, employee__catg_desc=ROLE_TO_DESC[user_role]).count(),
            },
            {
                'item': 'Payroll Processing',
                'status': PayBill.objects.filter(yymm=current_month, employee__catg_desc=ROLE_TO_DESC[user_role]).count() > 0,
                'count': PayBill.objects.filter(yymm=current_month, employee__catg_desc=ROLE_TO_DESC[user_role]).count(),
            },
        ]
    elif user_role in ['MAST', 'FIN', 'ATT', 'SUPER', 'ADMIN']:
        checklist_items = [
            {
                'item': 'Employee Data Validation',
                'status': Employee.objects.filter(emp_status=1).count() > 0,
                'count': Employee.objects.filter(emp_status=1).count(),
            },
            {
                'item': 'Attendance Records Current Month',
                'status': Attendance.objects.filter(yymm=current_month).count() > 0,
                'count': Attendance.objects.filter(yymm=current_month).count(),
            },
            {
                'item': 'Payroll Processing',
                'status': PayBill.objects.filter(yymm=current_month).count() > 0,
                'count': PayBill.objects.filter(yymm=current_month).count(),
            },
        ]
    else:
        try:
            employee = request.user.employee
            checklist_items = [
                {
                    'item': 'Profile Complete',
                    'status': bool(employee.bank_acno and employee.pan),
                    'description': 'Bank and PAN details'
                },
                {
                    'item': 'Current Month Attendance',
                    'status': Attendance.objects.filter(employee=employee, yymm=current_month).exists(),
                    'description': f'Attendance for {current_month}'
                },
                {
                    'item': 'Salary Processed',
                    'status': PayBill.objects.filter(employee=employee, yymm=current_month).exists(),
                    'description': f'Salary for {current_month}'
                },
            ]
        except Exception:
            checklist_items = []

    context = {'user_role': user_role, 'checklist_items': checklist_items}
    return render(request, 'checklist.html', context)

# AJAX VIEWS


@csrf_exempt
@login_required
def edit_attendance(request, att_id):
    user_role = request.session.get('user_role', 'EMP')
    if user_role not in ['DNB', 'CONTRACTUAL', 'CSR']:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        att = Attendance.objects.get(id=att_id)
    except Attendance.DoesNotExist:
        return JsonResponse({'error': 'Attendance record not found'}, status=404)

    if request.method == "POST":
        try:
            duty = int(request.POST.get('duty', 0))
            al = int(request.POST.get('al', 0))
            cl = int(request.POST.get('cl', 0))
            ml = int(request.POST.get('ml', 0))
            pl = int(request.POST.get('pl', 0))
            absent = int(request.POST.get('absent', 0))

            # Validate sum of days
            yymm_str = str(att.yymm)
            year = int('20' + yymm_str[:2])
            month = int(yymm_str[2:])
            prev_month_days = calendar.monthrange(year, month)[1]

            if duty + al + cl + ml + pl + absent != prev_month_days:
                return JsonResponse({'error': f'Total days mismatch: sum is {duty + al + cl + ml + pl + absent}, expected {prev_month_days}'}, status=400)

            att.duty = duty
            att.al = al
            att.cl = cl
            att.ml = ml
            att.pl = pl
            att.abs = absent
            att.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@login_required
def edit_paybill(request):
    user_role = request.session.get('user_role', 'EMP')
    if user_role not in ['FIN', 'ATT', 'MAST', 'SUPER', 'ADMIN']:
        return HttpResponseForbidden("You do not have permission to edit paybill.")
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            pb_id = data.get('id')
            stipend = data.get('stipend')
            adj = data.get('adj')
            
            paybill = PayBill.objects.get(id=pb_id)
            paybill.stipend = stipend
            paybill.adj = adj
            paybill.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def add_employee_view(request):
    user_role = request.session.get('user_role', 'EMP')
    allowed_roles = ['SUPER', 'ADMIN', 'DNB', 'CONTRACTUAL', 'CSR']
    if user_role not in allowed_roles:
        messages.error(request, 'You do not have permission to add employees.')
        return redirect('master')
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.name} created successfully!')
            return redirect('master')
    else:
        form = EmployeeForm()
    context = {
        'form': form,
        'user_role': user_role,
    }
    return render(request, 'add_employee.html', context)

@login_required
def edit_employee_view(request, emp_id):
    user_role = request.session.get('user_role', 'EMP')
    allowed_roles = ['SUPER', 'ADMIN', 'DNB', 'CONTRACTUAL', 'CSR']
    if user_role not in allowed_roles:
        messages.error(request, "You do not have permission to edit employees.")
        return redirect('master')
    employee = get_object_or_404(Employee, emp_id=emp_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee {employee.name} updated successfully!')
            return redirect('master')
    else:
        form = EmployeeForm(instance=employee)
    context = {
        'form': form,
        'employee': employee,
        'user_role': user_role,
    }
    return render(request, 'edit_employee.html', context)

@login_required
def delete_employee_view(request, emp_id):
    user_role = request.session.get('user_role', 'EMP')
    allowed_roles = ['SUPER', 'ADMIN', 'DNB', 'CONTRACTUAL', 'CSR']
    if user_role not in allowed_roles:
        messages.error(request, "Permission denied")
        return redirect('master')
    employee = get_object_or_404(Employee, emp_id=emp_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee deleted successfully!")
        return redirect('master')
    return redirect('master')



# USER CRUD VIEWS
@login_required
def add_user_view(request):
    user_role = request.session.get('user_role', 'EMP')
    
    if user_role not in ['SUPER', 'ADMIN']:
        messages.error(request, "You don't have permission to add users")
        return redirect('user_admin')
    
    if user_role == 'ADMIN':
        allowed_roles = [
            ('DNB', 'DNB Admin'),
            ('CONTRACTUAL', 'Contractual Admin'),
            ('CSR', 'CSR Admin'),
            ('finance_head', 'Finance Head'),
            ('hr_manager', 'HR Manager')
        ]
    else:  # SUPER
        allowed_roles = [
            ('admin', 'Admin'),
            ('DNB', 'DNB Admin'),
            ('CONTRACTUAL', 'Contractual Admin'),
            ('CSR', 'CSR Admin'),
            ('finance_head', 'Finance Head'),
            ('hr_manager', 'HR Manager'),
            ('superuser', 'Superuser')
        ]
    
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        selected_role = request.POST.get('role')
        
        allowed_role_values = [role[0] for role in allowed_roles]
        if selected_role not in allowed_role_values:
            messages.error(request, "You do not have permission to create this role.")
            return render(request, 'add_user.html', {
                'user_form': user_form,
                'user_role': user_role,
                'allowed_roles': allowed_roles,
            })
        
        if user_form.is_valid():
            try:
                with transaction.atomic():
                    new_user = user_form.save(commit=False)
                    
                    if selected_role == 'admin':
                        new_user.is_staff = True
                        new_user.is_superuser = False
                    elif selected_role in ['DNB', 'CONTRACTUAL', 'CSR']:
                        new_user.is_staff = True
                        new_user.is_superuser = False
                        new_user.username = selected_role  # Set username to role for identification
                    elif selected_role in ['finance_head', 'hr_manager']:
                        new_user.is_staff = True
                        new_user.is_superuser = False
                    elif selected_role == 'superuser':
                        new_user.is_staff = True
                        new_user.is_superuser = True
                    
                    new_user.save()
                    messages.success(request, f"User {new_user.username} created successfully as {dict(allowed_roles)[selected_role]}!")
                    return redirect('user_admin')
            except Exception as e:
                messages.error(request, f"Error creating user: {str(e)}")
    else:
        user_form = CustomUserCreationForm()
    
    return render(request, 'add_user.html', {
        'user_form': user_form,
        'user_role': user_role,
        'allowed_roles': allowed_roles,
    })





# UTILITY VIEWS
@csrf_exempt
@login_required
def refresh_data_view(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                employees = Employee.objects.select_related('user').all()
                for emp in employees:
                    emp.refresh_from_db()
                    if emp.user:
                        emp.user.refresh_from_db()
                return JsonResponse({'status': 'success', 'message': 'Data refreshed successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def redirect_to_dashboard(request):
    if request.user.is_authenticated:
        try:
            role = request.user.employee_profile.role
            if role in ['SUPER', 'ADMIN']:
                return redirect('admin_dashboard')
            elif role == 'FIN':
                return redirect('finance_dashboard')
            elif role == 'HR':
                return redirect('hr_dashboard')
            else:
                return redirect('employee_dashboard')
        except AttributeError:
            return redirect('login')
    return redirect('login')




@login_required
def edit_user_view(request, user_id):
    user_role = request.session.get('user_role', 'EMP')
    admin_user = get_object_or_404(User, id=user_id)

    # Restrict all except SUPER and ADMIN from editing users
    if user_role not in ['SUPER', 'ADMIN']:
        messages.error(request, "You don't have permission to edit users")
        return redirect('user_admin')

    # DNB, CONTRACTUAL, CSR cannot edit admin_dnb or admin_dnb4
    if user_role in ['DNB', 'CONTRACTUAL', 'CSR'] and admin_user.username in ['admin_dnb', 'admin_dnb4']:
        messages.error(request, "No permission to edit this user")
        return redirect('user_admin')

    # Only SUPER can edit superuser or admin_dnb
    if (admin_user.is_superuser or admin_user.username == 'admin_dnb') and user_role != 'SUPER':
        messages.error(request, "No permission to edit this user")
        return redirect('user_admin')

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=admin_user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {admin_user.username} updated successfully!")
            return redirect('user_admin')
    else:
        form = UserEditForm(instance=admin_user)

    context = {
        'form': form,
        'admin_user': admin_user,
        'user_role': user_role,
    }
    return render(request, 'edit_user.html', context)




@login_required
def delete_user_view(request, user_id):
    user_role = request.session.get('user_role', 'EMP')
    if user_role != 'SUPER':
        messages.error(request, "Only SUPER can delete users.")
        return redirect('user_admin')

    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('user_admin')

    # If you use a confirmation page, render it here; else, just redirect
    return redirect('user_admin')


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Only if you can't use CSRF token in AJAX; otherwise, keep CSRF token in headers
@login_required
def delete_attendance(request, att_id):
    if request.method == 'POST':
        att = get_object_or_404(Attendance, id=att_id)
        att.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
