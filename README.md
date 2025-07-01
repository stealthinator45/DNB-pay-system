# 🚀 DNB Pay System – Modern Attendance & Payroll Management


## 🌟 Project Overview

**DNB Pay System** is a robust, secure, and scalable web application built with Django and MySQL, designed to modernize attendance and payroll workflows for Sector 9 Hospital, BSP.  
It replaces legacy systems with a user-friendly, role-based platform that automates HR processes, ensures data integrity, and supports efficient payroll management.

## 🎯 Key Features

- **Role-Based Access Control**  
  Secure authentication for DNB, CSR, Contractual, Finance, and Super Admin users.
- **Dynamic Dashboards**  
  Personalized dashboards with real-time stats and navigation for each role.
- **Employee Master Management**  
  Add, edit, and view employee details with category-specific logic.
- **Attendance Automation**  
  Quick entry, editing, and auto-calculation of absents based on month and leave types.
- **Payroll Processing**  
  Automated salary computation and adjustments from attendance data.
- **Comprehensive Reporting**  
  Built-in reports and checklists for compliance and audits.
- **Modern UI**  
  Responsive, clean Bootstrap interface with intuitive forms and tables.
- **Security**  
  Strong authentication, session management, and restricted access to sensitive operations.

## 🛠️ Project Flow
![image](https://github.com/user-attachments/assets/6a575c35-1821-46cf-8baa-9504d4100801)


## 🛠️ Tech Stack

| Layer        | Technology                |
|--------------|--------------------------|
| Backend      | Django (Python 3.x)      |
| Database     | MySQL 8.x (or Oracle 19c)|
| Frontend     | HTML5, Bootstrap, JS     |
| ORM/Drivers  | Django ORM, PyMySQL      |
| Utilities    | python-decouple, Pillow, crispy-forms, cryptography |

## 📸 Screenshots & Demo

- Login Page
![WhatsApp Image 2025-06-25 at 20 46 55_d8474547](https://github.com/user-attachments/assets/4c200536-595a-45b5-957c-b33694fbb834)

-----------------------------


- Superuser Dashboard
![WhatsApp Image 2025-06-25 at 20 48 20_b0794268](https://github.com/user-attachments/assets/5e666620-e59c-4e8d-b130-09de5d92c7a5)
-----------------------------


- Superuser master table
  ![WhatsApp Image 2025-06-25 at 20 49 37_759e15f6](https://github.com/user-attachments/assets/98595d71-b5c1-4ae7-896f-2eede74323a5)
-----------------------------


- Add new user button 
![WhatsApp Image 2025-06-25 at 20 50 18_604479bc](https://github.com/user-attachments/assets/a41c2565-f22c-4549-9ae6-c2a755d947fb)
-----------------------------


- Category
![WhatsApp Image 2025-06-25 at 20 51 43_092ccd15](https://github.com/user-attachments/assets/6f05ea8f-7757-4cb7-a431-bde9aa8cea94)
-----------------------------


- Edit button
![image](https://github.com/user-attachments/assets/727f5fa4-ced7-4624-ac20-09957d821a44)
-----------------------------


- User admin option (superuser)
![WhatsApp Image 2025-06-25 at 20 52 39_35b03b8a](https://github.com/user-attachments/assets/b6b52892-a02e-4ce3-a60b-95e040316abd)
-----------------------------


- Attendance (superuser)
![WhatsApp Image 2025-06-25 at 20 53 16_daf86222](https://github.com/user-attachments/assets/bf47d6e6-3d8c-43f7-83ad-4b4956b979ca)
-----------------------------


- Adjustments
![image](https://github.com/user-attachments/assets/ae4c2040-b97f-44b6-bc50-0935d42d508d)
-----------------------------


- Processing
![WhatsApp Image 2025-06-25 at 20 54 05_245b470d](https://github.com/user-attachments/assets/3a331f88-2dbe-458c-bc3a-8e3b568e621e)
-----------------------------


- Reports
![WhatsApp Image 2025-06-25 at 20 55 06_5e03db42](https://github.com/user-attachments/assets/6d2a1abd-b58d-46e0-a5a1-f3601f255e45)
-----------------------------


- Enquiry
![image](https://github.com/user-attachments/assets/cfed40d4-f075-4146-93a9-1697fd03fadc)
-----------------------------


- Checklist
![image](https://github.com/user-attachments/assets/b499dcdb-3698-40dd-b981-a32489860fde)
-----------------------------


- Admin dashboard
![image](https://github.com/user-attachments/assets/f1637dc2-6268-44c5-97ef-e7ca2ad215aa)
-----------------------------


- Admin user admin view
![image](https://github.com/user-attachments/assets/7dc7bea6-a7ab-4dff-b2ee-887b4c006ab4)
-----------------------------


- DNB dashboard
![image](https://github.com/user-attachments/assets/612c44bf-d44c-41f5-a6f4-748152c7b4ef)
-----------------------------


- DNB (attendance view)
![image](https://github.com/user-attachments/assets/6b2eacda-9c02-4af5-a689-1f693302c870)
-----------------------------


- CSR login page
![image](https://github.com/user-attachments/assets/3a2e20e3-614d-498f-9399-9ba6b2c5dcfd)
-----------------------------


- CSR master view
![image](https://github.com/user-attachments/assets/bfbdd81a-d63c-4160-a484-df8a7e4df293)
-----------------------------


- CSR attendance view
![image](https://github.com/user-attachments/assets/e7b66ad2-9165-44d0-8d15-7f29f35f00bf)
-----------------------------


- CONTRACTUAL dashboard
  ![image](https://github.com/user-attachments/assets/0764aea5-8a68-498a-a7c1-8eefdb4a7c1b)
-----------------------------


- CONTRACTUAL attendance view
![image](https://github.com/user-attachments/assets/71831312-e0a8-45dc-89ca-35bda47fe326)
-----------------------------


- DNB master view
![image](https://github.com/user-attachments/assets/b8680ee1-ae6a-4394-a66a-d2f5181ea16e)
-----------------------------


- DNB attendance view
![image](https://github.com/user-attachments/assets/756a641a-b0ad-4f90-bf4c-63799bce8aba)
-----------------------------



- Login page (light view)
![image](https://github.com/user-attachments/assets/6a5b31e9-60f7-4359-9382-6c01c205b588)
-----------------------------




## 📝 Detailed Features & Modules

### 1. **Authentication & Authorization**
- Secure login for all user roles.
- Session management and password security.
- Role-based dashboard and navigation.

### 2. **Employee Master**
- Add/edit/view employee records.
- Filter by category (DNB, CSR, Contractual).
- Data validation and integrity checks.

### 3. **Attendance Management**
- Enter and edit monthly attendance.
- Auto-calculate absents based on the month (supports leap years).
- Validation: sum of all days matches days in month.
- Role-based edit permissions.

### 4. **Payroll Module**
- Automated stipend and adjustment calculations.
- Tax and deduction handling.
- Payroll reports for finance/admin.

### 5. **Reporting & Compliance**
- Downloadable reports (CSV, PDF).
- Audit logs and change tracking.
- Checklist for compliance.

## 🚦 Setup & Installation Guide

### **1. Prerequisites**
- Python 3.8+
- MySQL 8.x (or Oracle 19c, if using Oracle backend)
- Git (optional)
- Visual Studio Code or any IDE

### **2. Clone the Repository**
```bash
git clone https://github.com/yourusername/dnb_pay_system.git
cd dnb_pay_system
```

### **3. Create & Activate Virtual Environment**
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate
```

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5. Database Setup**
- Create a MySQL database (e.g., `mydb`) and user (`bspadmin`/`bsp123`).
- Grant privileges:
  ```sql
  CREATE DATABASE mydb CHARACTER SET utf8mb4;
  CREATE USER 'bspadmin'@'localhost' IDENTIFIED BY 'bsp123';
  GRANT ALL PRIVILEGES ON mydb.* TO 'bspadmin'@'localhost';
  FLUSH PRIVILEGES;
  ```
- Update `settings.py`:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'mydb',
          'USER': 'bspadmin',
          'PASSWORD': 'bsp123',
          'HOST': 'localhost',
          'PORT': '3306',
      }
  }
  ```

### **6. Apply Migrations**
```bash
python manage.py migrate
```

### **7. Create Superuser (Optional)**
```bash
python manage.py createsuperuser
```

### **8. Run the Server**
```bash
python manage.py runserver
```
Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## 🔑 Default Login Credentials

| Role      | Username      | Password     |
|-----------|--------------|-------------|
| Super     | admin_dnb4    | sprint456   |
| (Or create your own using createsuperuser) |

## 🧑‍💻 Developer

- **Piyush Kumar Tiwari**

## 📚 Learnings & Impact

- Migrated a legacy system to a modern web platform.
- Implemented real-world security and authentication.
- Automated complex HR workflows and payroll calculations.
- Enhanced data integrity and reporting for compliance.

## 🏆 Acknowledgements

Special thanks to the C&IT department, Sector 9 Hospital BSP, and our mentors for their invaluable guidance.

## 📢 License

This project is for educational and organizational use at Sector 9 Hospital, BSP.  
For other use, please contact the authors.

## 🚀 Let’s Connect!

[![LinkedIn](https://img.shields.io/badge/LinkedIn://linkedin.com/in/yourprofileields.io/badge/Email-grey?izing HR, one system at a time!_**
