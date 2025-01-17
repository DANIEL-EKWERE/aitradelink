from django.contrib import admin
from porfolio.models import Subscribe
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

# class AccountInline(admin.StackedInline):
#     model = Account
#     can_delete = False
#     verbose_name = 'Account'


# class CustomizedUserAdmin (UserAdmin):
#     inlines = (AccountInline,)

admin.site.unregister(User)
admin.site.register(User,)
# admin.site.register(Account)
# admin.site.register(Dashboard)
# admin.site.register(Histotry)
# admin.site.register(Withdraw)
# admin.site.register(Deposit)
# admin.site.register(Investment)
admin.site.register(Subscribe)

