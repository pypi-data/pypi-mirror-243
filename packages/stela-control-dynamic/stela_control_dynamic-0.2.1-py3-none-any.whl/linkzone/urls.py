from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
from linkzone import stripe_webhook

app_name="linkzone"

urlpatterns = [
    #emmerutpay
    path('requests/', views.request, name="request"),
    path('login-denied/', views.loginCheckout,  name="login-check"),
    path('cart/values', views.cartValues, name="cartvalues"),
    path('billings/payments/tdd-payment/', views.intentExpress, name="stripe_express"),
    path('billing/payload/<int:reciptid>/<int:orderid>', views.billingPayLoader, name="bill_payload"),
    path('mercantil-payment/', views.mercantilPayments, name="mercantil_payment"),
    path('payment-paypal', views.paymentPaypal, name="paypal"),
    path('stripe_payment/', views.paymentStripe, name="stripe_payment"),
    path('webhook/payments/', stripe_webhook.stripePayment, name="webhook_payment"),
    path('payment/', views.paymentLoader, name="payment_loader"),

]