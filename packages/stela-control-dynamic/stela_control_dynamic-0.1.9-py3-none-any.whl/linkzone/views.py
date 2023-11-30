import json
from django.db.models import Sum
from .context_processors import Cart
import stripe
import os
from datetime import timedelta
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from paypalcheckoutsdk.orders import OrdersGetRequest
from accounts.forms import LoginForm
from django.contrib.auth import login, logout, authenticate, logout
import http.client
from decimal import Decimal
from mercantil_cypher.mercantil_aes import AESCipher
from cloud.models import (
    Domains, VirtualCloud, ZoneDNS, CloudStorage, ResquetsCloud, UsageCloud
    )
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
import urllib.request
from django.conf import settings
from django.shortcuts import redirect, render
from accounts.models import UserBase
from stela_control.models import (
    Content, Order, StelaSelection, 
    StelaItems, ControlFacturacion, FacturaItems, StelaPayments, 
    PathControl, BillingRecipt, TemplateSections,
    DataEmail, DynamicBullets, OrderItems, ItemServices, Modules, Support, 
    ChatSupport, SupportResponse, SitePolicy, Customer, Addresses,
    Notifications, PaypalClient, Comments, SiteViews
    )
from geolocation.models import Country, City
from stela_control.forms import (
    NewsletterForm, SupportForm, ReadOnlySupportFormCostumer,
    )
from django.contrib import messages
from accounts.forms import UserEditForm
import requests
from django.forms import Textarea, inlineformset_factory
import datetime
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from stela_control.models import InvoiceControl, SiteControl
from django.template.loader import render_to_string, get_template
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AddressForm, CommentForm, ContactForm
from google.oauth2 import service_account
from google.cloud import monitoring_v3

# Create your views here.
def home(request):
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
    ip = user_ip.split(',')[0] 
    res = requests.get('http://ip-api.com/json/' + ip)
    data_one = res.text
    data = json.loads(data_one)
    print(data)
    form=ContactForm()
    form2=NewsletterForm()
    lang = request.LANGUAGE_CODE
    mainabout=Content.objects.filter(tag="Emmerut About Main", status="Publish", lang=lang)
    secondaryabout=Content.objects.filter(tag="Emmerut About Secondary", status="Publish", lang=lang)
    cloudservices=Content.objects.filter(tag="Emmerut Cloud Services", status="Publish", lang=lang)
    stelacontrol=Content.objects.filter(tag="Stela Control Dynamic", status="Publish", lang=lang)
    projects=Content.objects.filter(tag="Emmerut Projects", status="Publish", lang=lang)
    store=Content.objects.filter(tag="Emmerut Store", status="Publish", lang=lang)
    mainpost=Content.objects.filter(tag="Emmerut Blogs", status="Publish", lang=lang).order_by('created').last()
    posts=Content.objects.filter(tag="Emmerut Blogs", status="Publish", lang=lang).order_by('-created')[1:4]
    try:
        bulletabout=DynamicBullets.objects.filter(parent__tag="Emmerut About Secondary", parent__lang=lang)
        bullet1=bulletabout[0]
        bullet2=bulletabout[1]
        bullet3=bulletabout[2]
    except:
        bulletabout=None
        bullet1=None
        bullet2=None
        bullet3=None
    context = {
        'form':form,
        'newsletter':form2,
        'mainabout': mainabout,
        'about2':secondaryabout,
        'cloudservices': cloudservices,
        'stelacontrol': stelacontrol,
        'store': store,
        'projects': projects,
        'mainpost': mainpost,
        'posts': posts,
        'skill': bullet1,
        'skill2': bullet2,
        'skill3': bullet3
    }

    if request.method == 'POST':
        
        form_id = request.POST.get('form-id')
        print(form_id)

        if form_id == "contact":
            user_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
            ip = user_ip.split(',')[0] 
            form = ContactForm(request.POST)
            if form.is_valid():
                subject=form.cleaned_data['subject']
                message=form.cleaned_data['message']
                req=form.save(commit=False)
                req.host=ip
                req.save()

                html_content = render_to_string('stela_control/emails-template/contact/message_notification.html', {
                        'message': message,
                        'subject': subject        
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            subject,
                            text_content,
                            settings.STELA_EMAIL,
                            [settings.MAIN_EMAIL]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()

                messages.success(request, _("Your message has been sent"))
                return HttpResponseRedirect(reverse('linkzone:home'))
        
        if form_id == "newsletter":
            email=request.POST.get('email')
            if DataEmail.objects.filter(email=email).exists():
                messages.warning(request, _("This email is already registered"))
                return HttpResponseRedirect(reverse('linkzone:home'))
            else:
                form = NewsletterForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, _("Now you are subscribed"))
                    return HttpResponseRedirect(reverse('linkzone:home'))
                
    return render(request, 'index.html', context)

@login_required
def console(request):
    billing = InvoiceControl.objects.filter(recipt__customer__email=request.user.email, recipt__status="Pending")
    user = request.user
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
    ip = user_ip.split(',')[0] 
    alert = Notifications.objects.filter(user=user).order_by('-created')[:10]
    count = Notifications.objects.filter(user=user, status="No Read").count()
    # news = Lobby.objects.filter(status="Publish").order_by('-created')[:3]
    res = requests.get('http://ip-api.com/json/' + ip)
    data_one = res.text
    data = json.loads(data_one)
    # city = str(data['city'])

    # source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&appid=396f43747b3afe4607d17f52965a1f98').read()
    # list_of_data = json.loads(source)

    # temp_data = {
    #         "country_code": str(list_of_data['sys']['country']),
    #         "coordinate": str(list_of_data['coord']['lon']) + ', '
    #         + str(list_of_data['coord']['lat']),

    #         "temp": str(list_of_data['main']['temp']) + ' °C',
    #         "pressure": str(list_of_data['main']['pressure']),
    #         "humidity": str(list_of_data['main']['humidity']),
    #         'main': str(list_of_data['weather'][0]['main']),
    #         'description': str(list_of_data['weather'][0]['description']),
    #         'icon': list_of_data['weather'][0]['icon'],
    #     }

    context ={
       'billings': billing,
       'data': data,
    #    'temp': temp_data,
    #   'news': news,
       'alerts': alert,
       'count': count
    }

    return render(request, 'linkzone/index.html', context)

def request(request):

    if request.POST.get('action') == 'restart':
        key = request.POST.get('key')
        object = StelaSelection.objects.get(validator=key, status="Checked")
        object.delete()
    
        response = JsonResponse({'success': 'return something'})
        return response
    
    if request.POST.get('action') == 'cart':
        cart = Cart(request)
        amount = request.POST.get('amount')
        select_id = str(request.POST.get('selectid'))
       
        cart.service_add(selectid=select_id)
        cart_count = cart.__len__()

        StelaSelection.objects.filter(pk=select_id).update(
            amount=amount,
            status="Cart"
            )

        response = JsonResponse({'count':cart_count})
        return response
    
    if request.POST.get('action') == 'removeCart':
        cart = Cart(request)
        item = request.POST.get('item')
        object = StelaSelection.objects.get(pk=item)
        object.delete()
        cart.stela_del(obj=item)

        response = JsonResponse({'success': 'return something'})
        return response

    if request.POST.get('action') == 'alertDown':
        user=request.user
        Notifications.objects.filter(user=user, status="No Read").update(status="Readed")
        count = Notifications.objects.filter(user=user, status="No Read").count()

        response = JsonResponse({'count': count})
        return response

    if request.POST.get('action') == 'cleanAlerts':
        user=request.user
        objs=Notifications.objects.filter(user=user).delete()
        

        response = JsonResponse({'objs': objs})
        return response

        
def stelaCheck(request, value):
    selection = StelaSelection.objects.get(validator=value, status="Checked")
    domain = Domains.objects.get(name=selection.domain.name, tld=selection.domain.tld)
    total_integration = StelaSelection.objects.filter(domain=domain, status="Checked").aggregate(total=(Sum('integration__price')))
    total_modules = StelaItems.objects.filter(parent__domain=domain, parent__status="Checked").aggregate(total=(Sum('amount')))
    
    if domain.tld == "com":
        
        if  total_modules['total']:
            total = total_integration['total'] + total_modules['total']
            calc=round(total*Decimal(0.5), 2)
            initpay=round(total-calc, 2)
        else:
            total = total_integration['total']
            calc=round(total*Decimal(0.5), 2)
            initpay=round(total-calc, 2)
    else:

        if  total_modules['total']:
            total = total_integration['total'] + total_modules['total'] + domain.price
            calc=round(total*Decimal(0.5), 2)
            initpay=round(total-calc, 2)
        else:
            total = total_integration['total'] + domain.price
            calc=round(total*Decimal(0.5), 2)
            initpay=round(total-calc, 2)
        
        

    context = {
        'select': selection,
        'initpay':calc,
        'total': total
    }
    return render(request, 'linkzone/costumer/payments/check.html', context)

def cartValues(request):
    cart = Cart(request)
    amount=cart.import_total()
    return JsonResponse({'amount': amount})

def loginCheckout(request): 
    form = LoginForm()
    msg = ""

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request,user)
                    return redirect('/stela/checkout')
                else:
                    msg = 'credenciales invalidas'

            else:
                msg = 'credenciales invalidas'

        else: 
            msg = 'error validando usuario'


    return render(request, 'linkzone/costumer/payments/checkout.html', {
                    'call': 'stela',
                    'form': form,
                    'msg': msg
                    })

def checkoutStela(request):
    lang=request.LANGUAGE_CODE
    form = LoginForm()
    msg = ""
    if lang=="es-ve":
        vcost = Modules.objects.get(title="Uso de la instancia de la nube (Horas)", parent__title="Stela Cloud Services", parent__lang=lang)
        cscost = Modules.objects.get(title="Uso de almacenamiento en la nube (GB de datos)", parent__title="Stela Cloud Services", parent__lang=lang)
        reqcost= Modules.objects.get(title="Solicitudes de contenido en la nube", parent__title="Stela Cloud Services", parent__lang=lang)
        dnscost = Modules.objects.get(title="Costo Orbit Zona DNS", parent__title="Stela Cloud Services", parent__lang=lang)
    else:
        vcost= Modules.objects.get(title="Cloud Instance Usage (Hours)", parent__title="Stela Cloud Services", parent__lang=lang)
        cscost= Modules.objects.get(title="Cloud Storage Usage (GB Data)", parent__title="Stela Cloud Services", parent__lang=lang)
        reqcost= Modules.objects.get(title="Cloud Content Requests", parent__title="Stela Cloud Services", parent__lang=lang)
        dnscost= Modules.objects.get(title="Zone DNS Orbit Cost", parent__title="Stela Cloud Services", parent__lang=lang)
    
    if request.method == 'POST' and 'loginform' in request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request,user)
                    return redirect('/stela/checkout')
                else:
                    msg = 'credenciales invalidas'

                    return render(request, 'linkzone/costumer/payments/checkout.html', {
                    'call': 'stela',
                    'form': form,
                    })
            else:
                msg = 'credenciales invalidas'

                return render(request, 'linkzone/costumer/payments/checkout.html', {
                'call': 'stela',
                'form': form,
                'messages': msg
            })

        else: 
            msg = 'error validando usuario'

            return render(request, 'linkzone/costumer/payments/checkout.html', {
                'call': 'stela',
                'form': form,
                'messages': msg
            })
    
    context ={
        'form': form,
        'call': 'stela',
        'messages': msg,
        'cost1': vcost.price,
        'cost2': cscost.price,
        'cost3': reqcost.price,
        'cost4': dnscost.price
    }
    return render(request, 'linkzone/costumer/payments/checkout.html', context)

