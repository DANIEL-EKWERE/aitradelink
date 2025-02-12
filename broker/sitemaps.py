import datetime
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Account, Histotry, Withdraw,Deposit, Investment, Asset,Transfer,Profile,Swap  # Import your model (change this to match your app)

class AccountSitemap(Sitemap):
    changefreq = "monthly"  # How often the content changes
    priority = 0.8  # Importance (0.0 - 1.0)
    
    def items(self):
        return Account.objects.all()  # Change to your model

    def lastmod(self, obj):
        return datetime(2024, 1, 1)  # Use the field that tracks last update
    
class HistorySitemap(Sitemap):
    changefreq = "monthly"  # How often the content changes
    priority = 0.8  # Importance (0.0 - 1.0)
    
    def items(self):
        return Histotry.objects.all()  # Change to your model

    def lastmod(self, obj):
        return datetime(2025, 1, 1)  # Use the field that tracks last update


class WithdrawSitemap(Sitemap):
    changefreq = "monthly"  # How often the content changes
    priority = 0.8  # Importance (0.0 - 1.0)
    
    def items(self):
        return Withdraw.objects.all()  # Change to your model

    def lastmod(self, obj):
        return obj.date  # Use the field that tracks last update

class DepositSitemap(Sitemap):
    changefreq = "monthly"  # How often the content changes
    priority = 0.8  # Importance (0.0 - 1.0)
    
    def items(self):
        return Deposit.objects.all()  # Change to your model

    def lastmod(self, obj):
        return obj.date  # Use the field that tracks last update
    
class InvestmentSitemap(Sitemap):
    changefreq = "monthly"  # How often the content changes
    priority = 0.8  # Importance (0.0 - 1.0)
    
    def items(self):
        return Investment.objects.all()  # Change to your model

    def lastmod(self, obj):
        return datetime(2025, 1, 1)  # Use the field that tracks last update
    

class MyAssetSitemap(Sitemap):
    changefreq = "monthly"  # How often the content changes
    priority = 0.8  # Importance (0.0 - 1.0)
    
    def items(self):
        return Asset.objects.all()  # Change to your model

    def lastmod(self, obj):
        return datetime(2025, 1, 1)  # Use the field that tracks last update
    
class TransferSitemap(Sitemap):
    changefreq = "monthly"  # How often the content changes
    priority = 0.8  # Importance (0.0 - 1.0)
    
    def items(self):
        return Transfer.objects.all()  # Change to your model

    def lastmod(self, obj):
        return obj.date  # Use the field that tracks last update
    
class profileSitemap(Sitemap):
    changefreq = "monthly"  # How often the content changes
    priority = 0.8  # Importance (0.0 - 1.0)
    
    def items(self):
        return Profile.objects.all()  # Change to your model

    def lastmod(self, obj):
        return datetime(2025,1,1)  # Use the field that tracks last update
    
class SwapSitemap(Sitemap):
    changefreq = "monthly"  # How often the content changes
    priority = 0.8  # Importance (0.0 - 1.0)
    
    def items(self):
        return Swap.objects.all()  # Change to your model

    def lastmod(self, obj):
        return obj.date  # Use the field that tracks last update
    

# Sitemap for static views (if needed)
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "yearly"

    def items(self):
        return ["portfolio:home", "portfolio:about", "portfolio:contact", "portfolio:term-of-use", "portfolio:login", "portfolio:register", "portfolio:privacy-policy"]  # Add the names of your static views

    def location(self, item):
        return reverse(item)
