from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication
    path('', views.redirect_to_dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # Employee master (employee management)
    path('master/', views.master_view, name='master'),
    path('master/add/', views.add_employee_view, name='add_employee'),
    path('master/edit/<int:emp_id>/', views.edit_employee_view, name='edit_employee'),
    path('master/delete/<int:emp_id>/', views.delete_employee_view, name='delete_employee'),

    # User admin (Django user management)
    path('user-admin/', views.user_admin_view, name='user_admin'),
    path('user-admin/add/', views.add_user_view, name='add_user'),
    path('user-admin/edit/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('user-admin/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),

    # Attendance management
    path('attendance/', views.attendance_view, name='attendance'),
    path('attendance/edit/<int:att_id>/', views.edit_attendance, name='edit_attendance'),
    path('attendance/delete/<int:att_id>/', views.delete_attendance, name='delete_attendance'),

    # Functional views
    path('adjustments/', views.adjustments_view, name='adjustments'),
    path('processing/', views.processing_view, name='processing'),
    path('reports/', views.reports_view, name='reports'),
    path('enquiry/', views.enquiry_view, name='enquiry'),
    path('checklist/', views.checklist_view, name='checklist'),

    # Dashboard for each role
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/finance/', views.finance_dashboard, name='finance_dashboard'),
    path('dashboard/hr/', views.hr_dashboard, name='hr_dashboard'),

    # AJAX endpoints
    path('ajax/edit-attendance/', views.edit_attendance, name='ajax_edit_attendance'),
    path('ajax/edit-paybill/', views.edit_paybill, name='edit_paybill'),
    path('ajax/refresh-data/', views.refresh_data_view, name='refresh_data'),
]
