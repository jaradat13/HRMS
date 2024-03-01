from auditlog.models import LogEntry
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from deductions.models import Deductions
from socialsecurity.models import EmployeeSSPercentage
from incometax.models import IncomeTaxPercentage
from payroll.models import Payroll
from auditlog.registry import auditlog


def validate_image_size(value):
    filesize = value.size

    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError(_("The maximum file size that can be uploaded is 5MB."))


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg']  # Specify the allowed extensions

    if not ext.lower() in valid_extensions:
        raise ValidationError(_("Unsupported file extension. Only PDF, DOC, and DOCX files are allowed."))


def validate_file_size(value):
    filesize = value.size

    if filesize > 10 * 1024 * 1024:  # 10MB
        raise ValidationError(_("The maximum file size that can be uploaded is 10MB."))


class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )

    MARITAL_STATUS_CHOICES = (
        ('S', _('Single')),
        ('M', _('Married')),
        ('D', _('Divorced')),
        ('W', _('Widowed')),
    )

    DEGREE_CHOICES = (
        ('HS', _('High school')),
        ('AD', _('Associate / Diploma')),
        ('BA', _('Bachelor')),
        ('MA', _('Master')),
        ('PHD', _('Doctorate (Ph.D.)')),
    )
    NATIONALITY_CHOICES = (
        ('Jordan', _('Jordan')),
        ('USA', _('United States')),
        ('UK', _('United Kingdom')),
        # Add other nationalities as needed
    )
    EMPLOYMENT_TYPE_CHOICES = (
        ('FT', _('Full-Time')),
        ('PT', _('Part-Time')),
        ('CT', _('Contract')),
        ('INT', _('Intern')),
        ('OTH', _('Other')),
    )
    employee_id = models.BigAutoField(_('Employee ID'), primary_key=True, default=None)
    first_name = models.CharField(_('First name'), max_length=25)
    second_name = models.CharField(_('Second name'), max_length=25, blank=True, null=True)
    last_name = models.CharField(_('Last name'), max_length=25, blank=True, null=True)
    date_of_birth = models.DateField(_('Date of birth'), default=None)
    nationality = models.CharField(_('Nationality'), max_length=25, choices=NATIONALITY_CHOICES, default=None,
                                   blank=True, null=True)
    national_id_number = models.IntegerField(_('National ID Number'), unique=False, blank=True, null=True)
    id_expiry_date = models.DateField(_('ID Expiry Date'), default=None)
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES, default='', blank=False, null=False)
    marital_status = models.CharField(_('Marital status'), max_length=1, choices=MARITAL_STATUS_CHOICES, default='')
    phone_number = models.CharField(_('Phone number'), blank=False, null=False, max_length=18)
    email = models.EmailField(_('Email'), blank=False, null=False)
    address = models.CharField(_('Address'), max_length=100, blank=True, null=True)
    emergency_contact_name = models.CharField(_('Emergency contact name'), max_length=100, default=None, blank=True)
    emergency_contact_phone = models.CharField(_('Emergency contact phone'), blank=True,
                                               null=True, max_length=18)
    number_of_dependents = models.PositiveIntegerField(_('Number of dependents'), default=0, blank=True, null=True)
    department = models.ForeignKey('core.Department', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='employees')
    section = models.ForeignKey('core.Section', on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.ForeignKey('core.JobTitle', on_delete=models.SET_NULL, null=True, blank=True)
    employment_type = models.CharField(_('Employment Type'), max_length=3, choices=EMPLOYMENT_TYPE_CHOICES, null=True)
    is_department_head = models.BooleanField(_('Is Department Head'), default=False)
    hire_date = models.DateField(_('Hire date'), default=None)
    contract_expiry_date = models.DateField(_('Contract Expiry Date'), default=None, null=True, blank=True)

    is_active = models.BooleanField(_('Is active'), default=True)
    degrees = models.CharField(_('Degrees'), max_length=3, choices=DEGREE_CHOICES, null=True, blank=True)
    certifications = models.CharField(_('Certifications'), max_length=100, blank=False, null=False, default=None)
    social_security_number = models.IntegerField(_('Social security number'), blank=False, null=False)
    tax_identification_number = models.IntegerField(_('Tax identification number'), blank=True, null=True)
    bank_name = models.CharField(_('Bank name'), max_length=100, blank=True, null=True)
    bank_branch = models.CharField(_('Bank branch'), max_length=100, blank=True, null=True)
    bank_account_number = models.CharField(_('Bank account number'), max_length=100, blank=True, null=True)
    basic_salary = models.PositiveIntegerField(_('Basic salary'), null=False, blank=False, default=0)
    mobile_allowance = models.ForeignKey('allowance.MobileAllowance', related_name='employees', blank=True, null=True,
                                         on_delete=models.SET_NULL, default=None)
    housing_allowance = models.ForeignKey('allowance.HousingAllowance', related_name='employees', blank=True, null=True,
                                          on_delete=models.SET_NULL, default=None)
    travel_allowance = models.ForeignKey('allowance.TravelAllowance', related_name='employees', blank=True, null=True,
                                         on_delete=models.SET_NULL, default=None)
    uniform_allowance = models.ForeignKey('allowance.UniformAllowance', related_name='employees', blank=True, null=True,
                                          on_delete=models.SET_NULL, default=None)
    medical_allowance = models.ForeignKey('allowance.MedicalAllowance', related_name='employees', blank=True, null=True,
                                          on_delete=models.SET_NULL, default=None)
    other_allowance = models.ForeignKey('allowance.OtherAllowance', related_name='employees', blank=True, null=True,
                                        on_delete=models.SET_NULL, default=None)
    other_deductions = models.ForeignKey(Deductions, related_name='employees', blank=True, null=True,
                                         on_delete=models.SET_NULL, default=None)

    payroll = models.ForeignKey('payroll.Payroll', on_delete=models.SET_NULL, related_name='employee_payroll',
                                null=True, blank=True)
    image = models.ImageField(_('Image'), upload_to='media/employees_images/', null=True, blank=True,
                              validators=[validate_image_size], default='default.jpg')
    copy_of_id_card = models.FileField(_('Copy of ID card'), upload_to='media/ids/', null=True, blank=True,
                                       validators=[validate_file_size, validate_file_extension])
    copy_of_passport = models.FileField(_('Copy of passport'), upload_to='media/passports/', null=True, blank=True,
                                        validators=[validate_file_size, validate_file_extension])
    copy_of_degree = models.FileField(_('Copy of degree'), upload_to='media/degrees/', null=True, blank=True,
                                      validators=[validate_file_size, validate_file_extension])
    copy_of_visas = models.FileField(_('Copy of visas'), upload_to='media/visas/', null=True, blank=True,
                                     validators=[validate_file_size, validate_file_extension])

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


auditlog.register(Employee)