def checkout(request, reciptid, orderid):
    lang=request.LANGUAGE_CODE
    form = LoginForm()
    msg = ""
    if lang=="es-ve":
        vcost = Modules.objects.get(title="Uso de la instancia de la nube (Horas)", parent__title="Stela Cloud Services", parent__lang=lang)
        cscost = Modules.objects.get(title="Uso de almacenamiento en la nube (GB de datos)", parent__title="Stela Cloud Services", parent__lang=lang)
        reqcost= Modules.objects.get(title="Solicitudes de contenido en la nube", parent__title="Stela Cloud Services", parent__lang=lang)
        dnscost = Modules.objects.get(title="Costo Orbit Zona DNS", parent__title="Stela Cloud Services", parent__lang=lang)
    else:
        vcost= Modules.objects.get(title="Cloud Instance Usage (Hours)", parent__title="Stela Cloud Services", parent__lang=lang)
        cscost= Modules.objects.get(title="Cloud Storage Usage (GB Data)", parent__title="Stela Cloud Services", parent__lang=lang)
        reqcost= Modules.objects.get(title="Cloud Content Requests", parent__title="Stela Cloud Services", parent__lang=lang)
        dnscost= Modules.objects.get(title="Zone DNS Orbit Cost", parent__title="Stela Cloud Services", parent__lang=lang)

    if request.method == 'POST' and 'loginform' in request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request,user)
                    return redirect('/stela/checkout')
                else:
                    msg = 'credenciales invalidas'

                    return render(request, 'linkzone/costumer/payments/checkout.html', {
                    'call': 'stela',
                    'form': form,
                    })
            else:
                msg = 'credenciales invalidas'

                return render(request, 'linkzone/costumer/payments/checkout.html', {
                'call': 'stela',
                'form': form,
                'messages': msg
            })

        else: 
            msg = 'error validando usuario'

            return render(request, 'linkzone/costumer/payments/checkout.html', {
                'call': 'stela',
                'form': form,
                'messages': msg
            })
    
    url = settings.VES_MONITOR
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        currency=Decimal(data['USD']['promedio_real'])
    else:
        currency=Decimal(24.48)
        
    headers = {
            'X-IBM-Client-Id': settings.MERCANTIL_CLIENT_ID,
            'content-type': "application/json",
            'accept': "application/json"
            }
    MERCHANT_ID = settings.MERCANTIL_MERCHANT_ID
    TERMINAL_ID = settings.MERCANTIL_TERMINAL_ID
    conn = http.client.HTTPSConnection("apimbu.mercantilbanco.com")
    code_country="58" 
    # Client information
    CLIENT_IP = "10.0.0.1"
    CLIENT_BROWSER = "Chrome 18.1.3"
    key = b'A11103402525120190822HB01'
    cipher = AESCipher(key)

    user = request.user
    order=Order.objects.filter(pk=orderid)
    order_id=orderid
    invoice = BillingRecipt.objects.get(pk=reciptid)
    orderitems=OrderItems.objects.get(order_id=orderid)
    getimport=invoice.amount + invoice.tax
    payment_fee = getimport * Decimal(0.02)
    profit = invoice.amount * Decimal(0.25)
    total_paid = invoice.amount + invoice.tax + payment_fee

    get_control_number=BillingRecipt.objects.filter(is_generated=True, is_budget=False, payment_option="USD",).count()
    control_number = get_control_number + 1
    invoice_number = "DB"+"-"+"0"+str(control_number)


    base = round(invoice.amount * currency, 2)
    iva = round(invoice.tax * currency, 2)
    itotal = base + iva
    fee_ves = round(itotal * Decimal(0.07), 2)

    if invoice.discount:
        descuento = round(invoice.discount * currency, 2)
        total_ves = round(base + iva + fee_ves - descuento, 2)
        calc= invoice.amount + invoice.tax
        fee = round(calc * Decimal(0.07), 2)
        total_amount = invoice.amount + invoice.tax + fee - invoice.discount
    else:
        total_ves = round(base + iva + fee_ves, 2)
        calc2 = invoice.amount + invoice.tax
        fee = round(calc2 * Decimal(0.07), 2)
        total_amount = invoice.amount + invoice.tax + fee
        descuento = ""
    
    context={
        'form': form,
        'call': 'FinalPayment',
        'messages': msg,
        'inv': invoice,
        'total': total_amount,
        'base': base,
        'iva': iva,
        'fee': fee,
        'ves_fee': fee_ves,
        'descuento': descuento,
        'total_ves': total_ves,
        'oi': orderitems,
        'cost1': vcost.price,
        'cost2': cscost.price,
        'cost3': reqcost.price,
        'cost4': dnscost.price
    }   

    if request.method == 'POST':
    
        action = request.POST.get('action')
        print(action)
        
        if request.POST.get('action') == "paypal":
            PPClient = PaypalClient()
            data = request.POST.get('orderID')
            requestorder = OrdersGetRequest(data)
            response = PPClient.client.execute(requestorder)
            get_code = str('PP')+get_random_string(8).upper()
            if total_amount == response.result.purchase_units[0].amount.value:
                try:
                    order.update(status="Completed")

                    BillingRecipt.objects.filter(pk=invoice.pk).update(status="Payeed", payment_option="USD")
                    
                    StelaPayments.objects.create (
                                user=invoice.owner,
                                billing=order_id,
                                key_validator=response.result.id,
                                transaction_id=get_code,
                                payment_option='Paypal',
                                subtotal=invoice.amount,
                                taxes=invoice.tax,
                                profit=profit,
                                payment_fee=payment_fee,
                                total_paid=response.result.purchase_units[0].amount.value,
                                host=_("Final Stela Websites")
                            )
                    control_invoice = InvoiceControl.objects.filter(recipt=invoice)
                    control_invoice.update(control_id=invoice_number)
                    recipt = InvoiceControl.objects.get(recipt=invoice)

                    for select in orderitems:
                        selection=StelaSelection.objects.filter(pk=select.stela_selection.pk)
                        counter=StelaSelection.objects.filter(pk=select.stela_selection.pk).count()
                        
                    html_content = render_to_string('stela_control/emails-template/orders/stela_order_placed2.html', {
                        'order': order,
                        'subtotal': invoice.amount,
                        'tax': invoice.tax,
                        'fee': payment_fee,
                        'total': response.result.purchase_units[0].amount.value,
                        'count': counter,
                        'selection': selection 
                        })

                    text_content = strip_tags(html_content)
                    
                    email = EmailMultiAlternatives(
                            _('Payment Complete Successfully'),
                            text_content,
                            invoice.owner.email_sender,
                            [invoice.customer.email]
                                            
                        )
                    email.attach_alternative(html_content, "text/html")
                    email.send()

                    message = render_to_string('stela_control/emails-template/payments/sale_notification.html',{
                            
                    })

                    text_render = strip_tags(message)

                    email = EmailMultiAlternatives(
                            _('Billing Payment Made'),
                            text_render,
                            settings.STELA_EMAIL,
                            [settings.DEFAULT_EMAIL]
                                            
                        )
                    email.attach_alternative(message, "text/html")
                    email.send()

                    return JsonResponse({'success': _('Thanks for your purchase')})
                
                except Exception as e:
                    print(e)
                    return JsonResponse({'failed': _('Payment Failed')})
            else:
                #captar datos servidor notificar email
                # lon = str(data['lon'])
                # lat = str(data['lat'])
                # SiteControl.objects.create(
                #     ip=ip,
                #     lon=lon,
                #     lat=lat,
                #     pishing=True
                # )
                return JsonResponse({'failed': _('Amount Verification Failed')})
                
        
        if request.POST.get('action') == "tdd-pay":
            get_code = str('Epay')+get_random_string(8).upper()
            order_key = request.POST.get('order_key')
            order.update(status="Completed")
            BillingRecipt.objects.filter(pk=invoice.pk).update(status="Payeed", payment_option="USD")
                
            StelaPayments.objects.create (
                            user=invoice.owner,
                            billing=order_id,
                            key_validator=order_key,
                            transaction_id=get_code,
                            payment_option='Debit Card',
                            subtotal=invoice.amount,
                            taxes=invoice.tax,
                            profit=profit,
                            payment_fee=payment_fee,
                            total_paid=total_paid,
                            host=_("Stela Business App")
                        )
            control_invoice = InvoiceControl.objects.filter(recipt=invoice)
            control_invoice.update(control_id=invoice_number)
            recipt = InvoiceControl.objects.get(recipt=invoice)

            for select in orderitems:
                selection=StelaSelection.objects.filter(pk=select.stela_selection.pk)
                counter=StelaSelection.objects.filter(pk=select.stela_selection.pk).count()
                        
                html_content = render_to_string('stela_control/emails-template/orders/stela_order_placed2.html', {
                    'order': order,
                    'subtotal': invoice.amount,
                    'tax': invoice.tax,
                    'fee': payment_fee,
                    'total': total_paid,
                    'count': counter,
                    'selection': selection 
                    })

                text_content = strip_tags(html_content)
                    
                email = EmailMultiAlternatives(
                        _('Payment Complete Successfully'),
                        text_content,
                        invoice.owner.email_sender,
                        [invoice.customer.email]
                                        
                    )
                email.attach_alternative(html_content, "text/html")
                email.send()

                message = render_to_string('stela_control/emails-template/payments/sale_notification.html',{
                            
                })

                text_render = strip_tags(message)

                email = EmailMultiAlternatives(
                        _('Billing Payment Made'),
                        text_render,
                        settings.STELA_EMAIL,
                        [settings.DEFAULT_EMAIL]
                                        
                    )
                email.attach_alternative(message, "text/html")
                email.send()

            return JsonResponse({'success': 'Thanks for your purchase'})

        if request.POST.get('action') == 'c2pPaykey':
            data_id = str(request.POST.get('clientid'))
            client_data=data_id.encode()
            data_phone = code_country + str(request.POST.get('phone'))
            client_phone=data_phone.encode()
            CLIENT_ID = cipher.encrypt(client_data)
            CLIENT_ID_CIPHER = CLIENT_ID.decode("utf-8")
            MOBILE_DESTINATION = cipher.encrypt(client_phone)
            MERCHANT_MOBILE = MOBILE_DESTINATION.decode("utf-8")
            
            data = {
                "merchant_identify": {
                    "integratorId": TERMINAL_ID,
                    "merchantId": MERCHANT_ID,
                    "terminalId": "abcde"
                },
                "client_identify": {
                    "ipaddress": CLIENT_IP,
                    "browser_agent": CLIENT_BROWSER, 
                    "mobile": {
                        "manufacturer": "Samsung",
                        "model": "SOLSC",
                        "os_version": "",
                        "location": {
                            "lat": 0,
                            "lng": 0
                        }
                    }
                },
                "transaction_scpInfo": {
                "destination_id": CLIENT_ID_CIPHER,
                "destination_mobile_number": MERCHANT_MOBILE
        }
            }

            payload=json.dumps(data)
            conn.request("POST", "/mercantil-banco/sandbox/v1/mobile-payment/scp", payload, headers)

            res = conn.getresponse()
            data = res.read()

            text=data.decode("utf-8")
            print(text)
            bank_raw=json.loads(text)

            try:
                error_value=bank_raw['error_list']
                error_response=error_value[0]['description']
                
                if error_response == "Identificacion destino no valida su encriptacion":

                    response = JsonResponse({'empty': "Por favor llene los campos requeridos."})
                    return response
                    
                else:
                
                    response = JsonResponse({'failed': error_response})
                    return response

            except:
                    response = JsonResponse({'success': 'return something'})
                    return response
        
        if request.POST.get('action') == 'c2pPay':
            cart = Cart(request)
            get_code = str('pm')+get_random_string(20).lower()
            #payment data 
            user = request.user

            data_id = str(request.POST.get('clientid'))
            client_data=data_id.encode()

            flat_amount = str(total_ves)
            total = flat_amount.replace('.','')
            AMOUNT = int(total)
            BANK_ID = str(request.POST.get('bankcode'))
            
            data_phone = code_country + str(request.POST.get('phone'))
            client_phone=data_phone.encode()

            data_code = str(request.POST.get('optcode'))
            opt_code=data_code.encode()

            key = b'A11103402525120190822HB01'
            cipher = AESCipher(key)

            CLIENT_ID = cipher.encrypt(client_data)
            CLIENT_ID_CIPHER = CLIENT_ID.decode("utf-8")

            MOBILE_DESTINATION = cipher.encrypt(client_phone)
            MERCHANT_MOBILE = MOBILE_DESTINATION.decode("utf-8")
                    
            MOBILE_ORIGIN = cipher.encrypt(b'584122681189')
            CLIENT_MOBILE = MOBILE_ORIGIN.decode("utf-8")

            GET_PURCHASE_KEY = cipher.encrypt(opt_code)
            PURCHASE_KEY = GET_PURCHASE_KEY.decode("utf-8")

            get_control_number=ControlFacturacion.objects.all().count()
            control_number = get_control_number + 1
            numero_factura = "test-news"+"-"+"10"+str(control_number)
            conn = http.client.HTTPSConnection("apimbu.mercantilbanco.com")

            data = {
            "merchant_identify": {
                "integratorId": TERMINAL_ID,
                "merchantId": MERCHANT_ID,
                "terminalId": "abcde"
            },
            "client_identify": {
                "ipaddress": CLIENT_IP,
                "browser_agent": "undefined",
                "mobile": {
                "manufacturer": "",
                "model": "SOLSC",
                "os_version": "",
                "location": {
                    "lat": 37.422476,
                    "lng": 122.08425
                }
                }
            },
            "transaction_c2p": {
                "trx_type": "compra",
                "payment_method": "c2p",
                "destination_id": CLIENT_ID_CIPHER,
                "invoice_number": numero_factura,
                "currency": "VES",
                "amount": AMOUNT,
                "destination_bank_id": BANK_ID,
                "destination_mobile_number": MERCHANT_MOBILE,
                "origin_mobile_number": CLIENT_MOBILE,
                "twofactor_auth": PURCHASE_KEY
            }
            }

            payload=json.dumps(data)
            conn.request("POST", "/mercantil-banco/sandbox/v1/payment/c2p", payload, headers)

            res = conn.getresponse()
            data = res.read()

            text=data.decode("utf-8")
            print(text)
            bank_raw=json.loads(text)

            
            try:
                error_value=bank_raw['error_list']
                error_response=error_value[0]['description']

                if error_response == "Numero de factura procesado previamente":
                    twin_tranx = "Esta operacion ya fue procesada. Describa a soporte este N° Control" + " " + invoice_number

                    response = JsonResponse({'twin': twin_tranx})
                    return response

                elif error_response == "Segundo factor no valida su encriptacion":

                    response = JsonResponse({'empty': "Por favor ingrese la clave."})
                    return response
                else:
                    response = JsonResponse({'failed': error_response})
                    return response
            except:

                if bank_raw['transaction_c2p_response']['trx_status'] == "approved":

                    control_data=bank_raw['transaction_c2p_response']['invoice_number']
                    key_validator=bank_raw['transaction_c2p_response']['payment_reference']
                    print(key_validator)
                    order.update(status="Completed")
                    BillingRecipt.objects.filter(pk=invoice.pk).update(status="Payeed", payment_option="VES")
                    
                    control_invoice = InvoiceControl.objects.filter(recipt=invoice)
                    control_invoice.update(control_id=numero_factura)

                    StelaPayments.objects.create (
                            user=invoice.owner,
                            billing=order_id,
                            key_validator=get_code,
                            transaction_id=key_validator,
                            payment_option='Pago Movil',
                            subtotal=invoice.amount,
                            taxes=invoice.tax,
                            profit=profit,
                            payment_fee=payment_fee,
                            total_paid=total_paid,
                            host=_("Final Stela Websites")
                        )
                    if ControlFacturacion.objects.filter(control_id=control_data).exists():
                        pass
                    else:
                        orderget=Order.objects.get(pk=orderid)
                        factura_control = ControlFacturacion.objects.create(
                            owner=invoice.owner,
                            customer=invoice.customer,
                            order=orderget,
                            control_id=control_data,
                            base=base,
                            iva=iva,
                            total=itotal,
                        )
                        factura_pk = factura_control.pk
                        FacturaItems.objects.create(
                            order_id=factura_pk,
                            origin=orderget,
                        )
                    for select in orderitems:
                        selection=StelaSelection.objects.filter(pk=select.stela_selection.pk)
                        counter=StelaSelection.objects.filter(pk=select.stela_selection.pk).count()
                                
                        html_content = render_to_string('stela_control/emails-template/orders/stela_order_placed_ves2.html', {
                            'order': order,
                            'subtotal': base,
                            'tax': iva,
                            'fee': fee_ves,
                            'total': total,
                            'count': counter,
                            'selection': selection 
                            })

                        text_content = strip_tags(html_content)
                            
                        email = EmailMultiAlternatives(
                                _('Payment Complete Successfully'),
                                text_content,
                                invoice.owner.email_sender,
                                [invoice.customer.email]
                                                
                            )
                        email.attach_alternative(html_content, "text/html")
                        email.send()

                        message = render_to_string('stela_control/emails-template/payments/sale_notification.html',{
                                    
                        })

                        text_render = strip_tags(message)

                        email = EmailMultiAlternatives(
                                _('Billing Payment Made'),
                                text_render,
                                settings.STELA_EMAIL,
                                [settings.DEFAULT_EMAIL]
                                                
                            )
                        email.attach_alternative(message, "text/html")
                        email.send()

                    return JsonResponse({'success': 'Thanks for your purchase'})
        
    return render(request, 'linkzone/costumer/payments/billing-checkout.html', context)

