# forms.py
from django import forms
from .models import Trade, TradingPair

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['trading_pair', 'trade_type', 'amount']
        widgets = {
            'trading_pair': forms.Select(attrs={
                'class': 'form-control',
                'id': 'tradingPair'
            }),
            'trade_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'tradeType'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'tradeAmount',
                'step': '0.00000001',
                'min': '0'
            })
        }

class QuickTradeForm(forms.Form):
    TRADE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    
    symbol = forms.CharField(
        max_length=20,
        widget=forms.HiddenInput()
    )
    
    trade_type = forms.ChoiceField(
        choices=TRADE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control mb-2',
            'id': 'quickTradeType'
        })
    )
    
    amount = forms.DecimalField(
        max_digits=20,
        decimal_places=8,
        widget=forms.NumberInput(attrs={
            'class': 'form-control mb-2',
            'id': 'quickTradeAmount',
            'placeholder': 'Enter amount',
            'step': '0.00000001',
            'min': '0'
        })
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount