from django.urls import path
from .views import *
# from . import api
app_name = 'broker'


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard-index'),
    path('log/', log, name='logs'),
    # path('p2p-trading/', p2p, name='p2p'),
    # path('api/create_support/', api.create_support, name='api_create_support'),
    path('transfer/', transfer, name='transfer'),
    path('deposit/', deposit, name='deposit'),
    path('invoice/<str:amount>/<str:payment_method>/', invoice, name='invoice'),
    path('market/', market, name='market'),
    path('confirm-payment/',confirm_payment, name='confirm-payment'),
    path('withdraw/', withdraw, name='withdraw'),
    path('settings/', settings, name='settings'),
    path('logout/', signout, name='logout'),
    path('process-transfer/', process_transfer, name='process_transfer'),
    path('invoice/', invoice, name='invoice'),
    path('payment_method/', paymentMethod, name='payment_method'),
    path('swap/', swap, name='swap'),
    path('profile-setting/', update_profile, name='profile-setting'),
    # path('signin/', signin, name='signin'),
    # path('signup/', signup, name='signup'),
    # path('resetpassword/', resetpassword, name='reset-password'),
    # path('contact/', contactus, name='contact'),
    # path('about/', about, name='about'),
    # path('transaction/', transaction, name='transaction'),
    # path('signout/', signout, name='sign-out'),
    # path('investment/', investment, name='investment'),
    # path('', include('broker.urls')),
]