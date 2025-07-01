from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from datetime import datetime

def get_default_yymm():
    return int(datetime.now().strftime('%y%m'))

# Cleaned up category choices: only DNB, CONTRACTUAL, CSR
CATEGORY_CHOICES = [
    ('DNB', 'DNB'),
    ('CONTRACTUAL', 'CONTRACTUAL'),
    ('CSR', 'CSR'),
]

class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    dob = models.DateField()
    doj = models.DateField()
    dos = models.DateField(null=True, blank=True)
    STATUS_CHOICES = [(1, 'Active'), (0, 'Inactive')]
    emp_status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    stipend_rate = models.IntegerField(validators=[MinValueValidator(0)])
    daily_rate = models.IntegerField(null=True, blank=True)
    sex_code = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    bank_cd = models.CharField(max_length=10, blank=True)
    bank_acno = models.CharField(max_length=17, blank=True)
    pan = models.CharField(max_length=10, blank=True)
    # Remove old CATEGORY_CHOICES and use numeric category for 'catg'
    catg = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(14)])
    catg_desc = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    speciality = models.CharField(max_length=20, blank=True)
    trg_duration = models.IntegerField(default=0)
    stop_pay_ind = models.IntegerField(default=0)
    tuition_fee_ind = models.IntegerField(default=0)
    dnb_type = models.CharField(max_length=5, blank=True)
    yymm = models.IntegerField(default=get_default_yymm)

    def save(self, *args, **kwargs):
        # Optionally, ensure daily_rate is always set
        if not self.daily_rate and self.stipend_rate:
            self.daily_rate = self.stipend_rate // 30
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.emp_id} - {self.name}"

    class Meta:
        db_table = 'dnbmast'

class Attendance(models.Model):
    yymm = models.IntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, to_field='emp_id')
    duty = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(31)], default=0)
    al = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(31)], default=0)
    cl = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(31)], default=0)
    abs = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(31)], default=0)
    pl = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(31)], default=0)
    ml = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(31)], default=0)

    def total_days(self):
        return self.duty + self.al + self.cl + self.abs + self.pl + self.ml

    def clean(self):
        if self.total_days() > 31:
            raise ValidationError('Total attendance days cannot exceed 31')

    def __str__(self):
        return f"{self.employee.name} - {self.yymm}"

    class Meta:
        db_table = 'dnbatt'
        unique_together = ('yymm', 'employee')

class PayBill(models.Model):
    yymm = models.IntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, to_field='emp_id')
    stipend = models.IntegerField(default=0)
    adj = models.IntegerField(default=0)
    itaxrec = models.IntegerField(default=0)
    cessrec = models.IntegerField(default=0)
    cessaddl = models.IntegerField(default=0)
    gpay = models.IntegerField(default=0)
    npay = models.IntegerField(default=0)
    higher_tax_ind = models.IntegerField(default=0)

    def calculate_pay(self):
        self.gpay = self.stipend + self.adj
        if self.gpay > 20000:
            self.itaxrec = int(self.gpay * 0.10)
            self.cessrec = int(self.itaxrec * 0.03)
            self.cessaddl = int(self.itaxrec * 0.01)
        self.npay = self.gpay - (self.itaxrec + self.cessrec + self.cessaddl)

    def save(self, *args, **kwargs):
        self.calculate_pay()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.yymm} - ₹{self.npay}"

    class Meta:
        db_table = 'dnbpbill'
        unique_together = ('yymm', 'employee')
