from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from decimal import Decimal
import uuid

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
    status = models.CharField(default="UNDERREVIEW", max_length=50,choices=[('PENDING','PENDING'),('DECLINED','DECLINED'),('APPROVED','APPROVED'),('UNDERREVIEW','UNDERREVIEW'),('PAID','PAID')])
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
    status = models.CharField(default="PENDING", max_length=50,choices=[('PENDING','PENDING'),('DECLINED','DECLINED'),('APPROVED','APPROVED'),('PAID','PAID')])
    method = models.CharField(max_length=50, blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    account = models.CharField(max_length=20, blank=True, null=True)
    accname = models.CharField(max_length=100, blank=True, null=True)
    wallet_address = models.CharField(max_length=100, blank=True, null=True)
    trading_platform = models.CharField(max_length=50,null=True,blank=True)
    image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"




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
    
# class MyAsset(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bitcoin = models.CharField(max_length=100)
#     solana = models.CharField(max_length=100)
#     usdt = models.CharField(max_length=100)
#     ethereum = models.CharField(max_length=100,default=0)
#     bnb = models.CharField(max_length=100,default=0)
#     xrp = models.CharField(max_length=100,default=0)
#     cardano = models.CharField(max_length=100,default=0)
#     dogecoin = models.CharField(max_length=100,default=0)
#     litecoin = models.CharField(max_length=100,default=0)
#     usdc = models.CharField(max_length=100,default=0)

#     def __str__(self):
#         return self.user.username
    

class Asset(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bitcoin = models.IntegerField()
    solana = models.IntegerField()
    usdt = models.IntegerField()
    ethereum = models.IntegerField()
    bnb = models.IntegerField()
    xrp = models.IntegerField()
    cardano = models.IntegerField()
    dogecoin = models.IntegerField()
    litecoin = models.IntegerField()
    usdc = models.IntegerField()

    def __str__(self):
        return self.user.username
    
class Swap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    network = models.CharField(max_length=100)
    from_token = models.CharField(max_length=100)
    to_token = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.user.username
    


'''
trading codes here
'''


# models.py


class TradingPair(models.Model):
    symbol = models.CharField(max_length=20, unique=True)  # e.g., 'BTCUSDT'
    name = models.CharField(max_length=100)  # e.g., 'Bitcoin/USDT'
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.symbol

class Trade(models.Model):
    TRADE_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('EXECUTED', 'Executed'),
        ('CANCELLED', 'Cancelled'),
        ('CLOSED', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    amount = models.DecimalField(max_digits=20, decimal_places=8)  # Amount in base currency
    entry_price = models.DecimalField(max_digits=20, decimal_places=8)
    current_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    exit_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    total_value = models.DecimalField(max_digits=20, decimal_places=8)  # amount * entry_price
    profit_loss = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.trade_type} {self.amount} {self.trading_pair.symbol}"
    
    def calculate_profit_loss(self):
        """Calculate profit/loss based on current price"""
        if self.current_price and self.status == 'EXECUTED':
            if self.trade_type == 'BUY':
                self.profit_loss = (Decimal(str(self.current_price)) - self.entry_price) * self.amount
            else:  # SELL
                self.profit_loss = (self.entry_price - self.current_price) * self.amount
            self.save()
    
    def close_trade(self, exit_price):
        """Close the trade with given exit price"""
        self.exit_price = exit_price
        self.current_price = exit_price
        self.status = 'CLOSED'
        self.closed_at = timezone.now()
        
        if self.trade_type == 'BUY':
            self.profit_loss = (exit_price - self.entry_price) * self.amount
        else:  # SELL
            self.profit_loss = (self.entry_price - exit_price) * self.amount
        
        # Update user balance
        user_profile = UserProfile.objects.get(user=self.user)
        user_profile.deposit_wallet_balance += self.profit_loss
        user_profile.save()
        
        self.save()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    deposit_wallet_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    trading_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_profit_loss = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.user.username} - Balance: ${self.deposit_wallet_balance}"

class TradingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Session {self.session_id}"
