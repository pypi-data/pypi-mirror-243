from datetime import date
from django.db.models import Sum
from accounts.forms import UserEditForm
from accounts.models import UserBase
from django.forms import formset_factory
from django.http.response import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from linkzone.cart import Cart
from stela_control.models import (
    ClubPoints, Order, OrderItems, BillingRecipt, PetData,ChatSupport,Inventory, 
    Reviews, StelaSelection, Content, LegalProvision, SitePolicy, Support, SupportResponse
    )
from .forms import ContactForm, ReadOnlySupportFormCostumer, SupportForm, SupportForm
from stela_control.forms import ReviewsForm
# from .models import Comment, CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.forms import Textarea, inlineformset_factory
from django.template.loader import render_to_string, get_template
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@login_required
def console(request):
    
    return render(request, 'nexus/index.html')

def profile(request):
    owner = request.user
    pets = PetData.objects.filter(owner_id=owner.id)
    form = PetDataForm()
    if request.method == "POST":
        call = request.POST.get('form-id')
        action = request.POST.get('action')

        print(call)
        print(action)
        
        if call == "submitForm":
            form = PetDataForm(request.POST, request.FILES)
            if form.is_valid():
                pet = form.save(commit=False)
                pet.owner = request.user
                pet.save()
                    
                response = JsonResponse({'success': 'return something'})
                return response
            
        if call == "updatePet":
            pk=request.POST.get('obj-id')
            pet=PetData.objects.get(pk=pk)

            form=PetDataForm(request.POST, request.FILES, instance=pet)
            if form.is_valid():
                form.save()

                response = JsonResponse({'success': 'return something'})
                return response
        
        if call == "Update":
            pk=request.POST.get('pk')
            profile=UserBase.objects.get(pk=pk)

            form=UserEditForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()

                response = JsonResponse({'success': 'return something'})
                return response
        
        if action == "getProfile":
            obj_id=request.POST.get('id')
            obj=UserBase.objects.get(pk=obj_id)
            form=UserEditForm(instance=obj)

            obj_data = render_to_string('stela_control/load-data/form-clean.html', {
                            'form': form,  
                })

            response = JsonResponse({
                'response': obj_data,
                'pk': obj.pk
                })
            return response

        if action == "getPet":
            obj_id=request.POST.get('id')
            obj=PetData.objects.get(pk=obj_id)
            form=PetDataForm(instance=obj)

            obj_data = render_to_string('stela_control/load-data/form-clean.html', {
                            'form': form,  
                })

            response = JsonResponse({
                'response': obj_data,
                'pk': obj.pk
                })
            return response
        
        if action == "removePet":
            pet_id = request.POST.get('id')
            pet = PetData.objects.get(pk=pet_id)
            pet.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
    context= {
        'pets': pets,
        'form': form
        }
    return render(request, 'nexus/profile/profile.html', context)

def edit_profile(request):
    user = request.user
    form = UserEditForm(instance=user)

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
           form.save()
           
           messages.success(request, "Changes made successfully")
           return redirect('nexus:profile')

    context={
        'form': form
    }

    return render(request, 'nexus/profile/edit_profile.html', context)

def add_pet(request):
    user = request.user
    formset = formset_factory(PetDataForm, extra=1)

    if request.method == 'POST':
        petdata = formset(request.POST, request.FILES)
        
        if petdata.is_valid():

           for form in petdata:
                data = form.save(commit=False)
                data.owner = user
                data.save()
           
           messages.success(request, "Changes made successfully")
           return redirect('nexus:profile')

    context={
        'formset': formset
    }
    return render(request, 'nexus/pets/add-pet.html', context)

# def edit_pet(request, id):
#     pet = PetData.objects.get(id=id)
#     form = PetForm(instance=pet)

#     if request.method == 'POST':
#         form = PetForm(request.POST, request.FILES, instance=pet)
        
#         if form.is_valid():
#            form.save()
           
#            messages.success(request, "Changes made successfully")
#            return redirect('nexus:profile')

#     context={
#         'form': form
#     }

#     return render(request, 'nexus/pets/modify-pet.html', context)

