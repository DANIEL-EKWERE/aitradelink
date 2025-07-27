# management/commands/setup_trading.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from broker.models import TradingPair, UserProfile

class Command(BaseCommand):
    help = 'Set up initial trading data'

    def handle(self, *args, **options):
        # Create trading pairs
        trading_pairs = [
            {'symbol': 'BTCUSDT', 'name': 'Bitcoin/USDT'},
            {'symbol': 'ETHUSDT', 'name': 'Ethereum/USDT'},
            {'symbol': 'ADAUSDT', 'name': 'Cardano/USDT'},
            {'symbol': 'BNBUSDT', 'name': 'Binance Coin/USDT'},
            {'symbol': 'SOLUSDT', 'name': 'Solana/USDT'},
            {'symbol': 'XRPUSDT', 'name': 'Ripple/USDT'},
            {'symbol': 'DOGEUSDT', 'name': 'Dogecoin/USDT'},
            {'symbol': 'AVAXUSDT', 'name': 'Avalanche/USDT'},
        ]

        for pair_data in trading_pairs:
            pair, created = TradingPair.objects.get_or_create(
                symbol=pair_data['symbol'],
                defaults={'name': pair_data['name']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created trading pair: {pair.symbol}')
                )
            else:
                self.stdout.write(f'Trading pair already exists: {pair.symbol}')

        # Create user profiles for existing users who don't have one
        users_without_profile = User.objects.filter(userprofile__isnull=True)
        for user in users_without_profile:
            UserProfile.objects.create(
                user=user,
                deposit_wallet_balance=10000.00  # Give demo balance
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created profile for user: {user.username}')
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully set up trading data!')
        )