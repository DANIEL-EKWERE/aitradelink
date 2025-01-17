from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

# Create your models here.



class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    deposit_wallet_balance = models.IntegerField(default=0.0)
    interest_wallet_balance = models.IntegerField(default=0.0)
    total_invest_balance = models.IntegerField(default=0.0)
    total_deposit = models.IntegerField(default=0.0)
    total_withdraw = models.IntegerField(default=0.0)
    referral_balance = models.IntegerField(default=0.0)
    trading_platform = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Histotry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    tType = models.CharField(default="N/A", max_length=50)
    wallet_Address = models.CharField(default="N/A", max_length=100)
    status = models.CharField(max_length=50,choices=[('PENDING','PENDING'),('DECLINED','DECLINED'),('APPROVED','APPROVED')],default='PENDING')

    def __str__(self):
        return self.user.username
    

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)
    # confirm_payment = models.CharField(default='NO',max_length=100, choices=[('YES','YES'),('NO','NO')])
    payment_method = models.CharField(max_length=100,blank=True, null=True)
    status = models.CharField(default="UNDERREVIEW", max_length=50,choices=[('PENDING','PENDING'),('DECLINED','DECLINED'),('APPROVED','APPROVED'),('UNDERREVIEW','UNDERREVIEW')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)
    receiver_email = models.EmailField(max_length=254)
    status = models.CharField(default="PENDING", max_length=50,choices=[('PENDING','PENDING'),('DECLINED','DECLINED'),('APPROVED','APPROVED')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)
    wallet_Address = models.CharField(max_length=100)
    status = models.CharField(default="PENDING", max_length=50,choices=[('PENDING','PENDING'),('DECLINED','DECLINED'),('APPROVED','APPROVED')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=10, default='')
    last_name = models.CharField(max_length=10, default='')
    trading_platform = models.CharField(max_length=50,null=False,blank=False)
    phone = models.CharField(max_length=50)
    # address = models.CharField(max_length=50, default='N/A',blank=True,null=True)
    # state = models.CharField(max_length=50, default='N/A',blank=True,null=True)
    # city = models.CharField(max_length=50, default='N/A',blank=True,null=True)
    # zipcode = models.CharField(max_length=50, default='N/A',blank=True,null=True)
    # country = models.CharField(max_length=50,choices=[('COUNTRY1','COUNTRY1'),('COUNTRY2','COUNTRY2'),('COUNTRY3','COUNTRY3')])

    def __str__(self):
        return self.user.first_name


class Investment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    capital = models.CharField(max_length=50)
    daily = models.CharField(max_length=50)
    weekly = models.CharField(max_length=50)
    monthly = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    
class myAsset(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bitcoin = models.CharField(max_length=100)
    ethereum = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username