def delete_pet(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        petid = int(request.POST.get('petid'))
        pet_selection = StelaSelection.objects.filter(pet_id=petid)
        if pet_selection.exists():
            for pet in pet_selection:
                cart.delete(select=pet.id)
        petdata = PetData.objects.get(id=petid)
        petdata.delete()
        response = JsonResponse({'success': 'return something'})
        return response

# Order View Store.
@login_required
def appointments(request):
    user = request.user
    present = date.today()
    orders = Order.objects.filter(owner=user, status="Payeed").order_by('-created')[:6]
    filter = request.POST.get('term')
    q = request.POST.get('qs')

    if filter:
        orders = Order.objects.filter(owner=user, status="Payeed").order_by(filter)
    
    if q:
        orders = Order.objects.filter(owner=user, status="Payeed", appointment_date=q)

    context ={
        'orders': orders,
        'present': present,

    }
    return render(request, 'nexus/booking/appointments.html', context)

def autocompleteBooking(request):
  if 'term' in request.GET:
      q = Order.objects.filter(appointment_date__icontains=request.GET.get('term'))
      date = list()
      for obj in q:
          date.append(obj.appointment_date)
      return JsonResponse(date, safe=False)

@login_required
def order_detail(request, id):
     order = Order.objects.get(pk=id)
     appointmentDate = order.appointment_date
     shippingDateFormat = appointmentDate.strftime("%c")
     context ={
        'order':order, 'date_shipping_format':shippingDateFormat,
        }
     return render(request, 'nexus/booking/order_detail.html', context)


@login_required
def comment_view(request, id):
    lang = request.LANGUAGE_CODE
    form = ReviewsForm()
    orderitem = OrderItems.objects.raw('SELECT DISTINCT ON (service_id) * FROM siteapp_orderitem WHERE order_id=%s', [id])
    context ={
        'service': orderitem,
        'form': form
    }
    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            ip = request.META.get('REMOTE_ADDR')
            rate = form.cleaned_data['rate']
            comment = form.cleaned_data['comment']

            for item in orderitem:
                Reviews.objects.create(
                    order_id =id,
                    user_id=request.user.id,
                    product_id=item.service.id,
                    rate = rate,
                    comment = comment,
                    ip = ip
                )
            # current_site = get_current_site(request)

            # html_content = render_to_string('emails/linkzone/support_email.html', {
            #             'domain': current_site.domain
            #             'user': request.user.id,
            #             'service': orderitem,
            #     })
            # text_content = strip_tags(html_content)

            # email = EmailMultiAlternatives(
            #     'Hemos registrado tu caso',
            #     text_content,
            #     settings.STELA_EMAIL,
            #     [settings.NOTIFY_EMAIL]
               
            # )
            # email.attach_alternative(html_content, "text/html")
            # email.send()
            Order.objects.filter(id=id).update(order_status=True)
            messages.success(request, "Review Send, Thanks")
            return redirect ('nexus:appointments')

    return render(request, 'nexus/booking/review.html', context)

@login_required
def clubpoints(request):
    total_points = ClubPoints.objects.filter(user=request.user).aggregate(total=Sum('points'))
    club_orders = ClubPoints.objects.filter(user=request.user)
    top_club = ClubPoints.objects.all().values('user__username').annotate(total=Sum('points')).order_by('-total')[:3]
    context = {
        'points': total_points,
        'club_orders': club_orders,
        'top_club': top_club
    }

    return render(request, 'nexus/clubpoints/index.html', context)

@login_required
def support_view(request):
    current_user = request.user
    support_list = Support.objects.filter(user_id=current_user.id)
    q = request.POST.get('qs')
    date = request.POST.get('date')

    if q: 
        support_list = Support.objects.filter(ticket__icontains=q, user_id=current_user.id).order_by('-id')

    if date:
        date_min = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=int(date)), datetime.time.min)
        today = timezone.now()
        support_list = Support.objects.filter(user_id=current_user.id, created__range=[date_min, today]).order_by('-id')
    
    page = request.GET.get('page', 1)

    paginator = Paginator(support_list, 5)
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)

    context ={
        'support': lists
        }
    return render(request, 'nexus/user/issue_center/support.html', context)