def cloudCheckout(request, reciptid):
    lang=request.LANGUAGE_CODE
    form = LoginForm()
    msg = ""
    if lang=="es-ve":
        vcost = Modules.objects.get(title="Uso de la instancia de la nube (Horas)", parent__title="Stela Cloud Services", parent__lang=lang)
        cscost = Modules.objects.get(title="Uso de almacenamiento en la nube (GB de datos)", parent__title="Stela Cloud Services", parent__lang=lang)
        reqcost= Modules.objects.get(title="Solicitudes de contenido en la nube", parent__title="Stela Cloud Services", parent__lang=lang)
        dnscost = Modules.objects.get(title="Costo Orbit Zona DNS", parent__title="Stela Cloud Services", parent__lang=lang)
    else:
        vcost= Modules.objects.get(title="Cloud Instance Usage (Hours)", parent__title="Stela Cloud Services", parent__lang=lang)
        cscost= Modules.objects.get(title="Cloud Storage Usage (GB Data)", parent__title="Stela Cloud Services", parent__lang=lang)
        reqcost= Modules.objects.get(title="Cloud Content Requests", parent__title="Stela Cloud Services", parent__lang=lang)
        dnscost= Modules.objects.get(title="Zone DNS Orbit Cost", parent__title="Stela Cloud Services", parent__lang=lang)

    if request.method == 'POST' and 'loginform' in request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request,user)
                    return redirect('/stela/checkout')
                else:
                    msg = 'credenciales invalidas'

                    return render(request, 'linkzone/costumer/payments/checkout.html', {
                    'call': 'stela',
                    'form': form,
                    })
            else:
                msg = 'credenciales invalidas'

                return render(request, 'linkzone/costumer/payments/checkout.html', {
                'call': 'stela',
                'form': form,
                'messages': msg
            })

        else: 
            msg = 'error validando usuario'

            return render(request, 'linkzone/costumer/payments/checkout.html', {
                'call': 'stela',
                'form': form,
                'messages': msg
            })
    
    url = settings.VES_MONITOR
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        currency=Decimal(data['USD']['promedio_real'])
    else:
        currency=Decimal(24.48)
        
    headers = {
            'X-IBM-Client-Id': settings.MERCANTIL_CLIENT_ID,
            'content-type': "application/json",
            'accept': "application/json"
            }
    MERCHANT_ID = settings.MERCANTIL_MERCHANT_ID
    TERMINAL_ID = settings.MERCANTIL_TERMINAL_ID
    conn = http.client.HTTPSConnection("apimbu.mercantilbanco.com")
    code_country="58" 
    # Client information
    CLIENT_IP = "10.0.0.1"
    CLIENT_BROWSER = "Chrome 18.1.3"
    key = b'A11103402525120190822HB01'
    cipher = AESCipher(key)

    user = request.user
    invoice = BillingRecipt.objects.get(pk=reciptid)
    getimport=invoice.amount + invoice.tax
    payment_fee = getimport * Decimal(0.02)
    profit = invoice.amount * Decimal(0.25)
    total_paid = invoice.amount + invoice.tax + payment_fee

    get_control_number=BillingRecipt.objects.filter(is_generated=True, is_budget=False, payment_option="USD",).count()
    control_number = get_control_number + 1
    invoice_number = "DB"+"-"+"0"+str(control_number)


    base = round(invoice.amount * currency, 2)
    iva = round(invoice.tax * currency, 2)
    itotal = base + iva
    fee_ves = round(itotal * Decimal(0.07), 2)

    if invoice.discount:
        descuento = round(invoice.discount * currency, 2)
        total_ves = round(base + iva + fee_ves - descuento, 2)
        calc= invoice.amount + invoice.tax
        fee = round(calc * Decimal(0.07), 2)
        total_amount = invoice.amount + invoice.tax + fee - invoice.discount
    else:
        total_ves = round(base + iva + fee_ves, 2)
        calc2 = invoice.amount + invoice.tax
        fee = round(calc2 * Decimal(0.07), 2)
        total_amount = invoice.amount + invoice.tax + fee
        descuento = ""
    
    context={
        'form': form,
        'call': 'FinalPayment',
        'messages': msg,
        'inv': invoice,
        'total': total_amount,
        'base': base,
        'iva': iva,
        'fee': fee,
        'ves_fee': fee_ves,
        'descuento': descuento,
        'total_ves': total_ves,
        'cost1': vcost.price,
        'cost2': cscost.price,
        'cost3': reqcost.price,
        'cost4': dnscost.price
    }   

    if request.method == 'POST':
    
        action = request.POST.get('action')
        print(action)
        
        if request.POST.get('action') == "paypal":
            PPClient = PaypalClient()
            data = request.POST.get('orderID')
            requestorder = OrdersGetRequest(data)
            response = PPClient.client.execute(requestorder)
            get_code = str('PP')+get_random_string(8).upper()
            try:
                if total_amount == response.result.purchase_units[0].amount.value:
                    BillingRecipt.objects.filter(pk=invoice.pk).update(status="Payeed", payment_option="USD")
                    
                    order = Order.objects.create (
                    owner=invoice.owner,
                    customer=invoice.customer,
                    email=invoice.customer.email,
                    key_validator=response.result.id,
                    transaction_id=get_code,
                    payment_option='Paypal',
                    status="Payeed",
                    subtotal=invoice.amount,
                    taxes=invoice.tax,
                    payment_fee=fee,
                    profit=invoice.amount * Decimal(0.25),
                    total_paid=total_amount,
                    section="Stela Cloud"
                    )
                    order_id = order.pk
                    StelaPayments.objects.create (
                                user=invoice.owner,
                                billing=order_id,
                                key_validator=response.result.id,
                                transaction_id=get_code,
                                payment_option='Paypal',
                                subtotal=invoice.amount,
                                taxes=invoice.tax,
                                profit=profit,
                                payment_fee=payment_fee,
                                total_paid=response.result.purchase_units[0].amount.value,
                                host=_("Final Stela Websites")
                            )
                    control_invoice = InvoiceControl.objects.filter(recipt=invoice)
                    control_invoice.update(control_id=invoice_number)
                    recipt = InvoiceControl.objects.get(recipt=invoice)
                    html_content = render_to_string('stela_control/emails-template/payments/billing_payment.html', {
                        
                        })

                    text_content = strip_tags(html_content)
                    
                    email = EmailMultiAlternatives(
                            _('Payment Complete Successfully'),
                            text_content,
                            invoice.owner.email_sender,
                            [invoice.customer.email]
                                            
                        )
                    email.attach_alternative(html_content, "text/html")
                    email.send()

                    message = render_to_string('stela_control/emails-template/payments/payment_notification.html',{
                                'order': orderget,
                            })

                    text_render = strip_tags(message)

                    email = EmailMultiAlternatives(
                        _('Billing Notification'),
                        text_render,
                        settings.STELA_EMAIL,
                        [settings.DEFAULT_EMAIL]
                                                
                        )
                    email.attach_alternative(message, "text/html")
                    email.send()
                    
                    return JsonResponse({'success': _('Thanks for your purchase')})
                
                else:
                    #captar datos en servidor notificar email
                    # lon = str(data['lon'])
                    # lat = str(data['lat'])
                    # SiteControl.objects.create(
                    #     ip=ip,
                    #     lon=lon,
                    #     lat=lat,
                    #     pishing=True
                    # )
                    return JsonResponse({'failed': _('Amount Verification Failed')})
                
            except Exception as e:
                print(e)
                return JsonResponse({'failed': _('Payment Failed')})
        
        if request.POST.get('action') == "tdd-pay":
            get_code = str('Epay')+get_random_string(8).upper()
            order_key = request.POST.get('order_key')
            
            BillingRecipt.objects.filter(pk=invoice.pk).update(status="Payeed", payment_option="USD")
            order = Order.objects.create (
                owner=invoice.owner,
                customer=invoice.customer,
                email=invoice.customer.email,
                key_validator=order_key,
                transaction_id=get_code,
                payment_option='TDD-TDC Payment',
                status="Payeed",
                subtotal=invoice.amount,
                taxes=invoice.tax,
                payment_fee=fee,
                profit=invoice.amount * Decimal(0.25),
                total_paid=total_amount,
                section="Stela Cloud"
            )

            order_id = order.pk
            StelaPayments.objects.create (
                            user=invoice.owner,
                            billing=order_id,
                            key_validator=order_key,
                            transaction_id=get_code,
                            payment_option='Debit Card',
                            subtotal=invoice.amount,
                            taxes=invoice.tax,
                            profit=profit,
                            payment_fee=payment_fee,
                            total_paid=total_paid,
                            host=_("Stela Business App")
                        )
            control_invoice = InvoiceControl.objects.filter(recipt=invoice)
            control_invoice.update(control_id=invoice_number)
            recipt = InvoiceControl.objects.get(recipt=invoice)
            html_content = render_to_string('stela_control/emails-template/payments/billing_payment.html', {
                        
                        })
            text_content = strip_tags(html_content)
                
            email = EmailMultiAlternatives(
                        _('Payment Complete Successfully'),
                        text_content,
                        invoice.owner.email_sender,
                        [invoice.customer.email]
                                        
                    )
            email.attach_alternative(html_content, "text/html")
            email.send()

            message = render_to_string('stela_control/emails-template/payments/payment_notification.html',{
                                'order': orderget,
                            })

            text_render = strip_tags(message)

            email = EmailMultiAlternatives(
                 _('Billing Notification'),
                text_render,
                settings.STELA_EMAIL,
                [settings.DEFAULT_EMAIL]
                                        
                )
            email.attach_alternative(message, "text/html")
            email.send()

            return JsonResponse({'success': 'Thanks for your purchase'})

        if request.POST.get('action') == 'c2pPaykey':
            data_id = str(request.POST.get('clientid'))
            client_data=data_id.encode()
            data_phone = code_country + str(request.POST.get('phone'))
            client_phone=data_phone.encode()
            CLIENT_ID = cipher.encrypt(client_data)
            CLIENT_ID_CIPHER = CLIENT_ID.decode("utf-8")
            MOBILE_DESTINATION = cipher.encrypt(client_phone)
            MERCHANT_MOBILE = MOBILE_DESTINATION.decode("utf-8")
            
            data = {
                "merchant_identify": {
                    "integratorId": TERMINAL_ID,
                    "merchantId": MERCHANT_ID,
                    "terminalId": "abcde"
                },
                "client_identify": {
                    "ipaddress": CLIENT_IP,
                    "browser_agent": CLIENT_BROWSER, 
                    "mobile": {
                        "manufacturer": "Samsung",
                        "model": "SOLSC",
                        "os_version": "",
                        "location": {
                            "lat": 0,
                            "lng": 0
                        }
                    }
                },
                "transaction_scpInfo": {
                "destination_id": CLIENT_ID_CIPHER,
                "destination_mobile_number": MERCHANT_MOBILE
        }
            }

            payload=json.dumps(data)
            conn.request("POST", "/mercantil-banco/sandbox/v1/mobile-payment/scp", payload, headers)

            res = conn.getresponse()
            data = res.read()

            text=data.decode("utf-8")
            print(text)
            bank_raw=json.loads(text)

            try:
                error_value=bank_raw['error_list']
                error_response=error_value[0]['description']
                
                if error_response == "Identificacion destino no valida su encriptacion":

                    response = JsonResponse({'empty': "Por favor llene los campos requeridos."})
                    return response
                    
                else:
                
                    response = JsonResponse({'failed': error_response})
                    return response

            except:
                    response = JsonResponse({'success': 'return something'})
                    return response
        
        if request.POST.get('action') == 'c2pPay':
            cart = Cart(request)
            get_code = str('pm')+get_random_string(20).lower()
            #payment data 
            user = request.user

            data_id = str(request.POST.get('clientid'))
            client_data=data_id.encode()

            flat_amount = str(total_ves)
            total = flat_amount.replace('.','')
            AMOUNT = int(total)
            BANK_ID = str(request.POST.get('bankcode'))
            
            data_phone = code_country + str(request.POST.get('phone'))
            client_phone=data_phone.encode()

            data_code = str(request.POST.get('optcode'))
            opt_code=data_code.encode()

            key = b'A11103402525120190822HB01'
            cipher = AESCipher(key)

            CLIENT_ID = cipher.encrypt(client_data)
            CLIENT_ID_CIPHER = CLIENT_ID.decode("utf-8")

            MOBILE_DESTINATION = cipher.encrypt(client_phone)
            MERCHANT_MOBILE = MOBILE_DESTINATION.decode("utf-8")
                    
            MOBILE_ORIGIN = cipher.encrypt(b'584122681189')
            CLIENT_MOBILE = MOBILE_ORIGIN.decode("utf-8")

            GET_PURCHASE_KEY = cipher.encrypt(opt_code)
            PURCHASE_KEY = GET_PURCHASE_KEY.decode("utf-8")

            get_control_number=ControlFacturacion.objects.all().count()
            control_number = get_control_number + 1
            numero_factura = "test-news"+"-"+"15"+str(control_number)
            conn = http.client.HTTPSConnection("apimbu.mercantilbanco.com")

            data = {
            "merchant_identify": {
                "integratorId": TERMINAL_ID,
                "merchantId": MERCHANT_ID,
                "terminalId": "abcde"
            },
            "client_identify": {
                "ipaddress": CLIENT_IP,
                "browser_agent": "undefined",
                "mobile": {
                "manufacturer": "",
                "model": "SOLSC",
                "os_version": "",
                "location": {
                    "lat": 37.422476,
                    "lng": 122.08425
                }
                }
            },
            "transaction_c2p": {
                "trx_type": "compra",
                "payment_method": "c2p",
                "destination_id": CLIENT_ID_CIPHER,
                "invoice_number": numero_factura,
                "currency": "VES",
                "amount": AMOUNT,
                "destination_bank_id": BANK_ID,
                "destination_mobile_number": MERCHANT_MOBILE,
                "origin_mobile_number": CLIENT_MOBILE,
                "twofactor_auth": PURCHASE_KEY
            }
            }

            payload=json.dumps(data)
            conn.request("POST", "/mercantil-banco/sandbox/v1/payment/c2p", payload, headers)

            res = conn.getresponse()
            data = res.read()

            text=data.decode("utf-8")
            print(text)
            bank_raw=json.loads(text)

            
            try:
                error_value=bank_raw['error_list']
                error_response=error_value[0]['description']

                if error_response == "Numero de factura procesado previamente":
                    twin_tranx = "Esta operacion ya fue procesada. Describa a soporte este N° Control" + " " + invoice_number

                    response = JsonResponse({'twin': twin_tranx})
                    return response

                elif error_response == "Segundo factor no valida su encriptacion":

                    response = JsonResponse({'empty': "Por favor ingrese la clave."})
                    return response
                else:
                    response = JsonResponse({'failed': error_response})
                    return response
            except:

                if bank_raw['transaction_c2p_response']['trx_status'] == "approved":

                    control_data=bank_raw['transaction_c2p_response']['invoice_number']
                    key_validator=bank_raw['transaction_c2p_response']['payment_reference']
                    print(key_validator)
                    
                    BillingRecipt.objects.filter(pk=invoice.pk).update(status="Payeed", payment_option="VES")
                    order = Order.objects.create (
                        owner=invoice.owner,
                        customer=invoice.customer,
                        email=invoice.customer.email,
                        key_validator=key_validator,
                        transaction_id=get_code,
                        payment_option='PAGO MOVIL',
                        status="Payeed",
                        subtotal=invoice.amount,
                        taxes=invoice.tax,
                        payment_fee=fee,
                        profit=invoice.amount * Decimal(0.25),
                        total_paid=total_amount,
                        section="Stela Cloud"
                    )
                    order_id = order.pk
                    control_invoice = InvoiceControl.objects.filter(recipt=invoice)
                    control_invoice.update(control_id=numero_factura)

                    StelaPayments.objects.create (
                            user=invoice.owner,
                            billing=order_id,
                            key_validator=get_code,
                            transaction_id=key_validator,
                            payment_option='Pago Movil',
                            subtotal=invoice.amount,
                            taxes=invoice.tax,
                            profit=profit,
                            payment_fee=payment_fee,
                            total_paid=total_paid,
                            host=_("Final Stela Websites")
                        )
                    if ControlFacturacion.objects.filter(control_id=control_data).exists():
                        pass
                    else:
                        orderget=Order.objects.get(pk=order_id)
                        factura_control = ControlFacturacion.objects.create(
                            owner=invoice.owner,
                            customer=invoice.customer,
                            order=orderget,
                            control_id=control_data,
                            base=base,
                            iva=iva,
                            total=itotal,
                        )
                        factura_pk = factura_control.pk
                        FacturaItems.objects.create(
                            order_id=factura_pk,
                            origin=orderget,
                        )
                    html_content = render_to_string('stela_control/emails-template/payments/billing_payment.html', {
                        
                        })

                    text_content = strip_tags(html_content)

                    email = EmailMultiAlternatives(
                                'Su pago fue procesado exitosamente',
                                text_content,
                                settings.STELA_EMAIL,
                                [user.email]
                                                
                            )
                    email.attach_alternative(html_content, "text/html")
                    email.send()

                    message = render_to_string('stela_control/emails-template/payments/payment_notification.html',{
                                'order': orderget,
                            })

                    text_render = strip_tags(message)

                    email = EmailMultiAlternatives(
                            _('Billing Notification'),
                            text_render,
                            settings.STELA_EMAIL,
                            [settings.DEFAULT_EMAIL]
                                        
                        )
                    email.attach_alternative(message, "text/html")
                    email.send()
                    
                    return JsonResponse({'success': 'Thanks for your purchase'})
        
    return render(request, 'linkzone/costumer/payments/billing-checkout.html', context)

