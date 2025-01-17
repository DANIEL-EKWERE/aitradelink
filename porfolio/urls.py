from django.urls import path
from .views import *
# from . import api
app_name = 'portfolio'


urlpatterns = [
    path('', index, name='home'),
    path('term-of-use/', termOfUse, name='term-of-use'),
    path('about/', about, name='about'),
    # path('api/create_support/', api.create_support, name='api_create_support'),
    path('privacy-policy/', privacyPolicy, name='privacy-policy'),
    path('watch/', watch, name='watch'),
    # path('profile/', profile, name='profile'),
    # path('deposit/', deposit, name='deposit'),
    # path('depositcrypto/', depositcrypto, name='deposit-crypto'),
    # path('withdraw/', withdraw, name='withdraw'),
    # path('withdrawcrypto/', withdrawcrypto, name='withdraw-crypto'),
    # path('plans/', plans, name='plans'),
    # path('subscribe/', subscribe, name='subscribe'),
    path('signin/', signin, name='login'),
    path('contact/', contact, name='contact'),
    path('features/', features, name='features'),
    path('signup/', signup, name='register'),
    path('subscribe/', subscribe, name='subscribe'),
    path('forgotpassword/', forgotpassword, name='forgot-password'),
    # path('contact/', contactus, name='contact'),
    # path('about/', about, name='about'),
    # path('transaction/', transaction, name='transaction'),
    # path('signout/', signout, name='sign-out'),
    # path('investment/', investment, name='investment'),
    # path('', include('broker.urls')),
]