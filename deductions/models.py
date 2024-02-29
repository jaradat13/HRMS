from django.db import models


class Deductions(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, default=None, max_digits=10)

    def __str__(self):
        return f"{self.name}-{self.amount}"