@login_required
def create_case(request, id):
    current_user = request.user
    order = Order.objects.get(id=id)
    ticket_gen = str('ISSUE-')+get_random_string(6).upper()
    user = UserBase.objects.get(id=current_user.id)
    email_user = user.email
    form = SupportForm()
    context = {
            'form': form,
            'order': order
            }
    if request.method == 'POST':
        supportform = SupportForm(request.POST, request.FILES)
        
        if supportform.is_valid():
            subject = supportform.cleaned_data['option']

            supportcase = supportform.save(commit=False)
            supportcase.user_id = current_user.id
            supportcase.ticket = ticket_gen
            supportcase.email = email_user
            supportcase.save()

            current_site = get_current_site(request)

            html_content = render_to_string('emails/transactionals/support_email.html', {
                        'user': current_user,
                        'ticket': ticket_gen,
                })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                'We have registered your case',
                text_content,
                settings.SUPPORT_EMAIL,
                [email_user]
               
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            message = render_to_string('stela_control/emails-template/support_notification.html',{
                    'ticket': supportcase.ticket,
                    'subject': supportcase.option,
                    'user': current_user.username,
                    'date': supportcase.created

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
            return redirect('nexus:support')

    return render(request, 'nexus/user/issue_center/create_case.html', context)

@login_required
def update_case(request, id):
    current_user = request.user
    support = Support.objects.get(id=id)
    email_user = support.email
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
                'responses': responses
             }
    else:
        context = { 
                'readsupportform': readsuportform,
                'support': support,
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
                response.user_id = current_user.id
                response.case = parent
                response.save()

            html_content = render_to_string('stela_control/emails-template/support_notification.html', {
                        'ticket': response.case.ticket,
                        'subject': response.case.option,
                        'user': response.user.username,
                        'update': datetime.now(),
                        })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                'User has answered his case',
                text_content,
                settings.STELA_EMAIL,
                [settings.DEFAULT_EMAIL]
               
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, "Changes made successfully")
            return redirect('nexus:support')

    return render(request, 'nexus/user/issue_center/update_support.html', context)

def autocompleteSupport(request):
  if 'term' in request.GET:
      q = Support.objects.filter(ticket__icontains=request.GET.get('term'))
      titles = list()
      for search in q:
          titles.append(search.ticket)
      return JsonResponse(titles, safe=False)

def news(request, id):
    news = Content.objects.get(id=id)

    context = {
        'news': news
    }
    
    return render(request, 'link-zone/news/index.html', context)

def policy(request):
    policy = SitePolicy.objects.get(policy__icontains='Políticas')
    legal = LegalProvision.objects.filter(policy_id=policy.id).order_by('id')
    context = {
        'legal': legal,
        'policy': policy
    }
    
    return render(request, 'link-zone/docs_site/privacy.html', context)

def terms(request):
    policy = SitePolicy.objects.get(policy__icontains='Términos')
    legal = LegalProvision.objects.filter(policy_id=policy.id).order_by('id')
    context = {
        'legal': legal,
        'policy': policy
    }
    
    return render(request, 'link-zone/docs_site/terms.html', context)

def about_us(request):
    who_we_are = LegalProvision.objects.get(clause__icontains='¿quienes')
    mision = LegalProvision.objects.get(clause__icontains='misi')
    vision = LegalProvision.objects.get(clause__icontains='visi')
    target = LegalProvision.objects.get(clause__icontains='objet')
    plus = LegalProvision.objects.get(clause__icontains='¿que nos')
    values = LegalProvision.objects.get(clause__icontains='valores')
    context = {
        'sec1': who_we_are,
        'sec2': mision,
        'sec3': vision,
        'sec4': target,
        'sec5': plus,
        'sec6': values,
        'policy': policy
    }
    
    return render(request, 'link-zone/docs_site/about_us.html', context)

def contact(request):
    form = ContactForm()
    if request.user.is_authenticated:
       user = request.user
    else:
       user = 'anonimus'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email_user = form.cleaned_data['email']
            #subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            form.save()
            
            current_site = get_current_site(request)

            html_content = render_to_string('emails/linkzone/contact_email.html', {
                        'message': message,
                        })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                'Hemos recibido tu requerimiento',
                text_content,
                settings.CONTACT_EMAIL,
                [email_user]
               
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            message = render_to_string('emails/notify_admin.html',{
                    'site': current_site,
                    'user': user

            })
            text_render = strip_tags(message)

            email = EmailMultiAlternatives(
                'Han envíado un nuevo mensaje',
                text_render,
                settings.CONTACT_EMAIL,
                [settings.CLIENTES_RECIPIENT]
               
            )
            email.attach_alternative(message, "text/html")
            email.send()

            messages.success(request, "Su mensaje ha sido registrado exitosamente")
            return redirect('linkzone:contact')

    context = {
        'form':form
    }

    return render(request, 'link-zone/contact/create.html', context)

def get_invoice(request, id):
    try:
        order = Order.objects.get(id=id)
        invoice = BillingRecipt.objects.get(order_id=order.id)
        orderitem = OrderItems.objects.get(order_id=id)
    except:
        return HttpResponse('not found')
    
    data ={
        'orderitem': orderitem,
        'order_id': order.id,
        'transaction_id': order.transaction_id,
        'user_email': order.user.email,
        'name': order.user.first_name,
        'order': order,
        'subtotal': order.subtotal_ves,
        'iva': order.taxes_ves,
        'total': order.total_paid_ves,
        'number': invoice.number
    }
    
    if Order.objects.filter(payment_method='VES'):
        pdf = render_to_pdf('link-zone/payment/invoice_ves.html', data)
    else:
        pdf = render_to_pdf('link-zone/payment/invoice_usd.html', data)

    return HttpResponse(pdf, content_type='application/pdf')




