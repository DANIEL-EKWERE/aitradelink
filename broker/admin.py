from django.contrib import admin
from broker.models import Account, Dashboard,Histotry,Withdraw,Deposit,Investment, Asset, Transfer,Profile, Swap
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import TradingPair, Trade, UserProfile, TradingSession
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





# @admin.register(MyAsset)
# class AdminMyAsset(admin.ModelAdmin):
#     list_display = [
#         'user',
#         'bitcoin',
#         'solana',
#         'usdt',
#         'ethereum',
#         'bnb',
#         'xrp',
#         'cardano',
#         'dogecoin',
#         'litecoin',
#         'usdc',
#     ]


@admin.register(Asset)
class AdminAsset(admin.ModelAdmin):
    list_display = [
        'user',
        'bitcoin',
        'solana',
        'usdt',
        'ethereum',
        'bnb',
        'xrp',
        'cardano',
        'dogecoin',
        'litecoin',
        'usdc',
    ]

@admin.register(Swap)
class AdminSwap(admin.ModelAdmin):
    list_display = [
        'user',
        'network',
        'from_token',
        'to_token',
        'amount',
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



# admin.py


@admin.register(TradingPair)
class TradingPairAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['symbol', 'name']
    list_editable = ['is_active']

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'trading_pair', 'trade_type', 'amount', 
        'entry_price', 'current_price', 'profit_loss', 'status', 'created_at'
    ]
    list_filter = ['trade_type', 'status', 'trading_pair', 'created_at']
    search_fields = ['user__username', 'trading_pair__symbol']
    readonly_fields = ['id', 'created_at', 'executed_at', 'closed_at']
    
    fieldsets = (
        ('Trade Information', {
            'fields': ('id', 'user', 'trading_pair', 'trade_type', 'status')
        }),
        ('Price Information', {
            'fields': ('amount', 'entry_price', 'current_price', 'exit_price', 'total_value', 'profit_loss')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'executed_at', 'closed_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'trading_pair')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'deposit_wallet_balance', 'trading_balance', 'total_profit_loss'
    ]
    search_fields = ['user__username', 'user__email']
    list_filter = ['user__date_joined']
    readonly_fields = ['total_profit_loss']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Balance Information', {
            'fields': ('deposit_wallet_balance', 'trading_balance', 'total_profit_loss')
        }),
    )

@admin.register(TradingSession)
class TradingSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_id', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'session_id']
    list_editable = ['is_active']