from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Employee, Attendance, PayBill
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'emp_id', 'name', 'catg_desc', 'doj', 'emp_status', 'stipend_rate'
    )
    list_filter = ['catg_desc', 'emp_status', 'doj']
    search_fields = ['name', 'emp_id', 'pan', 'bank_acno']
    ordering = ['emp_id']
    fieldsets = (
        ('Personal Information', {
            'fields': ('emp_id', 'name', 'dob', 'doj', 'dos', 'sex_code')
        }),
        ('Employment Details', {
            'fields': ('emp_status', 'catg', 'catg_desc', 'speciality')
        }),
        ('Financial Information', {
            'fields': ('stipend_rate', 'daily_rate', 'bank_cd', 'bank_acno', 'pan')
        }),
        ('Training & Indicators', {
            'fields': ('trg_duration', 'stop_pay_ind', 'tuition_fee_ind', 'dnb_type')
        }),
    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'yymm', 'duty', 'al', 'cl', 'abs', 'pl', 'ml', 'total_days']
    list_filter = ['yymm', 'employee__catg_desc']
    search_fields = ['employee__name', 'employee__emp_id']
    ordering = ['-yymm', 'employee__name']

    def total_days(self, obj):
        return obj.total_days()
    total_days.short_description = 'Total Days'

    fieldsets = (
        ('Basic Information', {
            'fields': ('yymm', 'employee')
        }),
        ('Attendance Details', {
            'fields': ('duty', 'abs', 'al', 'cl', 'pl', 'ml')
        }),
    )

@admin.register(PayBill)
class PayBillAdmin(admin.ModelAdmin):
    list_display = ['employee', 'yymm', 'stipend', 'adj', 'gpay', 'npay', 'itaxrec']
    list_filter = ['yymm', 'employee__catg_desc']
    search_fields = ['employee__name', 'employee__emp_id']
    ordering = ['-yymm', 'employee__name']
    readonly_fields = ['gpay', 'npay', 'itaxrec', 'cessrec', 'cessaddl']

    fieldsets = (
        ('Basic Information', {
            'fields': ('yymm', 'employee')
        }),
        ('Salary Components', {
            'fields': ('stipend', 'adj')
        }),
        ('Calculated Fields (Read Only)', {
            'fields': ('gpay', 'npay', 'itaxrec', 'cessrec', 'cessaddl'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.calculate_pay()
        super().save_model(request, obj, form, change)

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    list_display = BaseUserAdmin.list_display

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.site_header = "DNB Pay System Administration"
admin.site.site_title = "DNB Pay Admin"
admin.site.index_title = "Welcome to DNB Pay System Administration"
