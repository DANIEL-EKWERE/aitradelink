# Generated by Django 5.1.3 on 2025-02-06 11:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=10)),
                ('last_name', models.CharField(default='', max_length=10)),
                ('trading_platform', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit_wallet_balance', models.IntegerField(default=0.0)),
                ('interest_wallet_balance', models.IntegerField(default=0.0)),
                ('total_invest_balance', models.IntegerField(default=0.0)),
                ('total_deposit', models.IntegerField(default=0.0)),
                ('total_withdraw', models.IntegerField(default=0.0)),
                ('referral_balance', models.IntegerField(default=0.0)),
                ('trading_platform', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=50)),
                ('payment_method', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('DECLINED', 'DECLINED'), ('APPROVED', 'APPROVED'), ('UNDERREVIEW', 'UNDERREVIEW')], default='UNDERREVIEW', max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Histotry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now_add=True)),
                ('tType', models.CharField(default='N/A', max_length=50)),
                ('wallet_Address', models.CharField(default='N/A', max_length=100)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('DECLINED', 'DECLINED'), ('APPROVED', 'APPROVED')], default='PENDING', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capital', models.CharField(max_length=50)),
                ('daily', models.CharField(max_length=50)),
                ('weekly', models.CharField(max_length=50)),
                ('monthly', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bitcoin', models.CharField(max_length=100)),
                ('solana', models.CharField(max_length=100)),
                ('usdt', models.CharField(max_length=100)),
                ('ethereum', models.CharField(default=0, max_length=100)),
                ('bnb', models.CharField(default=0, max_length=100)),
                ('xrp', models.CharField(default=0, max_length=100)),
                ('cardano', models.CharField(default=0, max_length=100)),
                ('dogecoin', models.CharField(default=0, max_length=100)),
                ('litecoin', models.CharField(default=0, max_length=100)),
                ('usdc', models.CharField(default=0, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('bank', models.CharField(blank=True, max_length=100, null=True)),
                ('account', models.CharField(blank=True, max_length=20, null=True)),
                ('accname', models.CharField(blank=True, max_length=100, null=True)),
                ('wallet_address', models.CharField(blank=True, max_length=100, null=True)),
                ('trading_platform', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Swap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.CharField(max_length=100)),
                ('from_token', models.CharField(max_length=100)),
                ('to_token', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=50)),
                ('receiver_email', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('DECLINED', 'DECLINED'), ('APPROVED', 'APPROVED')], default='PENDING', max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=50)),
                ('wallet_Address', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('DECLINED', 'DECLINED'), ('APPROVED', 'APPROVED')], default='PENDING', max_length=50)),
                ('method', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
