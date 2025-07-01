# DNB Pay System - Bhilai Steel Plant

A comprehensive Django-based payroll management system for DNB (Doctor of Nursing Bachelor) employees at Bhilai Steel Plant.

## Features

- **Role-based Authentication**: MAST (Admin), FIN (Finance), ATT (Attendance), EMP (Employee)
- **Employee Management**: Complete employee master data management
- **Attendance Tracking**: Monthly attendance with validation
- **Salary Processing**: Automated salary calculations with tax deductions
- **Seven Core Modules**: Processing, Master, Attendance, Adjustments, Reports, Enquiry, Checklist
- **Role-based Data Access**: Employees can only view their own data
- **Responsive Design**: Works on desktop and mobile devices

## Requirements

- Python 3.13+
- MySQL 5.7+
- Django 5.1.4

## Quick Setup

1. **Clone or extract the project**
2. **Create virtual environment**:
   ```bash
   python -m venv dnb_venv
   dnb_venv\Scripts\activate  # Windows
   source dnb_venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL database**:
   - Create database named `mydb`
   - Update password in `dnb_pay_system/settings.py`

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate dummy data**:
   ```bash
   python manage.py populate_dnb_data --clear
   ```

8. **Run server**:
   ```bash
   python manage.py runserver
   ```

## Login Credentials

### Admin Users
- **Admin**: admin_dnb / admin123
- **Finance**: finance_head / fin123  
- **HR**: hr_manager / hr123

### Employee Users (All use password: emp123)
- raj_dnb_junior, priya_dnb_senior, amit_contract, sneha_csr, etc.

## Project Structure

```
dnb_pay_system/
├── dnb_pay_system/          # Django project config
├── dnb_app/                 # Main application
├── templates/               # HTML templates
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Database Models

- **Employee**: Employee master data (DNBMAST)
- **Attendance**: Monthly attendance records (DNBATT)  
- **PayBill**: Salary processing (DNBPBILL)
- **UserProfile**: Extended user information

## Key Features

1. **Dashboard**: Role-based dashboards with relevant information
2. **Employee Master**: Complete CRUD operations for employee data
3. **Attendance**: Monthly attendance with leave type tracking
4. **Salary Processing**: Automated calculations with tax deductions
5. **Reports**: Role-based reporting system
6. **Search**: Advanced employee search functionality

## Security

- Role-based access control
- Data isolation for employees
- Secure authentication
- CSRF protection

## Support

For technical support or questions about the DNB Pay System, contact the development team.

## License

Proprietary - Bhilai Steel Plant
