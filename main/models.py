from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.urls import reverse

from main.utils import h_encode
# Create your models here.


class Donor(models.Model):

    Date = models.DateField(auto_now=False)
    # models.IntegerField(validators=[MaxValueValidator(3000),MinValueValidator(2000)])
    Financial_Year = models.IntegerField()

    choice1 = [('DB', 'Debit'), ('CR', 'Credit'), ('NA', 'N/A')]

    Type = models.CharField(max_length=2, choices=choice1)  # default = 'NA'
    Amount = models.DecimalField(max_digits=100, decimal_places=2)
    Cheque_Number = models.BigIntegerField()
    From_To = models.CharField(max_length=200)
    Name = models.CharField(max_length=50)
    On_Account_Of = models.CharField(max_length=200)
    Country = models.CharField(max_length=20)
    Remarks = models.CharField(max_length=200)
    Email = models.EmailField(max_length=254)
    Phone_Number = models.BigIntegerField()

    status_choice = [('RU', 'Receipt Unavailable'),
                     ('RG', 'Receipt Generated')]
    Status = models.CharField(max_length=2, choices=status_choice)

    Action = models.BooleanField(default=True)

    Token = models.CharField(max_length=7)

    def get_hashid(self):
        return h_encode(self.id)

    def get_absolute_url(self):
        return reverse("record", args=[self.id])