def websites(request):
    user = request.user
    alert = Notifications.objects.filter(user=user).order_by('-created')[:10]
    count = Notifications.objects.filter(user=user, status="No Read").count()
    orders = Order.objects.filter(owner=user).order_by('-id')
    filter = request.POST.get('term')
    q = request.POST.get('qs')

    if filter:
        orders = Order.objects.filter(owner=user).order_by(filter)
    
    if q:
        orders = Order.objects.filter(owner=user, transaction_id=q)

    page = request.GET.get('page', 1)

    paginator = Paginator(orders, 5)
    
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)
    context ={
       'pages': lists,
       'alerts': alert,
       'count': count
    }

    return render(request, 'linkzone/stela/websites.html', context)

def cloudServices(request):
    master_user=UserBase.objects.get(username="emmerut")
    user = request.user
    total_usage = 0
    from datetime import date
    json_path = os.path.join(os.getcwd(), 'credentials.json')
    start_time = datetime.datetime.utcnow() - datetime.timedelta(days=30)
    end_time = datetime.datetime.utcnow()

    # Carga las credenciales de GCP desde un archivo JSON
    credentials = service_account.Credentials.from_service_account_file(json_path)

    # Crea un cliente de la API de Stackdriver Monitoring
    client = monitoring_v3.MetricServiceClient(credentials=credentials)

    # Define los parámetros para obtener las métricas de CPU de una instancia de Compute Engine
    project_id = settings.GCP_PROJECT_ID
    project_name = f"projects/{project_id}"
    filter = 'metric.type="compute.googleapis.com/instance/uptime"'
    interval = monitoring_v3.TimeInterval(
        start_time={"seconds": int(start_time.timestamp())},
        end_time={"seconds": int(end_time.timestamp())},
    )
    # Obtiene las métricas de CPU de la instancia de Compute Engine
    results = client.list_time_series(
        name=project_name,
        filter=filter,
        interval=interval,
        view=None,
        retry=None,
    )
    for result in results:
        current_usage=result.points[0].value.double_value
        total_usage += current_usage
        
    alert = Notifications.objects.filter(user=user).order_by('-created')[:10]
    count = Notifications.objects.filter(user=user, status="No Read").count()
    today = timezone.localtime(timezone.now())
    cloud_account=UserBase.objects.get(pk=user.pk)
    history1=today
    history2=today-timedelta(days=30) 
    history3=today-timedelta(days=60)
    history4=today-timedelta(days=90)  
    history5=today-timedelta(days=120)   
    history6=today-timedelta(days=150)
    get_dns=ZoneDNS.objects.get(owner=user)
    get_vc=VirtualCloud.objects.get(owner=user)
    get_storage=CloudStorage.objects.get(owner=user)
    get_request=ResquetsCloud.objects.get(owner=user)
    dns=UsageCloud.objects.filter(zonadns=get_dns).aggregate(total=Sum('monthy_cost'))
    vcloud=UsageCloud.objects.filter(virtualcloud=get_vc).aggregate(total=Sum('monthy_cost'))
    cstorage=UsageCloud.objects.filter(cloudstorage=get_storage).aggregate(total=Sum('monthy_cost'))
    crequests=UsageCloud.objects.filter(requestcloud=get_request).aggregate(total=Sum('monthy_cost'))
    
    values = []
    usage = []

    from django.template.defaultfilters import date
    usage6 = UsageCloud.objects.filter(virtualcloud__owner=user, virtualcloud__created=history6).aggregate(get_usage=Sum('usage'))
    if usage6['get_usage']: 
        usage.append((usage6))
    else:
        usage6['get_usage'] = 0
        usage.append((usage6))
    values.append(date(history6, 'F'))

    usage5 = UsageCloud.objects.filter(virtualcloud__owner=user, virtualcloud__created=history5).aggregate(get_usage=Sum('usage'))
    if usage5['get_usage']: 
        usage.append((usage5))
    else:
        usage5['get_usage'] = 0
        usage.append((usage5))
    values.append(date(history5, 'F'))

    usage4 = UsageCloud.objects.filter(virtualcloud__owner=user, virtualcloud__created=history4).aggregate(get_usage=Sum('usage'))
    if usage4['get_usage']: 
        usage.append((usage4))
    else:
        usage4['get_usage'] = 0
        usage.append((usage4))
    values.append(date(history4, 'F'))

    usage3 = UsageCloud.objects.filter(virtualcloud__owner=user, virtualcloud__created=history3).aggregate(get_usage=Sum('usage'))
    if usage3['get_usage']: 
        usage.append((usage3))
    else:
        usage3['get_usage'] = 0
        usage.append((usage3))
    values.append(date(history3, 'F'))

    usage2 = UsageCloud.objects.filter(virtualcloud__owner=user, virtualcloud__created=history2).aggregate(get_usage=Sum('usage'))
    if usage2['get_usage']: 
        usage.append((usage2))
    else:
        usage2['get_usage'] = 0
        usage.append((usage2))
    values.append(date(history2, 'F'))

    usage1 = UsageCloud.objects.filter(virtualcloud__owner=user, virtualcloud__created=history1).aggregate(get_usage=Sum('usage'))
    if usage1['get_usage']: 
        usage.append((usage1))
    else:
        usage1['get_usage'] = total_usage
        usage.append((usage1))
    values.append(date(history1, 'F'))
    
    domains=Domains.objects.filter(owner=request.user, status="Payeed")
    customer=Customer.objects.get(email=user.email)
    billing=InvoiceControl.objects.filter(recipt__customer=customer, recipt__option="Cloud Subscription")

    context ={
        'billings':billing,
        'domains':domains,
        'cusage':current_usage,
        'dns':dns,
        'vcloud':vcloud,
        'cstorage':cstorage,
        'crequests':crequests, 
        'usage':usage,
        'account': cloud_account,
        'values':values,
        'alerts': alert,
        'count': count
    }
    if request.method == "POST":
        action=request.POST.get('action')
        
        if action == "downAccount":
            UserBase.objects.filter(pk=request.user.pk).update(cloud_services=False)
            Notifications.objects.create (
                user = master_user,
                status = "No Read",
                title = _("An account has been deactivated"),
                description ="Account ID " + user.cloud_id,
                section = "Cloud Services Down",
                url = "" 
            )
            return JsonResponse({'success': _('Your account has been deactivated')})
        
        if action == "upAccount":
            UserBase.objects.filter(pk=request.user.pk).update(cloud_services=True)
            Notifications.objects.create (
                user = master_user,
                status = "No Read",
                title = _("An account has been activated"),
                description ="Account ID " + user.cloud_id,
                section = "Cloud Services Up",
                url = "" 
            )
            return JsonResponse({'success': _('Your account has been activated')})

    return render(request, 'linkzone/cloud/index.html', context)

