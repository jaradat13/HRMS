# Generated by Django 5.0.2 on 2024-03-02 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], default='March', max_length=20)),
                ('year', models.IntegerField(default=2024)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_closed', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('month', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_salary', models.DecimalField(decimal_places=2, default=None, max_digits=10)),
                ('gross_salary', models.DecimalField(decimal_places=2, default=None, max_digits=10)),
                ('net_salary', models.DecimalField(decimal_places=2, default=None, max_digits=10)),
                ('mobile_allowance', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('travel_allowance', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('housing_allowance', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('medical_allowance', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('uniform_allowance', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('other_allowance', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('total_allowance', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('employee_ss_deduction', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('company_ss_deduction', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('income_tax_deduction', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('other_deductions', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('employee_total_deduction', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('total_deductions', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_payroll', to='employee.employee')),
                ('pay_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.payperiod')),
            ],
        ),
    ]
