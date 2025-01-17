from django.contrib import admin
from broker.models import Account, Dashboard,Histotry,Withdraw,Deposit,Investment, myAsset, Transfer,Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name = 'Account'


class CustomizedUserAdmin (UserAdmin):
    inlines = (AccountInline,)

@admin.register(Deposit)
class AdminDeposit(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'payment_method',
        'status',
        'date',

    ]


@admin.register(Transfer)
class AdminTransfer(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'receiver_email',
        # 'confirm_payment',
        'status',
        'date',

    ]

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = [
        'user',
        'first_name',
        'last_name',
        'phone',
        'country',
        'city',
        'zip_code',
        'state',
        'bank',
        'account',
        'accname',
        'wallet_address',
        'trading_platform',
        'image'
    ]





@admin.register(myAsset)
class AdminMyAsset(admin.ModelAdmin):
    list_display = [
        'user',
        'bitcoin',
        'ethereum',
        

    ]

@admin.register(Withdraw)
class AdminWithdraw(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'wallet_Address',
        'status',
        'date',

    ]

@admin.register(Dashboard)
class AdminDashboard(admin.ModelAdmin):
    list_display = [
        'user',
        'deposit_wallet_balance',
        'interest_wallet_balance',
        'total_invest_balance',
        'total_withdraw',
        'referral_balance',
        'trading_platform',
        'date',

    ]

@admin.register(Investment)
class AdminInvestment(admin.ModelAdmin):
    list_display = [
        'user',
        'capital',
        'daily',
        'weekly',
        'monthly',

    ]