def invoiceCloud(request, id):
    master_user=UserBase.objects.get(username="emmerut")
    invoice = InvoiceControl.objects.get(pk=id)

    if invoice.recipt.tax:

        if invoice.recipt.discount:
            total = invoice.recipt.amount + invoice.recipt.tax - invoice.recipt.discount
        else:
            total = invoice.recipt.amount + invoice.recipt.tax
    else:
        if invoice.recipt.discount:
            total = invoice.recipt.amount - invoice.recipt.discount
        else:
            total = invoice.recipt.amount

    context = {
        'inv': invoice,
        'total': total,
    }

    return render(request, 'linkzone/cloud/invoice.html', context)

def blogDetail(request, slug):
    lang = request.LANGUAGE_CODE
    blog = Content.objects.get(slug=slug)
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
    ip = user_ip.split(',')[0] 
    res = requests.get('http://ip-api.com/json/' + ip)
    data_one = res.text
    data = json.loads(data_one)
    try:
        cc = str(data['countryCode'])
        country=Country.objects.get(code3=cc)
    except:
        country=None
    
    viewscount=SiteViews.objects.filter(host=ip, page="Blog", blog=blog)
    count=+1

    if viewscount.exists():
        gethost=SiteViews.objects.get(host=ip, page="Blog", blog=blog)
        new_count=gethost.views + 1
        viewscount.update(
            views=new_count,
            lastdate=timezone.localtime(timezone.now())
        )
    else:
        SiteViews.objects.create(
            blog=blog,
            page="Blog",
            host=ip,
            views=count,
            country=country  
        )
        
    form=CommentForm()
    form2 = NewsletterForm()
    comments = Comments.objects.filter(post=blog.id, status="Published") 
    counter=SiteViews.objects.filter(page="Blog", blog=blog).aggregate(total=Sum('views'))
    count1=comments.count()
    count2=counter['total']

    context = {
        'blog':blog,
        'form': form,
        'newsletter':form2,
        'comments': comments,
        'comment_count': count1,
        'views_count': count2
    }

    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        print(form_id)

        if form_id == "comments":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment=form.save(commit=False)
                comment.post = blog
                comment.host=ip
                comment.save()

                messages.success(request, _("Your message has been sent"))
                return HttpResponseRedirect(reverse('linkzone:blog_detail', args=[str(slug)]))
        
        if form_id == "newsletter":
            email=request.POST.get('email')
            if DataEmail.objects.filter(email=email).exists():
                messages.warning(request, _("This email is already registered"))
                return HttpResponseRedirect(reverse('linkzone:blog_detail', args=[str(slug)]))
            else:
                form = NewsletterForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, _("Now you are subscribed"))
                    return HttpResponseRedirect(reverse('linkzone:blog_detail', args=[str(slug)]))

    return render(request, 'blog/single-blog.html', context)

def docs(request):
    lang=request.LANGUAGE_CODE
    author=UserBase.objects.get(username="emmerut")
    about=Content.objects.filter(section="About Values", status="Publish", lang=lang)
    apps=Content.objects.filter(path="Services", status="Publish", lang=lang)
    cards=Content.objects.filter(section="Card Content", status="Publish", lang=lang)
    image_bullets=Content.objects.filter(section="Image Bullet", status="Publish", lang=lang)
    box_bullet=Content.objects.filter(section="Icon Box", status="Publish", lang=lang)

    context={
        'about': about,
        'apps': apps,
        'cards': cards,
        'image_bullet': image_bullets,
        'box_bullets': box_bullet,
        'author': author
    }
    
    return render(request, 'linkzone/costumer/docs/index.html', context)

def stelaSuitePolicy(request):
    lang=request.LANGUAGE_CODE
    about=Content.objects.filter(parent__section="Emmerut About Us", status="Publish", lang=lang).order_by('-created')[:3]
    apps = TemplateSections.objects.filter(section='Content Emmerut', lang=lang)
    legal = SitePolicy.objects.filter(parent__section="Emmerut Legal", status="Publish", lang=lang)

    context={
        'apps': apps,
        'about': about,
        'legal': legal,
        'call': 'Stela Business Policy'
    }
    
    return render(request, 'linkzone/costumer/docs/policy-detail.html', context)

