from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from broker.sitemaps import AccountSitemap, HistorySitemap, WithdrawSitemap, DepositSitemap, InvestmentSitemap, MyAssetSitemap, TransferSitemap, profileSitemap, SwapSitemap  # Import blog sitemap if needed

sitemaps = {
    'static': StaticViewSitemap(),
    # 'account': AccountSitemap(),  # Example for blog sitemap
    # 'history': HistorySitemap(),
    # 'withdraw': WithdrawSitemap(),
    # 'deposit': DepositSitemap(),
    # 'investment': InvestmentSitemap(),
    # 'MyAsset': MyAssetSitemap(),
    # 'swap': SwapSitemap(),
    # 'transfer': TransferSitemap(),
    # 'profile':profileSitemap()
}

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
    path('settings/', setting, name='settings'),
    path('logout/', signout, name='logout'),
    path('process-transfer/', process_transfer, name='process_transfer'),
    path('invoice/', invoice, name='invoice'),
    path('payment_method/', paymentMethod, name='payment_method'),
    path('swap/', swap, name='swap'),
    path('process_swap/', process_swap, name='process_swap'),
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
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

# Add these patterns to your existing urlpatterns
trading_patterns = [
    path('trading-dashboard/', trading_dashboard, name='trading-dashboard'),
    path('execute-trade/', execute_trade, name='execute-trade'),
    path('close-trade/<uuid:trade_id>/', close_trade, name='close-trade'),
    path('trade-history/', get_trade_history, name='trade-history'),
    path('active-trades/', get_active_trades, name='active-trades'),
    path('save-trade-marker/', save_trade_marker, name='save-trade-marker'),
    path('get-trade-markers/', get_trade_markers, name='get-trade-markers'),
]

urlpatterns += trading_patterns