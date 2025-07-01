from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee, Attendance, PayBill
from .utils import get_category_desc, is_valid_category

# --- Custom User Forms for Admin ---

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser')

# --- Employee and Other Forms ---

CATEGORY_CHOICES = [(i, str(i)) for i in range(0, 13)]  # 0 to 12 inclusive

class EmployeeForm(forms.ModelForm):
    catg = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Category (0-12)',
        help_text='DNB: 0-6, CONTRACTUAL: 7-9,13-14, CSR: 10-12'
    )

    class Meta:
        model = Employee
        fields = [
            'yymm', 'emp_id', 'name', 'dob', 'doj', 'dos', 'emp_status', 'stipend_rate', 'daily_rate',
            'sex_code', 'bank_cd', 'bank_acno', 'pan', 'catg', 'catg_desc', 'speciality',
            'trg_duration', 'stop_pay_ind', 'tuition_fee_ind', 'dnb_type'
        ]
        widgets = {
            'yymm': forms.NumberInput(attrs={'class': 'form-control'}),
            'emp_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doj': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dos': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'emp_status': forms.Select(attrs={'class': 'form-select'}),
            'stipend_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'daily_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'sex_code': forms.Select(attrs={'class': 'form-select'}, choices=[('M', 'Male'), ('F', 'Female')]),
            'bank_cd': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_acno': forms.TextInput(attrs={'class': 'form-control'}),
            'pan': forms.TextInput(attrs={'class': 'form-control'}),
            'catg_desc': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'speciality': forms.TextInput(attrs={'class': 'form-control'}),
            'trg_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'stop_pay_ind': forms.NumberInput(attrs={'class': 'form-control'}),
            'tuition_fee_ind': forms.NumberInput(attrs={'class': 'form-control'}),
            'dnb_type': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        optional_fields = ['trg_duration', 'stop_pay_ind', 'tuition_fee_ind', 'dnb_type']
        for field_name, field in self.fields.items():
            if field_name in optional_fields:
                field.required = False
            else:
                field.required = True
            if not field.widget.attrs.get('class'):
                field.widget.attrs.update({'class': 'form-control'})

    def clean_catg(self):
        value = int(self.cleaned_data['catg'])  # ChoiceField returns string
        if not is_valid_category(value):
            raise forms.ValidationError("Category must be: 0-6 (DNB), 7-9,13-14 (CONTRACTUAL), or 10-12 (CSR)")
        return value

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.catg = int(self.cleaned_data['catg'])  # Ensure integer save
        instance.catg_desc = get_category_desc(instance.catg)
        if commit:
            instance.save()
        return instance

class CombinedUserEmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Employee
        fields = [
            'emp_id', 'name', 'dob', 'doj', 'stipend_rate',
            'sex_code', 'catg', 'bank_acno', 'pan'
        ]
        widgets = {
            'emp_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'doj': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'stipend_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'sex_code': forms.Select(attrs={'class': 'form-select'}, choices=[('M', 'Male'), ('F', 'Female')]),
            'catg': forms.NumberInput(attrs={'class': 'form-control'}),
            'bank_acno': forms.TextInput(attrs={'class': 'form-control'}),
            'pan': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        exclude = []
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'yymm': forms.NumberInput(attrs={'class': 'form-control'}),
            'duty': forms.NumberInput(attrs={'class': 'form-control'}),
            'al': forms.NumberInput(attrs={'class': 'form-control'}),
            'cl': forms.NumberInput(attrs={'class': 'form-control'}),
            'abs': forms.NumberInput(attrs={'class': 'form-control'}),
            'pl': forms.NumberInput(attrs={'class': 'form-control'}),
            'ml': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