def create_case(request):
    user = request.user
    ticket_gen = str('ISSUE-')+get_random_string(6).upper()
    email_user = user.email
    form = SupportForm()
    alert = Notifications.objects.filter(user=user).order_by('-created')[:10]
    count = Notifications.objects.filter(user=user, status="No Read").count()

    if request.method == 'POST':
        form = SupportForm(request.POST, request.FILES)
        
        if form.is_valid():
            supportcase = form.save(commit=False)
            supportcase.user_id = user.id
            supportcase.ticket = ticket_gen
            supportcase.email = email_user
            supportcase.save()

            rated_answer=supportcase.created+timedelta(days=2)
            html_content = render_to_string('emails/transactionals/support_email.html', {
                        'ticket': ticket_gen,
                        'subject': supportcase.option,
                        'date': supportcase.created,
                        'rated_answer': rated_answer,
                })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                _('We have registered your case'),
                text_content,
                settings.SUPPORT_EMAIL,
                [email_user]
               
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            message = render_to_string('stela_control/emails-template/support/support_notification.html',{
                    'ticket': supportcase.ticket,
                    'subject': supportcase.option,
                    'date': supportcase.created,
                    'rated_answer': rated_answer,
                    'user': request.user

            })
            text_render = strip_tags(message)

            email = EmailMultiAlternatives(
                'A new support case has been created',
                text_render,
                settings.STELA_EMAIL,
                [settings.DEFAULT_EMAIL]
               
            )
            email.attach_alternative(message, "text/html")
            email.send()

            messages.success(request, "Your case has been successfully registered")
            return redirect('linkzone:support_list')
        else:
            print (form.errors)

    return render(request, 'linkzone/costumer/issue_center/create_case.html', {
        'form': form,
        'alerts': alert,
        'count': count
        
        })

@login_required
def support_view(request):
    current_user = request.user
    support_list = Support.objects.filter(user_id=current_user.id)
    q = request.POST.get('qs')
    date = request.POST.get('date')
    alert = Notifications.objects.filter(user=current_user).order_by('-created')[:10]
    count = Notifications.objects.filter(user=current_user, status="No Read").count()

    if q: 
        support_list = Support.objects.filter(ticket__icontains=q, user_id=current_user.id).order_by('-id')

    if date:
        date_min = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=int(date)), datetime.time.min)
        today = timezone.now()
        support_list = Support.objects.filter(user_id=current_user.id, created__range=[date_min, today]).order_by('-id')
    
    page = request.GET.get('page', 1)

    paginator = Paginator(support_list, 7)
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)

    context ={
        'support': lists,
        'alerts': alert,
        'count': count
        }
    return render(request, 'linkzone/costumer/issue_center/support_list.html', context)

@login_required
def update_case(request, id):
    user = request.user
    support = Support.objects.get(id=id)
    email = user.email
    alert = Notifications.objects.filter(user=user).order_by('-created')[:10]
    count = Notifications.objects.filter(user=user, status="No Read").count()

    readsuportform = ReadOnlySupportFormCostumer(instance=support)
    
    if SupportResponse.objects.filter(case_id=id).exists():
        responseformset = inlineformset_factory(Support, ChatSupport, fields=('response',), widgets={'response': Textarea(attrs={ 'required': 'true' })}, extra=1, can_delete=False)
        responses = SupportResponse.objects.filter(case_id=id)
        chat_support = ChatSupport.objects.filter(case_id=id)
        context = { 
                'responseformset':responseformset,
                'readsupportform': readsuportform,
                'support': support,
                'chatsupport': chat_support,
                'responses': responses,
                'alerts': alert,
                'count': count
             }
    else:
        context = { 
                'readsupportform': readsuportform,
                'support': support,
                'alerts': alert,
                'count': count
             }
        
    if request.method == 'POST':
        readsupportform = ReadOnlySupportFormCostumer(request.POST, instance=support)
        formresponse = responseformset(request.POST)
        
        if all([readsupportform.is_valid(), 
                formresponse.is_valid(),
            ]):
           
            message = readsupportform.cleaned_data['message']
            parent = readsupportform.save(commit=False)
            parent.save()
        
            for form in formresponse:
                response = form.save(commit=False)
                response.user_id = user.id
                response.case = parent
                response.save()

            html_content = render_to_string('stela_control/emails-template/support/support_response.html', {
                        'ticket': response.case.ticket,
                        'subject': response.case.option,
                        'user': response.user.username,
                        'update': datetime.date.today(),
                        })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                _('User has answered his case'),
                text_content,
                settings.STELA_EMAIL,
                [settings.DEFAULT_EMAIL]
               
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, _("Changes made successfully"))
            return redirect('linkzone:support_list')

    return render(request, 'linkzone/costumer/issue_center/update_support.html', context)


def profile(request):
    user = request.user
    data = UserBase.objects.get(pk=user.id)
    profile = UserEditForm(instance=data)
    addressForm = AddressForm()
    addresses = Addresses.objects.filter(user_id=user.id)
    alert = Notifications.objects.filter(user=user).order_by('-created')[:10]
    count = Notifications.objects.filter(user=user, status="No Read").count()

    context = {
        'profile': profile,
        'address': addressForm,
        'addresses': addresses,
        'alerts': alert,
        'count': count
    }
    return render(request, 'linkzone/costumer/profile-center.html', context)

def profileForm(request):

    user = request.user
    data = UserBase.objects.get(pk=user.id)

    if request.method == 'POST':
        user = request.user
        data = UserBase.objects.get(pk=user.id)
        profile = UserEditForm(request.POST, request.FILES, instance=data)
        if profile.is_valid():
            form = profile.save(commit=False)
            form.user = user
            form.save()

            return redirect('/console/profile')
        else:
            print (profile.errors)

def addressForm(request):

    if request.method == 'POST':
        user = request.user
        addressForm = AddressForm(request.POST)
        address = Addresses.objects.filter(user_id=user.id, status="Selected")

        if addressForm.is_valid():
            form = addressForm.save(commit=False)
            form.user = user
            if address.exists():
                form.status = "Not Selected"
            else:
                form.status = "Selected"
            form.save()

            return redirect('/console/profile')
        else:
            print (addressForm.errors)

def siteRequests(request):
    user = request.user
    if request.POST.get('action') == 'cityCheck':
        country_id = request.POST.get('country_id')
        cities = City.objects.filter(country_id=country_id)
    
        return render(request, 'linkzone/render/city_data.html', {'cities': cities})

    if request.POST.get('action') == 'addressDefault':
        address_id = request.POST.get('address_id')
        address = Addresses.objects.filter(user_id=user.id, status="Selected")
        
        if address.exists():
            address.update(status="Not Selected")
            Addresses.objects.filter(pk=address_id).update(status="Selected")
    
            response = JsonResponse({'success': 'return something'})
            return response

    if request.POST.get('action') == 'deleleAddress':
    
        ids = request.POST.getlist('id[]')
        for id in ids:
            addresses = Addresses.objects.get(pk=id)
            addresses.delete()

        response = JsonResponse({'success': 'return something'})
        return response
    
    if request.POST.get('action') == 'closeAccount':
        user = request.user
        UserBase.objects.filter(id=user.id).update(is_active=False)
        
        messages.error(request, "your account has been deactivated. You can reactivate it by contacting support")
        response = JsonResponse({'success': 'return something'})
        return response

    if request.POST.get('form-call') == "newsletter":
        email=request.POST.get('email')
        form=NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.email=email
            newsletter.save()    
            
            html_content = render_to_string('stela_control/emails-template/newsletter/success.html', {
                
                })

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                    'You have successfully subscribed',
                    text_content,
                    settings.NEWSLETTER_EMAIL,
                    [email]
                                    
                )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            message = render_to_string('stela_control/emails-template/newsletter/stela-notify.html',{
                       
                })

            text_render = strip_tags(message)

            email = EmailMultiAlternatives(
                    'You Have a new subscriber',
                    text_render,
                    settings.STELA_EMAIL,
                    [settings.DEFAULT_EMAIL]
                        
                )
            email.attach_alternative(message, "text/html")
            email.send()

            response = JsonResponse({'success': 'success'})
            return response
        else:
            print(form.errors)
            error = str(form.errors)

            email_used = _('Data email with this Email already exists.')
            valid_email = _('Enter a valid email address.')

            if error == '<ul class="errorlist"><li>email<ul class="errorlist"><li>'+ email_used +'</li></ul></li></ul>':

                response = JsonResponse({'used': 'something went wrong, try again'})
                return response
            
            if error == '<ul class="errorlist"><li>email<ul class="errorlist"><li>'+ valid_email +'</li></ul></li></ul>':

                response = JsonResponse({'valid': 'something went wrong, try again'})
                return response
            
            response = JsonResponse({'error': 'something went wrong, try again'})
            return response
        
def editAddress(request, id):
    user = request.user
    address = Addresses.objects.get(pk=id)
    form = AddressForm(instance=address)
    alert = Notifications.objects.filter(user=user).order_by('-created')[:10]
    count = Notifications.objects.filter(user=user, status="No Read").count()

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)

        if form.is_valid():
            form.save()
            return redirect('/console/profile')

        else:
            print (form.errors)

    context = {
        
        'form': form,
        'alerts': alert,
        'count': count
    }

    return render(request, 'linkzone/costumer/update-address.html', context)

def get_invoice(request, id):
    invoice = InvoiceControl.objects.get(id=id)

    if invoice.recipt.tax:

        if invoice.recipt.discount:
            total = invoice.recipt.amount + invoice.recipt.tax - invoice.recipt.discount
        else:
            total = invoice.recipt.amount + invoice.recipt.tax
    else:
        if invoice.recipt.discount:
            total = invoice.recipt.amount - invoice.recipt.discount
        else:
            total = invoice.recipt.amount

    context = {
        'inv': invoice,
        'total': total
    }

    return render(request, 'linkzone/costumer/invoice.html', context)

def intentExpress(request):

    if request.method == 'POST':
        cart = Cart(request)
        total = str(cart.import_total())
        total = total.replace('.','')
        total = int(total)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='usd',
            metadata={
                'orderid':None
            },
            automatic_payment_methods={
                    'enabled': True,
                },
        )
    return JsonResponse({
        'clientSecret': intent['client_secret']
    })
    
