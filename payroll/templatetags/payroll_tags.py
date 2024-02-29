from django import template

register = template.Library()


@register.filter
def has_allowances(payrolls):
    return any(payroll.allowance for payroll in payrolls)
