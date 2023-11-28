from django.urls import path
from .views import (
    MonoView,
    CurrencyView,
    ClientInfoView,
    BalanceView,
    StatementView,
    CreateWebhook,
)

app_name = 'monobank'

urlpatterns = [
    path('', MonoView.as_view()),
    path(
        'currency/',
        CurrencyView.as_view(), name='currency_detail'
    ),
    path(
        'client-info/',
        ClientInfoView.as_view(), name='mono_client_info_detail'
    ),
    path(
        'balance/', 
        BalanceView.as_view(), name='mono_balance_detail'
    ),
    path(
        'statement/',
        StatementView.as_view(), name='mono_statement_list'
    ),
    path(
        'webhook/',
        CreateWebhook.as_view(), name='webhook_create'
    ), 
]