def mercantilPayments(request):
    url = 'https://reseller.enom.com/interface.asp'
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
    ip = user_ip.split(',')[0] 
    headers = {
            'X-IBM-Client-Id': "81188330-c768-46fe-a378-ff3ac9e88824",
            'content-type': "application/json",
            'accept': "application/json"
            }

    MERCHANT_ID = 200284
    TERMINAL_ID = 31
    code_country="58" 
    # Client information
    CLIENT_IP = ip
    CLIENT_BROWSER = "undefined"
        
    if request.POST.get('action') == 'c2pPaykey':
        data_id = str(request.POST.get('clientid'))
        client_data=data_id.encode()
        data_phone = code_country + str(request.POST.get('phone'))
        client_phone=data_phone.encode()

        key = b'A11103402525120190822HB01'
        cipher = AESCipher(key)

        CLIENT_ID = cipher.encrypt(client_data)
        CLIENT_ID_CIPHER = CLIENT_ID.decode("utf-8")
        MOBILE_DESTINATION = cipher.encrypt(client_phone)
        MERCHANT_MOBILE = MOBILE_DESTINATION.decode("utf-8")
         
        conn = http.client.HTTPSConnection("apimbu.mercantilbanco.com")

        data = {
             "merchant_identify": {
                 "integratorId": TERMINAL_ID,
                 "merchantId": MERCHANT_ID,
                 "terminalId": "abcde"
             },
             "client_identify": {
                 "ipaddress": CLIENT_IP,
                 "browser_agent": CLIENT_BROWSER, 
                 "mobile": {
                     "manufacturer": "Samsung",
                     "model": "SOLSC",
                     "os_version": "",
                     "location": {
                        "lat": 0,
                        "lng": 0
                     }
                 }
             },
             "transaction_scpInfo": {
             "destination_id": CLIENT_ID_CIPHER,
             "destination_mobile_number": MERCHANT_MOBILE
	 }
         }

        payload=json.dumps(data)
        conn.request("POST", "/mercantil-banco/sandbox/v1/mobile-payment/scp", payload, headers)

        res = conn.getresponse()
        data = res.read()

        text=data.decode("utf-8")
        print(text)
        bank_raw=json.loads(text)

        try:
            error_value=bank_raw['error_list']
            error_response=error_value[0]['description']
            
            if error_response == "Identificacion destino no valida su encriptacion":

                 response = JsonResponse({'empty': "Por favor llene los campos requeridos."})
                 return response
                 
            else:
            
                response = JsonResponse({'failed': error_response})
                return response

        except:
                response = JsonResponse({'success': 'return something'})
                return response
    
    if request.POST.get('action') == 'c2pPay':
        euser = settings.ENOM_USER
        ekey = settings.ENOM_KEY
        cart = Cart(request)
        get_code = str('pm')+get_random_string(20).lower()
        #payment data 
        user = request.user

        data_id = str(request.POST.get('clientid'))
        client_data=data_id.encode()

        flat_amount = str(cart.total_ves())
        total = flat_amount.replace('.','')
        AMOUNT = int(total)
        BANK_ID = str(request.POST.get('bankcode'))
        
        data_phone = code_country + str(request.POST.get('phone'))
        client_phone=data_phone.encode()

        data_code = str(request.POST.get('optcode'))
        opt_code=data_code.encode()

        key = b'A11103402525120190822HB01'
        cipher = AESCipher(key)

        CLIENT_ID = cipher.encrypt(client_data)
        CLIENT_ID_CIPHER = CLIENT_ID.decode("utf-8")

        MOBILE_DESTINATION = cipher.encrypt(client_phone)
        MERCHANT_MOBILE = MOBILE_DESTINATION.decode("utf-8")
                
        MOBILE_ORIGIN = cipher.encrypt(b'584122681189')
        CLIENT_MOBILE = MOBILE_ORIGIN.decode("utf-8")

        GET_PURCHASE_KEY = cipher.encrypt(opt_code)
        PURCHASE_KEY = GET_PURCHASE_KEY.decode("utf-8")

        get_control_number=ControlFacturacion.objects.all().count()
        control_number = get_control_number + 1
        invoice_number = "get-news"+"-"+"14"+str(control_number)
        conn = http.client.HTTPSConnection("apimbu.mercantilbanco.com")

        data = {
        "merchant_identify": {
            "integratorId": TERMINAL_ID,
            "merchantId": MERCHANT_ID,
            "terminalId": "abcde"
        },
        "client_identify": {
            "ipaddress": CLIENT_IP,
            "browser_agent": "undefined",
            "mobile": {
            "manufacturer": "",
            "model": "SOLSC",
            "os_version": "",
            "location": {
                "lat": 37.422476,
                "lng": 122.08425
            }
            }
        },
        "transaction_c2p": {
            "trx_type": "compra",
            "payment_method": "c2p",
            "destination_id": CLIENT_ID_CIPHER,
            "invoice_number": invoice_number,
            "currency": "VES",
            "amount": AMOUNT,
            "destination_bank_id": BANK_ID,
            "destination_mobile_number": MERCHANT_MOBILE,
            "origin_mobile_number": CLIENT_MOBILE,
            "twofactor_auth": PURCHASE_KEY
        }
        }

        payload=json.dumps(data)
        conn.request("POST", "/mercantil-banco/sandbox/v1/payment/c2p", payload, headers)

        res = conn.getresponse()
        data = res.read()

        text=data.decode("utf-8")
        print(text)
        bank_raw=json.loads(text)

        
        try:
            error_value=bank_raw['error_list']
            error_response=error_value[0]['description']

            if error_response == "Numero de factura procesado previamente":
                twin_tranx = "Esta operacion ya fue procesada. Describa a soporte este N° Control" + " " + invoice_number

                response = JsonResponse({'twin': twin_tranx})
                return response

            elif error_response == "Segundo factor no valida su encriptacion":

                 response = JsonResponse({'empty': "Por favor ingrese la clave."})
                 return response
            else:
                 response = JsonResponse({'failed': error_response})
                 return response
        except:

            if bank_raw['transaction_c2p_response']['trx_status'] == "approved":

                total_paid=bank_raw['transaction_c2p_response']['amount']
                key_validator=bank_raw['transaction_c2p_response']['payment_reference']
                control_data=bank_raw['transaction_c2p_response']['invoice_number']
                master_user=UserBase.objects.get(username="emmerut")
                customer=Customer.objects.filter(email=user.email)
                if customer.exists():
                    customer.update(
                        userid=data_id,
                        owner=master_user,
                        full_name=user.full_name,
                        email=user.email,
                        address=user.address,
                        phone=user.phone_number
                    )
                else:
                    customer=Customer.objects.create(
                        owner=master_user,
                        userid=data_id,
                        full_name=user.full_name,
                        email=user.email,
                        address=user.address,
                        phone=user.phone_number
                    )
                cust=Customer.objects.get(email=user.email)
                if InvoiceControl.objects.filter(control_id=invoice_number).exists():
                    pass
                else:
                    invoice = BillingRecipt.objects.create(
                        owner=master_user,
                        customer=cust,
                        payment_option="VES",
                        option="Init Stela Website",
                        amount=cart.import_sub(),
                        tax=cart.import_tax()
                    )
                    InvoiceControl.objects.create(
                        recipt=invoice,
                        control_id=invoice_number
                    )
                    BillingRecipt.objects.filter(pk=invoice.pk).update(
                        status="Payeed",
                        is_generated=True
                    )
                get_host = get_current_site(request)
                order = Order.objects.create (
                        owner=request.user,
                        customer=cust,
                        email=user.email,
                        key_validator=key_validator,
                        transaction_id=get_code,
                        payment_option='PAGO MOVIL',
                        status="Payeed",
                        subtotal=cart.service_sub(),
                        taxes=cart.service_tax(),
                        payment_fee=cart.service_fee(),
                        profit=cart.service_sub() * Decimal(0.25),
                        total_paid=cart.service_total(),
                        section="Stela Websites"
                    )
                data=cart.serviceData()
                order_id = order.pk

                for item in data:
                    selection = StelaSelection.objects.filter(id=item.id)
                    counter=StelaSelection.objects.filter(id=item.id).count()
                    for select in selection:
                        vcs=VirtualCloud.objects.filter(owner=request.user)
                        if vcs.exists():
                            pass
                        else:
                            VirtualCloud.objects.filter(domain=select.domain).update(owner=request.user)

                        csu=CloudStorage.objects.filter(owner=request.user)
                        if csu.exists():
                            pass
                        else:
                            CloudStorage.objects.filter(domain=select.domain).update(owner=request.user)

                        dns=ZoneDNS.objects.filter(owner=request.user)
                        if dns.exists():
                            pass
                        else:
                            ZoneDNS.objects.filter(domain=select.domain).update(owner=request.user)

                        crc=ResquetsCloud.objects.filter(owner=request.user)
                        if crc.exists():
                            pass
                        else:
                            ResquetsCloud.objects.filter(domain=select.domain).update(owner=request.user)
                        
                        OrderItems.objects.create (
                                nameitem=item.integration.title,
                                order_id=order_id,
                                stela_selection=select,
                                amount=item.amount
                            )
                        modules=Modules.objects.filter(parent=item.integration)
                        for module in modules:
                            ItemServices.objects.create(
                                recipt=invoice,
                                field=module,
                                amount=module.price,
                                qty=1
                            )
                        # params = {
                        # 'command': 'Purchase',
                        # 'uid': settings.ENOM_USER,
                        # 'pw': settings.ENOM_KEY,
                        # 'EndUserIP': ip,
                        # 'sld': select.domain.name,
                        # 'tld': select.domain.tld,
                        # 'responsetype': 'Text'
                        # }
                        # response = requests.get(url, params=params)
                        # if response.ok:
                        #     Domains.objects.filter(name=select.domain.name, tld=select.domain.tld).update(owner=request.user, status="Payeed") 
                        # else:
                        #     Domains.objects.filter(name=select.domain.name, tld=select.domain.tld).update(owner=request.user)
                    
                    selection.update(status="Payeed")
                    
                    for loop in selection:
                        Notifications.objects.create (
                            user = order.owner,
                            status = "No Read",
                            title = _("You Have a New Project"),
                            description =_("We start jobs for ") + order.transaction_id,
                            section = order.section,
                            url = "https://emmerut.com/console/websites" 
                        )
                        Notifications.objects.create (
                            user = master_user,
                            status = "No Read",
                            title = _("New Project Request"),
                            description =_("CustomerID ") + cust.userid,
                            section = "Project Request",
                            url = "https://stela.emmerut.com/orders" 
                        )
                fetch=StelaPayments (
                            order=order_id,
                            user=master_user,
                            key_validator=get_code,
                            transaction_id=key_validator,
                            payment_option='Pago Movil',
                            subtotal=cart.import_sub(),
                            taxes=cart.import_tax(),
                            profit=cart.import_total() * Decimal(0.25),
                            payment_fee=cart.import_fee(),
                            total_paid=cart.import_total(),
                            host=get_host.domain
                        )
                fetch.save()
                if ControlFacturacion.objects.filter(control_id=control_data).exists():
                    pass
                else:
                    factura_control = ControlFacturacion.objects.create(
                        owner=master_user,
                        customer=cust,
                        order=order,
                        control_id=control_data,
                        base=cart.servicio_base(),
                        iva=cart.servicio_iva(),
                        total=cart.total_ves(),
                    )
                    factura_pk = factura_control.pk
                    FacturaItems.objects.create(
                        order_id=factura_pk,
                        origin=order,
                    )
                html_content = render_to_string('stela_control/emails-template/orders/stela_order_placed_ves.html', {
                            'order': order,
                            'subtotal': cart.servicio_base(),
                            'tax': cart.servicio_iva(),
                            'fee': cart.servicio_fee(),
                            'total': cart.total_ves(),
                            'count': counter,
                            'selection': selection       
                        })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            'Su compra fue procesada exitosamente',
                            text_content,
                            settings.STELA_EMAIL,
                            [user.email]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                
                message = render_to_string('stela_control/emails-template/payments/sale_notification.html',{
                            
                        })

                text_render = strip_tags(message)

                email = EmailMultiAlternatives(
                        _('You Have a Sale'),
                        text_render,
                        settings.STELA_EMAIL,
                        [settings.DEFAULT_EMAIL]
                                    
                    )
                email.attach_alternative(message, "text/html")
                email.send()

                cart.stela_clear()
                return JsonResponse({'success': 'Thanks for your purchase'})


def test(request):

    context = {

    }
    return render(request, 'test.html', context)

