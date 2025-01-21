from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.views import PasswordResetView
from .views import *
# from . import api
app_name = 'portfolio'

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'forgot-password.html'



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


     # Password reset views
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    
    # Password reset views
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]