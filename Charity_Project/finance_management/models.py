from django.db import models
from donor_management.models import Donor
from project_management.models import Project

class Budget(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='project_budget') 
    total_budget = models.DecimalField(max_digits=20, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    remaining_budget = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_budget(self, amount):
        self.amount_spent += amount
        self.remaining_budget = self.total_budget - self.amount_spent
        self.save()

    def __str__(self):
        return f"Budget for {self.donor} in {self.project}"

class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('project', 'Project Expense'),
        ('administrative', 'Administrative Expense'),
        ('other', 'Other Expense'),
    ]

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses')
    description = models.TextField()
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    expense_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.expense_type.capitalize()} - {self.amount} on {self.expense_date}"


class FinancialReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    generated_on = models.DateField(auto_now_add=True)
    total_income = models.DecimalField(max_digits=20, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=20, decimal_places=2)
    net_balance = models.DecimalField(max_digits=20, decimal_places=2)
    report_pdf = models.FileField(upload_to='financial_reports/')

    def __str__(self):
        return f"{self.report_type.capitalize()} generated on {self.generated_on}"