@login_required
def paymentPaypal(request):
    url = 'https://reseller.enom.com/interface.asp'
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
    ip = user_ip.split(',')[0] 
    res = requests.get('http://ip-api.com/json/' + ip)
    data_one = res.text
    data = json.loads(data_one)
    PPClient = PaypalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user = request.user
    try:
        requestorder = OrdersGetRequest(data)
        response = PPClient.client.execute(requestorder)
        get_host = get_current_site(request)
        cart = Cart(request)
        get_code = str('PP')+get_random_string(10).lower()
        master_user=UserBase.objects.get(username="emmerut")
        customer=Customer.objects.filter(email=user.email)
        get_control_number=BillingRecipt.objects.filter(is_generated=True, is_budget=False, payment_option="USD",).count()
        control_number = get_control_number + 1
        invoice_number = "DB"+"-"+"0"+str(control_number)
        print(cart.import_total())
        print(response.result.purchase_units[0].amount.value)
        if customer.exists():
            pass
        else:
            customer=Customer.objects.create(
                owner=master_user,
                userid=user.username,
                full_name=user.full_name,
                email=user.email,
                address=user.address,
                phone=user.phone_number
            )
        cust=Customer.objects.get(email=user.email)
        if InvoiceControl.objects.filter(control_id=invoice_number).exists():
            customer.update(
                owner=master_user,
                full_name=user.full_name,
                email=user.email,
                address=user.address,
                phone=user.phone_number
            )
        else:
            invoice = BillingRecipt.objects.create(
                owner=master_user,
                customer=cust,
                payment_option="USD",
                option="Init Stela Website",
                amount=cart.import_sub(),
                tax=cart.import_tax()
            )
            InvoiceControl.objects.create(
                recipt=invoice,
                control_id=invoice_number
            )
            BillingRecipt.objects.filter(pk=invoice.pk).update(
                status="Payeed",
                is_generated=True
            )
            
        order = Order.objects.create (
                owner=request.user,
                customer=cust,
                email=response.result.payer.email_address,
                key_validator=response.result.id,
                transaction_id=get_code,
                payment_option='Paypal',
                status="Payeed",
                subtotal=cart.service_sub(),
                taxes=cart.service_tax(),
                payment_fee=cart.service_fee(),
                profit=cart.service_sub() * Decimal(0.25),
                total_paid=cart.service_total(),
                section="Stela Websites"
            )
        data=cart.serviceData()
        order_id = order.pk

        for item in data:
            selection = StelaSelection.objects.filter(id=item.id)
            counter=StelaSelection.objects.filter(id=item.id).count()
            for select in selection:
                vcs=VirtualCloud.objects.filter(owner=request.user)
                if vcs.exists():
                    pass
                else:
                    VirtualCloud.objects.filter(domain=select.domain).update(owner=request.user)

                csu=CloudStorage.objects.filter(owner=request.user)
                if csu.exists():
                    pass
                else:
                    CloudStorage.objects.filter(domain=select.domain).update(owner=request.user)

                dns=ZoneDNS.objects.filter(owner=request.user)
                if dns.exists():
                    pass
                else:
                    ZoneDNS.objects.filter(domain=select.domain).update(owner=request.user)

                crc=ResquetsCloud.objects.filter(owner=request.user)
                if crc.exists():
                    pass
                else:
                    ResquetsCloud.objects.filter(domain=select.domain).update(owner=request.user)

                OrderItems.objects.create (
                        nameitem=item.integration.title,
                        order_id=order_id,
                           stela_selection=select,
                        amount=item.amount
                    )

                modules=Modules.objects.filter(parent=item.integration)
                for module in modules:
                    ItemServices.objects.create(
                        recipt=invoice,
                        field=module,
                        amount=module.price,
                        qty=1
                    )
                # params = {
                #     'command': 'Purchase',
                #     'uid': settings.ENOM_USER,
                #     'pw': settings.ENOM_KEY,
                #     'EndUserIP': ip,
                #     'sld': select.domain.name,
                #     'tld': select.domain.tld,
                #     'responsetype': 'Text'
                #     }
                # response = requests.get(url, params=params)
                # if response.ok:
                   #     Domains.objects.filter(name=select.domain.name, tld=select.domain.tld).update(owner=request.user, status="Payeed") 
                # else:
                #     Domains.objects.filter(name=select.domain.name, tld=select.domain.tld).update(owner=request.user)

            selection.update(status="Payeed")
            UserBase.objects.filter(pk=request.user.pk).update(cloud_services=True)
        StelaPayments.objects.create (
                order=order_id,
                user=master_user,
                key_validator=response.result.id,
                transaction_id=get_code,
                payment_option='Paypal',
                subtotal=cart.import_sub(),
                taxes=cart.import_tax(),
                profit=cart.import_sub() * Decimal(0.25),
                payment_fee=cart.import_fee(),
                total_paid=response.result.purchase_units[0].amount.value,
                host=get_host.domain
            )

            
        cart.stela_clear()
        for loop in selection:
            Notifications.objects.create (
                user = request.user,
                status = "No Read",
                title = _("You Have a New Project"),
                description =_("We start jobs for ") + order.transaction_id,
                section = order.section,
                url = "https://emmerut.com/console/websites" 
            )
            Notifications.objects.create (
                user = master_user,
                status = "No Read",
                title = _("New Project Request"),
                description =_("CustomerID ") + cust.userid,
                section = "Project Request",
                url = "https://stela.emmerut.com/orders" 
            )

        html_content = render_to_string('stela_control/emails-template/orders/stela_order_placed.html', {
                        'order': order,
                        'subtotal': cart.import_sub(),
                        'tax': cart.import_tax(),
                        'fee': cart.import_fee(),
                        'total': cart.import_total(),
                        'count': counter,
                        'selection': selection       
                    })

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
                    _('Your purchase was processed successfully'),
                    text_content,
                    settings.STELA_EMAIL,
                       [user.email]                           
            )
        email.attach_alternative(html_content, "text/html")
        email.send()
                    
        message = render_to_string('stela_control/emails-template/payments/sale_notification.html',{
                            
            })

        text_render = strip_tags(message)

        email = EmailMultiAlternatives(
                _('You Have a Sale'),
                text_render,
                settings.STELA_EMAIL,
                [settings.DEFAULT_EMAIL]
                                
            )
        email.attach_alternative(message, "text/html")
        email.send()
        return JsonResponse({'success': 'Thanks for your purchase'})
        
    except Exception as e:
        print(f"Se produjo un error: {e}")
        return JsonResponse({'failed': 'Internal Failure'})

def orderGenerator(data):
    Order.objects.create(key_validator=data)
    
@login_required   
def paymentStripe(request):
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
    ip = user_ip.split(',')[0]
    url = 'https://reseller.enom.com/interface.asp'
    cart = Cart(request)
    get_host = get_current_site(request)
    user = request.user
    data=cart.serviceData()
    get_code = str('Epay')+get_random_string(8).upper()
    master_user=UserBase.objects.get(username="emmerut")
    customer=Customer.objects.filter(email=user.email)
    get_control_number=BillingRecipt.objects.filter(is_generated=True, is_budget=False, payment_option="USD",).count()
    control_number = get_control_number + 1
    invoice_number = "DB"+"-"+"0"+str(control_number)

    if customer.exists():
        customer.update(
            owner=master_user,
            userid=user.username,
            full_name=user.full_name,
            email=user.email,
            address=user.address,
            phone=user.phone_number
        )
    else:
        customer=Customer.objects.create(
            owner=master_user,
            userid=user.username,
            full_name=user.full_name,
            email=user.email,
            address=user.address,
            phone=user.phone_number
        )
    cust=Customer.objects.get(email=user.email)
    if InvoiceControl.objects.filter(control_id=invoice_number).exists():
        pass
    else:
        invoice = BillingRecipt.objects.create(
            owner=master_user,
            customer=cust,
            payment_option="USD",
            option="Stela Website",
            amount=cart.import_sub(),
            tax=cart.import_tax()
        )
        InvoiceControl.objects.create(
            recipt=invoice,
            control_id=invoice_number
        )
        BillingRecipt.objects.filter(pk=invoice.pk).update(
            status="Payeed",
            is_generated=True
        )
    order_key = request.POST.get('order_key')
    order = Order.objects.filter(key_validator=order_key)
    if order.exists():
        order.update (
            owner=request.user,
            customer=cust,
            email=user.email,
            key_validator=order_key,
            transaction_id=get_code,
            payment_option='Stela Payments',
            status="Payeed",
            subtotal=cart.service_sub(),
            taxes=cart.service_tax(),
            payment_fee=cart.service_fee(),
            profit=cart.service_sub() * Decimal(0.25),
            total_paid=cart.service_total(),
            section="Stela Websites"
            )
        get_order = Order.objects.get(key_validator=order_key)
        order_id = get_order.pk

        for item in data:
            selection = StelaSelection.objects.filter(id=item.id)
            counter=StelaSelection.objects.filter(id=item.id).count()

            for select in selection:
                vcs=VirtualCloud.objects.filter(owner=request.user)
                if vcs.exists():
                    pass
                else:
                    VirtualCloud.objects.filter(domain=select.domain).update(owner=request.user)

                csu=CloudStorage.objects.filter(owner=request.user)
                if csu.exists():
                    pass
                else:
                    CloudStorage.objects.filter(domain=select.domain).update(owner=request.user)

                dns=ZoneDNS.objects.filter(owner=request.user)
                if dns.exists():
                    pass
                else:
                    ZoneDNS.objects.filter(domain=select.domain).update(owner=request.user)

                crc=ResquetsCloud.objects.filter(owner=request.user)
                if crc.exists():
                    pass
                else:
                    ResquetsCloud.objects.filter(domain=select.domain).update(owner=request.user)

                modules=Modules.objects.filter(parent=item.integration)
                for module in modules:
                    ItemServices.objects.create(
                        recipt=invoice,
                        field=module,
                        amount=module.price,
                        qty=1
                )   
                OrderItems.objects.create (
                        nameitem=item.integration.title,
                        order_id=order_id,
                        stela_selection=select,
                        amount=item.amount
                    )
                # params = {
                #     'command': 'Purchase',
                #     'uid': settings.ENOM_USER,
                #     'pw': settings.ENOM_KEY,
                #     'EndUserIP': ip,
                #     'sld': select.domain.name,
                #     'tld': select.domain.tld,
                #     'responsetype': 'Text'
                #     }
                # response = requests.get(url, params=params)
                # if response.ok:
                #     Domains.objects.filter(name=select.domain.name, tld=select.domain.tld).update(owner=request.user, status="Payeed") 
                # else:
                #     Domains.objects.filter(name=select.domain.name, tld=select.domain.tld).update(owner=request.user)
                    
        selection.update(status="Payeed")
        UserBase.objects.filter(pk=request.user.pk).update(cloud_services=True)
        for loop in selection:
            Notifications.objects.create (
                user = request.user,
                status = "No Read",
                title = _("You Have a New Project"),
                description =_("We start jobs for ") + get_order.transaction_id,
                section = get_order.section,
                url = "https://emmerut.com/console/websites" 
            )
            Notifications.objects.create (
                user = master_user,
                status = "No Read",
                title = _("New Project Request"),
                description =_("CustomerID ") + cust.userid,
                section = "Project Request",
                url = "https://stela.emmerut.com/orders" 
            )
        StelaPayments.objects.create (
                    order=order_id,
                    user=master_user,
                    key_validator=order_key,
                    transaction_id=get_code,
                    payment_option='Stripe',
                    subtotal=cart.import_sub(),
                    taxes=cart.import_tax(),
                    profit=cart.import_sub() * Decimal(0.25),
                    payment_fee=cart.import_fee(),
                    total_paid=cart.import_total(),
                    host=get_host.domain
                )

        cart.stela_clear()  
        html_content = render_to_string('stela_control/emails-template/orders/stela_order_placed.html', {
                        'order': order,
                        'subtotal': cart.import_sub(),
                        'tax': cart.import_tax(),
                        'fee': cart.import_fee(),
                        'total': cart.import_total(),
                        'count': counter,
                        'selection': selection       
                    })

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
                    _('Your purchase was processed successfully'),
                    text_content,
                    settings.STELA_EMAIL,
                    [user.email]                           
            )
        email.attach_alternative(html_content, "text/html")
        email.send()
                
        message = render_to_string('stela_control/emails-template/payments/sale_notification.html',{
                            
            })

        text_render = strip_tags(message)

        email = EmailMultiAlternatives(
                _('You Have a Sale'),
                text_render,
                settings.STELA_EMAIL,
                [settings.DEFAULT_EMAIL]
                                    
            )
        email.attach_alternative(message, "text/html")
        email.send()

        return JsonResponse({'success': 'Thanks for your purchase'})
        
    else:
        return JsonResponse({'failed': 'Key validator invalid'})


@login_required
def paymentLoader(request):
    
    return render(request, 'linkzone/costumer/payments/payment-loader.html')

def billingPayLoader(request, reciptid, orderid):
    inv=BillingRecipt.objects.get(pk=reciptid)
    order=Order.objects.get(pk=orderid)
    context ={
        'inv': inv,
        'order': order
    }
    return render(request, 'linkzone/costumer/billing/payment-loader.html', context)

def order_placed(request):
    
    context = {
       
    }
    return render(request, 'linkzone/costumer/payments/order-placed.html', context)

