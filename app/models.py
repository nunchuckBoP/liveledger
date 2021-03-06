from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.db.models import Sum
import decimal
import datetime

class Ledger(models.Model):
    objects = models.Manager()
    created_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, 'shared_users', blank=True)
    description = models.CharField(max_length=182)

    @property
    def balance(self):
        # adds all of the ledger items up for the ledger
        # and calculates the balance
        #items = LedgerItem.objects.filter(ledger=self)
        #total = 0.0
        #for i in items:
        #    total = total + i.get_amount
        #return total

        # get the deducted totals
        withdrawl_total = LedgerItem.objects.filter(ledger=self).filter(income=False).aggregate(Sum('amount'))
        if withdrawl_total['amount__sum'] is None:
            withdrawl_total['amount__sum'] = decimal.Decimal(0.0)

        # gets the addition totals
        deposit_total = LedgerItem.objects.filter(ledger=self).filter(income=True).aggregate(Sum('amount'))
        if deposit_total['amount__sum'] is None:
            deposit_total['amount__sum'] = decimal.Decimal(0.0)
        
        # returns the additions minus the deductions
        return round(deposit_total['amount__sum'] - withdrawl_total['amount__sum'], 2)

    def __str__(self):  
        return self.description

class LedgerItem(models.Model):
    objects = models.Manager()
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=182, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    income = models.BooleanField()
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    @property
    def get_amount(self):
        if self.income:
            return self.amount
        else:
            return -1 * self.amount

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def __str__(self):
        return "description: %s, Amount: %s" % (self.description, self.get_amount)