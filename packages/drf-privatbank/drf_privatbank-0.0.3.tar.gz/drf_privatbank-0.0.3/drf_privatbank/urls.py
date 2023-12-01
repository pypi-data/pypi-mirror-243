from django.urls import path
from .views import (
    PrivatBankView,
    PrivatBankInfo,
    BalancePrivatView,
    StatementPrivatView,
    PaymentPrivatView,
    PrivatBankCurrencyCashRate,
    PrivatBankCurrencyNonCashRate,
)

app_name = 'drf_privatbank'


urlpatterns = [
    path('', PrivatBankView.as_view()),
    path(
        'currency/cash_rate/', 
        PrivatBankCurrencyCashRate.as_view(), name='privat_currency_cash_rate_list'
    ),
    path(
        'currency/non_cash_rate/', 
        PrivatBankCurrencyNonCashRate.as_view(), name='privat_currency_non_cash_rate_list'
    ),
    path(
        'info/', 
        PrivatBankInfo.as_view(), name='privat_info_detail'
    ),
    path(
        'balance/', 
        BalancePrivatView.as_view(), name='privat_balance_detail'
    ),
    path(
        'statement/',
        StatementPrivatView.as_view(), name='privat_statement_list'
    ),
    path(
        'payment/',
        PaymentPrivatView.as_view(), name='privat_payment_create'
    ),
]
