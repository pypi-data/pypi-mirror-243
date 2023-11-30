from django.utils import timezone
from pytz import country_timezones
from django.db.models import F
import time, ast, boto3, json, openai, binascii, http.client, requests, base64, pickle, datetime, stripe, os
from datetime import timedelta 
from bs4 import BeautifulSoup
from .functions import caption_optimizer
import re, phonenumbers
from crispy_forms.utils import render_crispy_form
from phonenumbers import geocoder, carrier
from dateutil.relativedelta import relativedelta
from django.contrib.sessions.backends.db import SessionStore
from django.template.defaultfilters import date
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from linkzone.context_processors import Cart, SiteData
from mercantil_cypher.mercantil_aes import AESCipher
from paypalcheckoutsdk.orders import OrdersGetRequest
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.crypto import get_random_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.forms import Textarea, formset_factory, inlineformset_factory, modelformset_factory
from django.db.models import Sum
from django.contrib.auth.decorators import user_passes_test
from linkzone.forms import (
    ContactForm, ResponseContactForm, ResponseContactFormDisabled
)
from geolocation.models import Country
from cloud.models import (
    VirtualCloud, ZoneDNS, CloudStorage, ResquetsCloud, UsageCloud, Domains
)
from .models import (
    Content, Wallet, DataEmail, 
    DynamicBullets, Newsletter, SendMoney, BillingRecipt,
    ItemProducts, ItemServices, ItemDiscount,  
    InvoiceControl, BudgetControl, StelaSelection, 
    StelaItems, Templates, Order, StelaPayments, PathControl, 
    ControlFacturacion, FacturaItems, TemplateSections, StelaColors,
    ModuleItems, ProStelaData, OrderItems, Inventory, Modules, 
    Variants, Sizes, Gallery, Bulletpoints, Sizes, VariantsImage, Customer, 
    Budget, Category, SitePolicy, LegalProvision, SupportResponse, 
    Support, ChatSupport, SiteControl, ItemCloud, FacebookPage, InstagramAccount, FacebookPostPage, FacebookPageComments, FacebookPageCommentsReply, FacebookPageConversations,
    FacebookPageEvent,  FacebookPageLikes, FacebookPageMessages, FacebookPageShares, FacebookPostMedia, IGMediaContent, FacebookPageImpressions,
    IGPost, IGUserTag, FAQ, SetFaq, Poll, Contact,Comments, PaypalClient, Notifications,
    IGPostMetric, IGCarouselMetric, IGReelMetric, IGStoriesMetric, Company, SocialLinks, ProStelaExpert, ProStelaUsage, Reviews
    
)
from google.oauth2 import service_account
from django_hosts.resolvers import reverse
from linkzone.forms import *
from django.http.response import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate, logout
from accounts.forms import LoginForm
from django.shortcuts import redirect, render, get_object_or_404 
from django.contrib import messages
from accounts.forms import RegistrationForm, UserEditForm
from accounts.models import UserBase
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from accounts.token import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import (
    SiteNewsForm, FAQForm, NewsletterForm,
    PolicyForm, UserForm, BillingForm, BillingDiscountForm, 
    ModulesForm,TemplateForm, ProductForm, StylesForm, 
    TempSecForm, ColorsForm, VariantForm, SizeForm, GalleryForm, BulletForm, 
    ServiceForm, VariantImageForm, BillingChargeFormDynamic, BillingChargeFormPOS, 
    BillingFormSuscription, AppstelaForm, LegalProvitionForm, StelaAboutForm, 
    PathForm, MediaForm, FooterContentForm, categForm, 
    BulletSimpleForm, CommentsFormBlog, ReadOnlySupportForm, WalletForm,
    FbPostForm, FacebookEventsForm, IGPostForm, IGMediaForm, RequiredFormSet, CompanyForm, SocialMediaForm,
    SendGridForm,BlogForm, ContentForm, RedirectContentForm, StickerContentForm, ContentDynamicForm,
    SimpleContentForm, SetFaqForm, ImageContentForm, TextContentForm, AboutContentForm, ReviewsForm
    )
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from google.oauth2 import service_account
from google.cloud import monitoring_v3
from django.http import JsonResponse
from facebook_business.api import FacebookAdsApi
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.business import Business
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#coreStela
@login_required
def clean_register(request):

    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST': 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/websites')
            else:
                msg = 'credenciales invalidas'

        else: 
            msg = 'error validando usuario'
   
    event = "Clean Register"
    context={
        'event': event,
        'form': form,
        'msg':msg
       
    }

    return render(request, 'accounts/user/clean_user.html',context)

@login_required
def websites(request):
    lang=request.LANGUAGE_CODE
    services = Inventory.objects.filter(type="Service")
    templates = Templates.objects.filter(status="Active")
    dark = request.COOKIES[settings.SESSION_COOKIE_NAME]
    context = {
        'services': services,
        'templates': templates,
        'dark': dark,
     }
    return render(request, 'stela_control/site/sections/website.html', context)

def suscription(request, pk):
    lang=request.LANGUAGE_CODE
    selection = StelaSelection.objects.get(pk=pk)
    integration = Inventory.objects.get(pk=selection.integration.pk)
    templates = Templates.objects.filter(status="Active")
    dark = request.COOKIES[settings.SESSION_COOKIE_NAME]
    context = {
        'integration': integration,
        'templates': templates,
        'selection': selection,
        'dark': dark,
     }
    return render(request, 'stela_control/site/sections/suscriptions.html', context)

@login_required
def requestAPI(request): 
    action = request.POST.get('action')
    obj = request.POST.get('queryid')
    print(action)
    if not obj:
        obj = 0

    stelaquery=ProStelaData.objects.filter(pk=obj)
        
    if action == 'callProStelaCustom':
        start_time = time.time()
        prompt_limit= 10
        openai.api_key = settings.API_KEY
        
        prompt = request.POST.get('prompt')

        qtitle=str(prompt)
        string=qtitle.split()
        title=" ".join(string[:8])
        
        if stelaquery.exists():
                text=ProStelaData.objects.get(id=obj)
                messages=ast.literal_eval(text.chatbox)
                storage_data=ast.literal_eval(text.storage_data)
        else:
            messages = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'}
                    ]
            storage_data = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'}
                    ]

        while action != 'end':
            if len(messages) > prompt_limit:
                del messages[6:9]
            messages.append({'role': 'user', 'content': prompt})
            storage_data.append({'role': 'user', 'content': prompt})
            print(len(messages))
            try:
                response = openai.chat.completions.create (
                    model='gpt-3.5-turbo-16k',
                    messages=messages,
                    temperature=0.2
                )
                tokens=response.usage.total_tokens
                response_content = response.choices[0].message.content
                response_content.replace('\n', '<br>')
                    
                if tokens < 4097:
                    messages.append({"role": "assistant", "content":response_content})
                    storage_data.append({"role": "assistant", "content":response_content})

                    
                chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                    'messages': storage_data,
                    'user': request.user,
                    })
                
                end_time = time.time()
                response_time = end_time - start_time
                print(response_time)

                if stelaquery.exists():
                    stelaquery.update(
                        chatbox=messages, 
                        storage_data=storage_data,
                        response_time=response_time
                    )
                    qs=ProStelaData.objects.get(id=obj)
                else:
                    qs=ProStelaData.objects.create(
                        title=title,
                        user=request.user,
                        section="custom",
                        chatbox=messages,
                        storage_data=storage_data,
                        response_time=response_time
                    )
                ProStelaUsage.objects.create(
                    prompt=qs,
                    tokens=tokens
                )
                if tokens < 4097:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        })
                else:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        'alert1': 'event'
                        })
                
            except openai.APIError as e:
                    return JsonResponse({
                        'alert2': 'event'
                        })
                  
    if action == 'callProStelaMarketing':
        start_time = time.time()
        prompt_limit= 10
        openai.api_key = settings.API_KEY
        
        prompt = request.POST.get('prompt')

        qtitle=str(prompt)
        string=qtitle.split()
        title=" ".join(string[:8])
        
        if stelaquery.exists():
                text=ProStelaData.objects.get(id=obj)
                messages=ast.literal_eval(text.chatbox)
                storage_data=ast.literal_eval(text.storage_data)
        else:
            messages = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'},
                        {'role': 'system', 'content': 'Eres especialista en marketing'}
                    ]
            storage_data = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'},
                        {'role': 'system', 'content': 'Eres especialista en marketing'}
                    ]

        while action != 'end':
            if len(messages) > prompt_limit:
                del messages[6:9]
            messages.append({'role': 'user', 'content': prompt})
            storage_data.append({'role': 'user', 'content': prompt})
            print(len(messages))
            try:
                response = openai.chat.completions.create (
                    model='gpt-3.5-turbo-16k',
                    messages=messages,
                    temperature=0.2
                )
                tokens=response.usage.total_tokens
                response_content = response.choices[0].message.content
                response_content.replace('\n', '<br>')
                    
                if tokens < 4097:
                    messages.append({"role": "assistant", "content":response_content})
                    storage_data.append({"role": "assistant", "content":response_content})

                    
                chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                    'messages': storage_data,
                    'user': request.user,
                    })
                
                end_time = time.time()
                response_time = end_time - start_time
                print(response_time)

                if stelaquery.exists():
                    stelaquery.update(
                        chatbox=messages, 
                        storage_data=storage_data,
                        response_time=response_time
                    )
                    qs=ProStelaData.objects.get(id=obj)
                else:
                    qs=ProStelaData.objects.create(
                        title=title,
                        user=request.user,
                        section="Marketing Chats",
                        chatbox=messages,
                        storage_data=storage_data,
                        response_time=response_time
                    )
                ProStelaUsage.objects.create(
                    prompt=qs,
                    tokens=tokens
                )
                if tokens < 4097:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        })
                else:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        'alert1': 'event'
                        })
                
            except openai.APIError as e:
                    return JsonResponse({
                        'alert2': 'event'
                        })
                         
    if action == 'callStelaSight':
        url = []
        prompt = str(request.POST.get('prompt'))
        qty = int(request.POST.get('qty'))
        openai.api_key = settings.API_KEY
        response = openai.Image.create(
            prompt=prompt,
            n=qty,
            size="512x512"
            )
        for obj in response['data']:
            url.append(obj['url'])
        
        images_html = render_to_string('stela_control/load-data/meta/stela-sight/data.html', {
                        'url': url,
                        })
        return JsonResponse({'success': images_html})
    
    if action == "smartHashtag":
        hashdata = []
        userdata = []
        placesdata = []
        keyword = str(request.POST.get('qs'))
        keyword_findall = ''.join(re.findall(r'\w+', keyword))
        clean_keyword = keyword_findall.lower()
        url = "https://instagram-data12.p.rapidapi.com/search/"

        querystring = {
            "query":clean_keyword
            }

        headers = {
            "X-RapidAPI-Key": settings.KEYHUB,
            "X-RapidAPI-Host": settings.HUBHOST
        }

        response = requests.get(url, headers=headers, params=querystring)

        data = response.json()
        print(data)
        hashtags = data['hashtags'][:5]
        users = data['users'][:5]
       
        for list in hashtags:
            hashdata.append(list['hashtag'])

        for list in users:
            userdata.append(list['user'])

        boost_html = render_to_string('stela_control/load-data/meta/smart-boost/index.html', {
                        'hashtags': hashdata,
                        'users': userdata,
                        })
        return JsonResponse({'success': boost_html})
    
    if action == "callStelaChat":
        start_time = time.time()
        obj = request.POST.get('queryid')
        text=ProStelaData.objects.get(id=obj)
        messages=ast.literal_eval(text.storage_data)
        chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                'messages': messages,
                'user': request.user,
                })

        return JsonResponse({'response': chat_html, 'qs':text.pk})
    
    if action == "deleteQuery":
        obj = request.POST.get('queryid')
        query=ProStelaData.objects.get(id=obj)
        query.delete()
        
        return JsonResponse({'success': 'response'})
    
    if action == "cityCheck":
        country_id = request.POST.get('country_id')
        cities = City.objects.filter(country_id=country_id)
    
        return render(request, 'render/city_data.html', {'cities': cities})

def validators(request):
    action = request.POST.get('action')

    if action == "validateEmail":
        email=request.POST.get('email')
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
                response = JsonResponse({'alert':_('Please enter a valid email.')})
        else:
            response = JsonResponse({'success':_('Ok')})
    
    if action == "validateCharfield":
        subject=request.POST.get('text')
        pattern =  r"^[a-zA-Z0-9\-/., ñÑáéíóúÁÉÍÓÚ]*$"
        if not re.match(pattern, subject):
                response = JsonResponse({'alert':_('Special characters are not allowed.')})
        else:
            response = JsonResponse({'success':_('Ok')})
    
    if action == "validateTextArea":
        email=request.POST.get('textarea')
        pattern = r"^[^<>&'\"; ñÑáéíóúÁÉÍÓÚ]*$"
        if not re.match(pattern, email):
                response = JsonResponse({'alert':_('These characters are not allowed (<, >, /, \, &=)')})
        else:
            response = JsonResponse({'success':_('Ok')})
    
    if action == "validatePhonenumber":
        phone=request.POST.get('phone')
        s = str(phone)
        clean_string = s.replace(" ", "").replace("-", "")
        pattern = r'^\+[\d\s]{10,12}$'
        if not re.match(pattern, clean_string):
                response = JsonResponse({'alert':_('Only this format is allowed (+123456789)')})
        else:
            clean_number = phonenumbers.parse(clean_string, None)
            if phonenumbers.is_possible_number(clean_number):
                response = JsonResponse({'success':_('Ok')})
            else:
                response = JsonResponse({'alert':_('This phonenumber is not valid')})

    return response

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def newcomer(request):
    lang=request.LANGUAGE_CODE
    newcomer_form=  CompanyForm()
    get_formset = inlineformset_factory(
                Company, SocialLinks, 
                form=SocialMediaForm,
                extra=0, can_delete=False,
                )
    context = {
        'newcomerform': newcomer_form,
        'formsetmedia': get_formset(prefix="socialmedia")
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        call = request.POST.get('form-id')
        print(action)
        print(call)
        if action == 'cityCheck':
                country_id = request.POST.get('country_id')
                cities = City.objects.filter(country_id=country_id)

                return render(request, 'linkzone/render/city_data.html', {'cities': cities})
            
        if call == 'newcomerForm':
            form = CompanyForm(request.POST, request.FILES)
            formset = get_formset(request.POST, prefix="socialmedia")
            business = request.POST.get('select-business')
            city_id = request.POST.get('city_legal')

            if all([form.is_valid(),
                    formset.is_valid()
                ]):
                parent = form.save(commit=False)
                parent.owner = request.user
                parent.business = business
                parent.city_legal = City.objects.get(id=city_id)
                parent.lang = lang
                parent.save()

                for form in formset:
                    child = form.save(commit=False)
                    child.parent = parent
                    child.save()

                return JsonResponse({'success': _('Register validated, Welcome.')}) 
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})
                
    return render(request, 'stela_control/newcomer.html', context)
    
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def console(request): 
    lang=request.LANGUAGE_CODE
    events=Notifications.objects.filter(user=request.user)
    date_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    date_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)   
    month_min = timezone.localtime(timezone.now()) - timedelta(days=15)
    month_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    views_count=SiteControl.objects.all().count()
    sales=Order.objects.filter(created__range=[date_min, date_max]).aggregate(get_total=(Sum('total_paid')))
    orders=Order.objects.filter(status="Pending")
    subs=UserBase.objects.filter(is_subscribed=True, created__range=[month_min, month_max])
    support=Support.objects.all()
    billing=InvoiceControl.objects.filter(recipt__owner=request.user)
    context = {
        'events': events,
        'billing':billing,
        'viewscount': views_count,
        'sales': sales,
        'orders': orders,
        'subs': subs,
        'support': support,
     }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        call = request.POST.get('form-id')
        print(action)
        print(call)

        if action == "dateFilter":
            qdate = request.POST.get('date')
            date_min = datetime.datetime.combine(datetime.timedelta(days=qdate), datetime.time.min)
            date_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
            sales=Order.objects.filter(created__range=[date_min, date_max]).aggregate(get_total=(Sum('total_paid')))
           
            return JsonResponse({'sales': sales})
        
    return render(request, 'stela_control/index.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def templates(request):
    stock = Templates.objects.all()
    formset = formset_factory(TemplateForm, formset=RequiredFormSet, extra=1) 

    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id)
        print(action)

        if form_id == 'newForm':

            formset = formset(request.POST, request.FILES)

            if formset.is_valid():
                
                for form in formset:
                    item= form.save(commit=False)
                    item.save()

                return redirect('/inventory-control/templates')
            
            else:
                print (formset.errors)
                return render(request, 'stela_control/inventory/templates/index-templates.html', {
                    'stock': stock,
                    'formset': formset, 
                    'errors': formset.errors,
            })

        if action == 'data':
            obj_id=request.POST.get('objid')
            obj=Templates.objects.get(pk=obj_id)
            form=TemplateForm(instance=obj)

            obj_data = render_to_string('stela_control/load-data/form-base.html', {
                            'form': form,  
                            'size': obj  
                })

            response = JsonResponse({'response': obj_data})
            return response

        if form_id == "Update":
            pk=request.POST.get('obj-id')
            template=Templates.objects.get(pk=pk)
            form = TemplateForm(request.POST, request.FILES, instance=template, prefix='update') 
            if form.is_valid():
                form.save()
            
                return redirect('/inventory-control/templates')
            else:
                print(formset.errors)
                return render(request, 'stela_control/inventory/templates/index-templates.html', {
                    'stock': stock,
                    'formset': formset, 
                    'errors': formset.errors,
            })

        if action == 'deleteTemplate':
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Templates.objects.get(pk=id)
                obj.delete()
            response = JsonResponse({'success': 'return something'})
            return response

    return render(request, 'stela_control/inventory/templates/index-templates.html', {
            'stock': stock,
            'formset': formset, 
    })

def stelaChat(request):
    user=request.user
    custom=ProStelaData.objects.filter(user=user, section="custom").order_by('-created')
    content=ProStelaData.objects.filter(user=user, section="Content Chats").order_by('-created')
    marketing=ProStelaData.objects.filter(user=user, section="Marketing Chats").order_by('-created')
    development=ProStelaData.objects.filter(user=user, section="Development Chats").order_by('-created')
    context = {
        'custom': custom,
        'content': content,
        'marketing': marketing,
        'development': development
    }
    
    return render(request, 'stela_control/chatstela/index.html', context)

def stelaExpert(request):
    user=request.user
    messages=ProStelaData.objects.filter(user=user, section="custom").order_by('-created')

    context = {
        'messages': messages,
    }

    if request.method == 'POST':
        action = request.POST.get('action')
        call = request.POST.get('form-id')
        print(action)
        print(call)

        if action == "startModel":
            model=request.POST.get('model')
            new_model=ProStelaExpert()
            new_model.owner = request.user
            new_model.model = model
            try:
                if ProStelaExpert.objects.filter(owner=request.user).exists():
                    model=ProStelaExpert.objects.get(owner=request.user)
                    model.delete()
                    new_model.save()
                    response = JsonResponse({'success': _('Your ProStela Model has been selected successfully')})
                else:
                    new_model.save()
                    response = JsonResponse({'success': _('Your ProStela Model has been selected successfully')})
            except Exception as e:
                response = JsonResponse({'alert': _('Sorry, this model has already been selected')})
        return response

    return render(request, 'stela_control/prostela-expert/index.html', context)

def loginstela(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST': 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request,user)
                    return redirect('console')
                else:
                    msg = 'credenciales invalidas'
            else:
                msg = 'credenciales invalidas'

        else: 
            msg = 'error validando usuario'    
    return render(request, 'stela_control/accounts/user/login.html', {'form':form, 'msg':msg})

def logout_view(request):
    logout(request)
    return redirect('/')

#communicationsModule 
def contactMessage(request):
    contact = Contact.objects.all().order_by('-id')
    
    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        
        if action == "data":
            obj_id=request.POST.get('objid')
            obj=Contact.objects.get(pk=obj_id)
            form=ContactForm(instance=obj, prefix="update")
            if obj.status == "Answered":
                get_formset = inlineformset_factory(
                Contact, ContactResponse, 
                form=ResponseContactFormDisabled,
                extra=0, can_delete=False,
                )
            else:
                get_formset = inlineformset_factory(
                Contact, ContactResponse, 
                form=ResponseContactForm,
                extra=1, can_delete=False,
                )
            formset=get_formset(instance=obj)
            obj_data = render_to_string('stela_control/load-data/contact/modal.html', {
                            'form': form, 
                            'formset': formset,
                            'obj': obj  
                })

            response = JsonResponse({'response': obj_data})
            return response

        if form_id == "Update":
            obj_id=request.POST.get('obj-id')
            response=request.POST.get('contact_response-0-message')
            obj=Contact.objects.get(pk=obj_id)
            form=ContactForm(request.POST, instance=obj, prefix="update")
            get_formset = inlineformset_factory(
            Contact, ContactResponse, 
            form=ResponseContactForm,
            extra=0, can_delete=True,
            )
            formset=get_formset(request.POST, instance=obj)
            
            if all([form.is_valid(),
                    formset.is_valid(),
                    ]):
                name=form.cleaned_data['name']
                subject=form.cleaned_data['subject']
                message=form.cleaned_data['message']
                emailuser=form.cleaned_data['email']
                parent = form.save(commit=False)
                parent.status = "Answered"
                parent.save()
                
                instances = formset.save(commit=False)
                            
                for obj in formset.deleted_objects:
                        obj.delete()
                            
                for instance in instances:
                    instance.parent = parent
                    instance.save()
                
                html_content = render_to_string('stela_control/emails-template/contact/message_response.html', {
                        'name': name,
                        'subject': subject,
                        'message': message,
                        'response': response        
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            'RE: '+subject,
                            text_content,
                            settings.DEFAULT_EMAIL,
                            [emailuser]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                messages.success(request, _("Changes made successfully"))
                return redirect('/content/inbox')
            else:
                print(form.errors)
        
        if action == "deleteContact":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Contact.objects.get(pk=id)
                obj.delete()
            response = JsonResponse({'success': 'return something'})
            return response
    
    context={
       'contact':contact
    }

    return render(request, 'stela_control/inbox/index.html', context)

def commentsBlog(request):
    comments = Comments.objects.all().order_by('-id')
    
    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id)
        print(action)
        
        if action == "data":
            obj_id=request.POST.get('objid')
            obj=Comments.objects.get(pk=obj_id)
            form=CommentsFormBlog(instance=obj, prefix="update")
        
            obj_data = render_to_string('stela_control/load-data/form-base.html', {
                            'form': form, 
                            'obj': obj  
                })

            response = JsonResponse({'response': obj_data})
            return response

        if form_id == "Update":
            obj_id=request.POST.get('obj-id')
            obj=Comments.objects.get(pk=obj_id)
            form=CommentsFormBlog(request.POST, instance=obj, prefix="update")
            if form.is_valid():
                parent = form.save(commit=False)
                parent.save()
                        
                return redirect('/comments-blog')
            else:
                print(form.errors)
        
        if action == "deleteComments":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Comments.objects.get(pk=id)
                obj.delete()
            response = JsonResponse({'success': 'return something'})
            return response
    
    context={
       'comments':comments
    }

    return render(request, 'stela_control/content/comments/index.html', context)

def supportCenter(request):
    cases = Support.objects.all().order_by('-id')
    context={
        'cases': cases
    }
    return render(request, 'stela_control/support/list.html', context)

def updateSupport(request, id):
    current_user = request.user
    support = Support.objects.get(id=id)
    email_user = support.email
    readsuportform = ReadOnlySupportForm(instance=support)
    responseformset = inlineformset_factory(Support, SupportResponse, fields=('response',), extra=1, can_delete=False)
    
    if SupportResponse.objects.filter(case_id=id).exists():
        responseformset = inlineformset_factory(Support, ChatSupport, fields=('response',), widgets={'response': Textarea(attrs={ 'required': 'true' })}, extra=1, can_delete=False)
        responses = SupportResponse.objects.filter(case_id=id)
        chat_support = ChatSupport.objects.filter(case_id=id)
        context = { 
                'readsupportform': readsuportform,
                'responseform': responseformset,
                'support': support,
                'responses': responses,
                'chatsupport': chat_support,
                'update': datetime.datetime.now(),
             }
    else:
        responseformset = inlineformset_factory(Support, SupportResponse, fields=('response',), widgets={'response': Textarea(attrs={ 'required': 'true' })}, extra=1, can_delete=False)
        context = { 
                'readsupportform': readsuportform,
                'responseform': responseformset,
                'support': support,
                'update': datetime.datetime.now(),
             }
        
    if request.method == 'POST':
        readsupportform = ReadOnlySupportForm(request.POST, instance=support)
        formresponse = responseformset(request.POST)
        
        if all([readsupportform.is_valid(), 
                formresponse.is_valid(),
            ]):
            parent = readsupportform.save(commit=False)
            parent.save()
        
            for form in formresponse:
                response = form.save(commit=False)
                response.user_id = current_user.id
                response.case = parent
                response.save()

            html_content = render_to_string('emails/transactionals/support_response.html', {
                        'case': support.ticket,
                        'subject': support.option,
                        'date': support.created
                        })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                _('Your case has been answered'),
                text_content,
                settings.SUPPORT_EMAIL,
                [email_user]
               
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            Notifications.objects.create (
                    user = support.user,
                    status = "No Read",
                    title = _("Support Case Reply"),
                    description =support.option,
                    section = "support",
                    url = "https://emmerut.com/console/support" 
                )
            
            return redirect('/support-center')
        else:
            print(readsupportform.errors, formresponse.errors)

            messages.success(request, _("Changes made successfully"))
            return redirect('/support-center')

    return render(request, 'stela_control/support/update.html', context)

def update_support(request, id):
    support = Support.objects.get(id=id)
    current_user = support.user
    email_user = support.email
    readsuportform = ReadOnlySupportForm(instance=support)
    responseformset = inlineformset_factory(Support, SupportResponse, fields=('response',), extra=1, can_delete=False)
    
    if SupportResponse.objects.filter(case_id=id).exists():
        responseformset = inlineformset_factory(Support, ChatSupport, fields=('response',), widgets={'response': Textarea(attrs={ 'required': 'true' })}, extra=1, can_delete=False)
        responses = SupportResponse.objects.filter(case_id=id)
        chat_support = ChatSupport.objects.filter(case_id=id)
        context = { 
                'readsupportform': readsuportform,
                'responseform': responseformset,
                'support': support,
                'responses': responses,
                'chatsupport': chat_support,
                'update': datetime.now(),
             }
    else:
        responseformset = inlineformset_factory(Support, SupportResponse, fields=('response',), widgets={'response': Textarea(attrs={ 'required': 'true' })}, extra=1, can_delete=False)
        context = { 
                'readsupportform': readsuportform,
                'responseform': responseformset,
                'support': support,
                'update': datetime.now(),
             }
        
    if request.method == 'POST':
        readsupportform = ReadOnlySupportForm(request.POST, instance=support)
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

            html_content = render_to_string('emails/transactionals/support_response.html', {
                        'message': message,
                        })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                'Your case has been answered',
                text_content,
                settings.SUPPORT_EMAIL,
                [email_user]
               
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            Notifications.objects.create (
                            user = current_user,
                            status = "No Read",
                            title = "New Support Respond",
                            description ="Please read  " + support.ticket,
                            section ="Support",
                            url = "https://emmerut.com/console/support-list" 
                        )
            messages.success(request, "Changes made successfully")
            return redirect('/support-list/')

    return render(request, 'stela_control/support/update_support.html', context)

def new_email_marketing(request):
    form = NewsletterForm() 

    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            instance=form.save()
            newsletter=Newsletter.objects.get(id=instance.id)
            if newsletter.status=="Send":
                subject = newsletter.subject
                body = newsletter.body
                html_content = render_to_string('emails/linkzone/contact_email.html', {
                        'body': body,
                        })
                text_content = strip_tags(html_content)
                for email in newsletter.email.all():
                     send_email = EmailMultiAlternatives(
                                    subject,
                                    text_content,
                                    settings.SUPPORT_EMAIL,
                                    [email]
                                    )
                     send_email.attach_alternative(html_content, "text/html")
                     send_email.send()
                
                return redirect('stela:email_marketing_list')

    context={
        'form':form
    }

    return render(request, 'stela_control/marketing/email-marketing/new_email.html', context)

def emailMarketing(request):
    email = Newsletter.objects.all()
    q = request.POST.get('qs')
    date = request.POST.get('date')

    if q: 
        email = Newsletter.objects.filter(subject__icontains=q).order_by('-id')

    if date:
        date_min = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=int(date)), datetime.time.min)
        today = timezone.now()
        email = Newsletter.objects.filter(created__range=[date_min, today]).order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(email, 5)
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)

    context={
        'pages': lists,
    }

    return render(request, 'stela_control/marketing/email-marketing/email_list.html', context)

def update_email_marketing(request, id):
    email = Newsletter.objects.get(id=id)
    form = NewsletterForm(instance=email)

    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=email)
        if form.is_valid():
            instance=form.save()
            newsletter=Newsletter.objects.get(id=instance.id)
            if newsletter.status=="Enviado":
                subject = newsletter.subject
                body = newsletter.body
                html_content = render_to_string('emails/linkzone/contact_email.html', {
                        'body': body,
                        })
                text_content = strip_tags(html_content)
                for email in newsletter.email.all():
                     send_email = EmailMultiAlternatives(
                                    subject,
                                    text_content,
                                    settings.SUPPORT_EMAIL,
                                    [email]
                                    )
                     send_email.attach_alternative(html_content, "text/html")
                     send_email.send()
                
                return redirect('stela:email_marketing_list')

        return redirect('stela:email_marketing_list')

    context={
        'email':email,
        'form':form
    }

    return render(request, 'stela_control/marketing/email-marketing/update_email.html', context)

def delete_email_marketing(request):
    if request.method=='POST':
        product_ids = request.POST.getlist('id[]')
        for id in product_ids:
            product = Newsletter.objects.get(pk=id)
            product.delete()
        response = JsonResponse({'success': 'return something'})
        return response

def autocompletemark(request):
  if 'term' in request.GET:
      q = Newsletter.objects.filter(subject__icontains=request.GET.get('term'))
      titles = list()
      for product in q:
          titles.append(product.subject)
      return JsonResponse(titles, safe=False)
    
def emails_list(request):
    email = DataEmail.objects.all()
    q = request.POST.get('qs')
    date = request.POST.get('date')

    if q: 
        email = Newsletter.objects.filter(subject__icontains=q).order_by('-id')

    if date:
        date_min = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=int(date)), datetime.time.min)
        today = timezone.now()
        email = Newsletter.objects.filter(created__range=[date_min, today]).order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(email, 5)
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)

    context={
        'pages': lists,
    }

    return render(request, 'stela_control/marketing/email-marketing/emails_list.html', context)

def delete_emails(request):
    if request.method=='POST':
        product_ids = request.POST.getlist('id[]')
        for id in product_ids:
            product = DataEmail.objects.get(pk=id)
            product.delete()
        response = JsonResponse({'success': 'return something'})
        return response

def autocompletemail(request):
  if 'term' in request.GET:
      q = DataEmail.objects.filter(email__icontains=request.GET.get('term'))
      titles = list()
      for product in q:
          titles.append(product.email)
      return JsonResponse(titles, safe=False)
  
#contentModule
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def mainContent(request):
    
        
    return render(request, 'stela_control/content/index.html', {
            'call': 'emmerut',  

            })
    
def siteMain(request):
    author=UserBase.objects.get(pk=request.user.pk)
    lang=request.LANGUAGE_CODE
    
    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)

        if action == "checkSlide":        
            content=Content.objects.filter(author=author, section="Slider Blurry", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=SimpleContentForm,
                    extra=0, can_delete=True,
                )
                formset = get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='Slider Blurry'))
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/slider_form.html', { 
                    'formset': formset   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=SimpleContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/slider_form.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "checkSection":        
            pk=request.POST.get('authorid')
            author=UserBase.objects.get(pk=pk)
            content=Content.objects.filter(author=author, section="Sections Pack", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=RedirectContentForm,
                    extra=0, can_delete=True,
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/sections_form.html', { 
                    'formset': get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='Sections Pack'))   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=RedirectContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=3 
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/sections_form.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "checkProject":        
            pk=request.POST.get('authorid')
            author=UserBase.objects.get(pk=pk)
            content=Content.objects.filter(author=author, section="Project Carousel", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=RedirectContentForm,
                    extra=0, can_delete=True,
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/projects_form.html', { 
                    'formset': get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='Project Carousel'))   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=RedirectContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/projects_form.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response

        if action == "checkApp":        
            content=Content.objects.filter(author=author, section="App Carousel", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=StickerContentForm,
                    extra=0, can_delete=True,
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/apps_form.html', { 
                    'formset': get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='App Carousel'))   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=StickerContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/apps_form.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response

        if action == "checkSetFAQ":
            faq_pk=request.POST.get('faqpk')
            faq=FAQ.objects.get(pk=faq_pk)
            get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0, can_delete=True,
                )
            obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/faq_form.html', { 
                'formset2': get_formset(instance=faq, prefix='formset2')   
            })
            return JsonResponse({'content': obj_data})
            
        if form_id == "slider-form":
            content=Content.objects.filter(author=author, section="Slider Blurry", lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=SimpleContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "Slider Blurry"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/slider_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = formset_factory(
                    form=SimpleContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "Slider Blurry"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/slider_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if form_id == "section-form":
            content=Content.objects.filter(author=author, section="Sections Pack", lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=RedirectContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "Sections Pack"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/sections_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = inlineformset_factory(
                        UserBase, Content, 
                        form=RedirectContentForm,
                        extra=0,
                        can_delete=False,
                        validate_min=True, 
                        min_num=1 
                    )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "Sections Pack"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/sections_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
                
        if form_id == "project-form":
            content=Content.objects.filter(author=author, section="Project Carousel", lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=RedirectContentForm,
                    extra=0, can_delete=False,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "Project Carousel"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/projects_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = inlineformset_factory(
                        UserBase, Content, 
                        form=RedirectContentForm,
                        extra=0,
                        can_delete=False,
                        validate_min=True, 
                        min_num=3
                    )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "Project Carousel"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/projects_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "apps-form":
            content=Content.objects.filter(author=author, section="App Carousel", lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=StickerContentForm,
                    extra=0,
                    can_delete=False,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "App Carousel"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/apps_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = inlineformset_factory(
                        UserBase, Content, 
                        form=StickerContentForm,
                        extra=0,
                        can_delete=False,
                        validate_min=True, 
                        min_num=1
                    )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "App Carousel"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/apps_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "faq-form":
            content=FAQ.objects.filter(author=author, lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, FAQ, 
                    form=FAQForm,
                    extra=0, can_delete=False,
                )
                formset=get_formset(request.POST, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/faq_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
            else:
                get_formset = inlineformset_factory(
                    UserBase, FAQ, 
                    form=FAQForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                get_formset2 = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='formset')
                formset2=get_formset2(request.POST, prefix='formset2')
                if all[
                    formset.is_valid(),
                    formset2.is_valid()
                    ]:
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.lang = lang
                        data.save()

                    for form2 in formset2:
                        data2 = form2.save(commit=False)
                        data2.faq = data
                        data2.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/faq_form_clean.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
                
        if form_id == "setfaq-form":
            faq_pk=request.POST.get('faqpk')
            faq=FAQ.objects.get(pk=faq_pk)
            get_formset = inlineformset_factory(
                FAQ, SetFaq, 
                form=SetFaqForm,
                extra=0, can_delete=True,
            )
            formset=get_formset(request.POST, prefix='formset2', instance=faq)
            if formset.is_valid():

                for form in formset:
                    data = form.save(commit=False)
                    data.faq = faq
                    data.save()

                return JsonResponse({'success':_('Your content was upload successfully')})
            else:
                print(formset.errors)
                obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/faq_form.html', { 
                    'formset': formset,
                    'errors': formset.errors,
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
            
    return render(request, 'stela_editor/main.html', {
                
            })

def siteDocs(request):
    lang=request.LANGUAGE_CODE
    author=UserBase.objects.get(pk=request.user.pk)
    about=Content.objects.filter(section="About Values", lang=lang)
    apps=Content.objects.filter(path="Services", lang=lang)
    cards=Content.objects.filter(section="Card Content", lang=lang)
    image_bullets=Content.objects.filter(section="Image Bullet", lang=lang)
    box_bullet=Content.objects.filter(section="Icon Box", lang=lang)
    
    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)
        
        if action == "checkAbout":
            content=Content.objects.filter(author=author, section="About Values", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=AboutContentForm,
                    extra=0, can_delete=True,
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/aboutform.html', { 
                    'formset': get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='About Values')), 
                    'pk': author.pk
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=AboutContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/aboutform.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "checkCardContent":        
            content=Content.objects.filter(author=author, section="Card Content", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=ContentForm,
                    extra=0, can_delete=True,
                )
                formset = get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='Card Content'))
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/cardform.html', { 
                    'formset': formset,
                    'pk': author.pk   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=ContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/cardform.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "checkImageBullet":  
            uk=request.POST.get('uk')
            if uk:      
                content=Content.objects.get(pk=uk)
                form=ImageContentForm(instance=content)
                get_formset = inlineformset_factory(
                    Content, DynamicBullets, 
                    form=BulletSimpleForm,
                    extra=0, can_delete=False,
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/imagebulletform.html', { 
                    'form': form,
                    'formset': get_formset(instance=content, prefix='formset'),
                    'pk': content.pk
                        
                })
                response = JsonResponse({'content': obj_data})
            else:
                form=ImageContentForm()
                get_formset = formset_factory(
                    form=BulletSimpleForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/imagebulletform.html', { 
                    'form': form,
                    'formset': get_formset(prefix='formset')
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "checkBoxIconBulllets":        
            content=Content.objects.filter(author=author, section="Icon Box", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=TextContentForm,
                    extra=0, can_delete=True,
                )
                formset = get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='Icon Box'))
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/box-info.html', { 
                    'formset': formset,
                    'pk': author.pk   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=TextContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/box-info.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response

        if action == "checkDocs":
            pk=request.POST.get('pk')
            if pk:
                obj=SitePolicy.objects.get(pk=pk)
                form=PolicyForm(instance=obj)
                get_formset = inlineformset_factory(
                SitePolicy, LegalProvision, 
                form=LegalProvitionForm,
                extra=0, can_delete=True,
                )
                formset=get_formset(instance=obj, prefix='terms')

                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/terms.html', {
                                'form': form, 
                                'formset': formset,   
                                'obj': obj  
                    })

                response = JsonResponse({'content': obj_data})
            else:
                form=PolicyForm()
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(prefix='terms')

                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/terms.html', {
                                'form': form, 
                                'formset': formset,   
                    })
                response = JsonResponse({'empty': obj_data})
            return response

        if action == "checkFAQ": 
            pk=request.POST.get('pk')
            if pk:   
                print(pk)
                content=FAQ.objects.get(pk=pk)
                form=FAQForm(instance=content)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0, can_delete=False,
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/faq_form.html', { 
                    'formset': get_formset(instance=content, prefix='formset')   
                })
                response = JsonResponse({'content': obj_data})
            else:
                form=FAQForm()
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/faq_form.html', { 
                    'form': form,
                    'formset': get_formset(prefix='formset')
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "removeDoc":
            doc_id=request.POST.get('id')
            doc=SitePolicy.objects.get(pk=doc_id)
            doc.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if action == "removeContent":
            content_id=request.POST.get('id')
            content=Content.objects.get(pk=content_id)
            content.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if action == "removeFAQ":
            content_id=request.POST.get('id')
            content=FAQ.objects.get(pk=content_id)
            content.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if form_id == "doc-form":
            update_form = request.POST.get('form-update')
            if update_form:
                form=PolicyForm(request.POST, instance=update_form)
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, prefix='terms', instance=update_form)
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    policy = form.save(commit=False)
                    policy.owner = author
                    policy.lang = lang
                    policy.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.policy = policy
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'clause_cke':'content'})
            else:
                form=PolicyForm(request.POST)
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='terms')
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    policy = form.save(commit=False)
                    policy.owner = author
                    policy.lang = lang
                    policy.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.policy = policy
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'clause_cke':'content'})
        
        if form_id == "about-form":
            pk = request.POST.get('form-update')
            if pk:
                instance=UserBase.objects.get(pk=pk)
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=AboutContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=instance)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "About Values"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/aboutform.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'about_cke':'content'})
            else:
                get_formset = formset_factory(
                    form=AboutContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "About Values"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/aboutform.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'about_cke':'content'})
        
        if form_id == "card-form":
            pk = request.POST.get('form-update')
            if pk:
                instance=UserBase.objects.get(pk=pk)
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=ContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=instance)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "Card Content"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/cardform.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'about_cke':'content'})
            else:
                get_formset = formset_factory(
                    form=ContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "Card Content"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/cardform.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'about_cke':'content'})

        if form_id == "imagebullet-form":
            pk = request.POST.get('form-update')
            if pk:
                content=Content.objects.get(pk=pk)
                form=ImageContentForm(request.POST, request.FILES, instance=content)
                get_formset = inlineformset_factory(
                    Content, DynamicBullets, 
                    form=BulletSimpleForm,
                    extra=0, can_delete=False,
                )
                formset=get_formset(request.POST, prefix='formset', instance=content)
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.path = "Services"
                    parent.section = "Image Bullet"
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.parent = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                form=ImageContentForm(request.POST, request.FILES)
                get_formset = formset_factory(
                    form=BulletSimpleForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1
                )
                formset=get_formset(request.POST, prefix='formset')
                print(form.is_valid(),
                        formset.is_valid())
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.path = "Services"
                    parent.section = "Image Bullet"
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.parent = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
    
        if form_id == "boxicon-form":
            pk = request.POST.get('form-update')
            if pk:
                instance=UserBase.objects.get(pk=pk)
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=TextContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=instance)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "Icon Box"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/box-info.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = formset_factory(
                    form=TextContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "Icon Box"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/box-info.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if form_id == "faq-form":
            pk = request.POST.get('form-update')
            if pk:
                content=FAQ.objects.get(pk=pk)
                form=FAQForm(request.POST, instance=content)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0, can_delete=False,
                )
                formset=get_formset(request.POST, prefix='formset', instance=content)
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.faq = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/faq_form.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'clause_faq':'content'})
            else:
                form=FAQForm(request.POST)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='formset')
                print(form.is_valid(),
                        formset.is_valid())
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.faq = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/faq_form.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'clause_faq':'content'})
    
    return render(request, 'stela_editor/docs.html', {
            'about': about,
            'apps': apps,
            'cards': cards,
            'image_bullet': image_bullets,
            'box_bullets': box_bullet,
            })

def userConnect(request):
    lang=request.LANGUAGE_CODE
    image = Content.objects.filter(tag='Linkzone Image', lang=lang)
    updates = Content.objects.filter(parent__section='Linkzone Updates', lang=lang)
   
    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)

    return render(request, 'stela_control/content/user_connect/index.html', {
            # 'form': form,
            # 'formset': formset,
            'image': image,
            'updates': updates
            })

def stelaStory(request):
    lang=request.LANGUAGE_CODE
    country_id = str(lang).split('-')
    get_timezone = country_timezones(country_id[1])[0]
    author=UserBase.objects.get(pk=request.user.pk)
    schedule_action = False
    feed=Content.objects.filter(author=author, lang=lang).order_by('-id')
    schedule_post=Content.objects.filter(author=author, lang=lang, is_schedule=True)
    schedule = []
    if schedule_post.exists():
        for post in schedule_post:
            if post.mp4():
                planning_data = {
                    'id': post.pk,
                    'title':post.title, 
                    'start': post.schedule.isoformat(), 
                    'extendedProps': {
                        'fullTitle': post.title,
                        'mediatype': "VIDEO",
                    },
                    'allDay': False, 
                }
                schedule.append(planning_data)
                calendar_data = json.dumps(schedule)
            else:
                planning_data = {
                    'id': post.pk,
                    'title':post.title, 
                    'start': post.schedule.isoformat(), 
                    'extendedProps': {
                        'fullTitle': post.title,
                        'mediatype': "IMAGE",
                    },
                    'allDay': False, 
                }
                schedule.append(planning_data)
                calendar_data = json.dumps(schedule)
        schedule_action = True
    else:
        calendar_data = ""
        
    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)

        if action == "checkBlog":       
            form = BlogForm()
            obj_data = render_to_string('stela_control/load-data/maincontent/forms/blog_form.html', { 
                    'form': form
                })
            return JsonResponse({'empty': obj_data})
        
        if action == "postData":   
            postpk=request.POST.get('obj')    
            post = Content.objects.get(pk=postpk)
            obj_data = render_to_string('stela_control/load-data/stela_story/feed-item.html', { 
                    'post': post,
                    'usertz': get_timezone,
                })
            return JsonResponse({'content': obj_data})
        
        if action == "filter":   
            filter=request.POST.get('get_value')   
            feed=Content.objects.filter(author=author, lang=lang).order_by('-id')
            if filter in [_('News'), _('Tutorials'), _('Tips and Tricks'), _('Guides and Manuals'), _('Inspiration'), _('Events and Conferences'), _('Interviews')]:   
                filter_feed=feed.filter(category=filter)
                obj_data = render_to_string('stela_control/load-data/stela_story/table-blog-filter.html', { 
                        'feed': filter_feed,
                        'usertz': get_timezone,
                    })
                response = JsonResponse({'filter_data': obj_data})

            elif filter in ['today', '15', '29']:
                if filter == 'today':
                    start_date = datetime.datetime.now().date()
                    end_date = start_date
                elif filter == '15':
                    end_date = datetime.datetime.now().date()
                    start_date = end_date - timedelta(days=15)
                elif filter == '29':
                    end_date = datetime.datetime.now().date()
                    start_date = end_date - timedelta(days=29)

                filter_feed=feed.filter(created__range=[start_date, end_date])
                obj_data = render_to_string('stela_control/load-data/stela_story/table-blog-filter.html', { 
                        'feed': filter_feed,
                        'usertz': get_timezone,
                    })
                response = JsonResponse({'filter_data': obj_data})

            elif filter == '':
                obj_data = render_to_string('stela_control/load-data/stela_story/table-blog-filter.html', { 
                        'feed': feed,
                        'usertz': get_timezone,
                    })
                response = JsonResponse({'filter_data': obj_data})
            return response
        
        if action == "updateFeed":   
            pk = request.POST.get('feed_id')    
            post=Content.objects.get(pk=pk)
            form = BlogForm(instance=post)
            if post.is_schedule:
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/blog_form.html', { 
                        'form': form,
                    })
                response = JsonResponse({
                        'content': obj_data,
                        'getDate': post.schedule
                    })
            else:
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/blog_form.html', { 
                        'form': form,
                    })
                response = JsonResponse({'content': obj_data})
                
            return response
        
        if action == "removeObj":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Content.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if action == "loadPages":
            lang=request.LANGUAGE_CODE
            country_id = str(lang).split('-')
            get_timezone = country_timezones(country_id[1])[0] 
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            print(starts)
            print(ends)
            new_posts = Content.objects.filter(author=author, lang=lang).order_by('-id')[starts:ends]
            new_pages = render_to_string('stela_control/load-data/blog-feed.html', {
                    'feed': new_posts,
                    'usertz': get_timezone,
                    })
            return JsonResponse({'response': new_pages})
        
        if form_id == "blog-form":
            form = BlogForm(request.POST, request.FILES)
            website = request.POST.get('website')
            schedule = request.POST.get('schedule')
            if form.is_valid():
                data = form.save(commit=False)
                data.author = author
                data.section = "Blog Post"
                data.site = website
                data.lang = lang
                data.save()

                if schedule:
                    Content.objects.filter(pk=data.id).update(schedule=schedule, is_schedule=True)

                return JsonResponse({'success':_('Your post was upload successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/blog_form.html', { 
                    'form': form,
                    'errors': form.errors,
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
        
        if form_id == "blog-update":
            pk = request.POST.get('obj-id')    
            post=Content.objects.get(pk=pk)
            form = BlogForm(request.POST, request.FILES, instance=post)
            website = request.POST.get('website')
            schedule = request.POST.get('schedule')
            if form.is_valid():
                data = form.save(commit=False)
                data.author = author
                data.section = "Blog Post"
                data.site = website
                data.lang = lang
                data.save()

                if schedule:
                    Content.objects.filter(pk=data.id).update(schedule=schedule, is_schedule=True)

                return JsonResponse({'success':_('Your post was upload successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/blog_form.html', { 
                    'form': form,
                    'errors': form.errors,
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
            
    return render(request, 'stela_control/content/stelastory.html', {
                'calendar_data': calendar_data,
                'schedule': schedule_action,
                'usertz': get_timezone,
                'feed': feed

            })

#inventoryModule
@login_required
def services(request):
    lang=request.LANGUAGE_CODE
    stock=Inventory.objects.filter(type="Service", lang=lang)
    form = ServiceForm()
    get_formset = inlineformset_factory(
        Inventory, Modules, 
        form=ModulesForm,
        extra=0, can_delete=False,
        )
    formset=get_formset(prefix='form')
    
    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id)
        print(action)

        if form_id == "newService":
            update_form = request.POST.get('form-update')
            if update_form:
                service=Inventory.objects.get(pk=update_form)
                set_formset = inlineformset_factory(
                    Inventory, Modules, 
                    form=ModulesForm,
                    extra=0, can_delete=True,
                    )
                form = ServiceForm(request.POST, request.FILES, instance=service, prefix="update")
                formset = set_formset(request.POST, request.FILES, prefix='update', instance=service)  
                if all([form.is_valid(),
                        formset.is_valid(),
                        ]):
                        parent = form.save(commit=False)
                        parent.save()
                            
                        instances = formset.save(commit=False)
                                
                        for obj in formset.deleted_objects:
                                obj.delete()
                                
                        for instance in instances:
                            instance.parent = parent
                            instance.save()

                        return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/formset-base-services.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
            else:
                form = ServiceForm(request.POST, request.FILES)
                formset = get_formset(request.POST, request.FILES, prefix='form')
                    
                if all([form.is_valid(), 
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.owner = request.user
                    parent.type = "Service"
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.parent = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/formset-base-services', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
        
        if action == "data":
            obj_id=request.POST.get('objid')
            obj=Inventory.objects.get(pk=obj_id)
            form=ServiceForm(instance=obj, prefix="update")
            get_formset = inlineformset_factory(
            Inventory, Modules, 
            form=ModulesForm,
            extra=0, can_delete=True,
            )
            formset=get_formset(instance=obj, prefix='update')

            obj_data = render_to_string('stela_control/load-data/formset-base-services.html', {
                            'form': form, 
                            'formset': formset,   
                            'pk': obj_id, 
                })

            response = JsonResponse({'response': obj_data})
            return response

        if action == "deleteObj":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Inventory.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
    
    return render(request, 'stela_control/inventory/services/index-services.html', {
        'stock': stock,
        'form': form,
        'formset': formset, 
        'errors': formset.errors,
        'call': 'home'
        })

@login_required
def products(request):
    lang=request.LANGUAGE_CODE
    stock=Inventory.objects.filter(type="Product", lang=lang)
    categories=Category.objects.filter(owner=request.user)
    colors=StelaColors.objects.filter(owner=request.user)
    sizes=Sizes.objects.all()

    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')

        if action == "categoryData":
            pk=request.POST.get('pk')
            if pk:
                obj=Category.objects.get(pk=pk)
                form = categForm(instance=obj)
                obj_data = render_to_string('stela_control/load-data/products/new/category-form.html', {
                                'form': form,  
                                'obj': pk, 
                    })
            else:
                get_formset = formset_factory(
                    categForm, 
                    formset=RequiredFormSet, 
                    extra=1,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/products/update/category-form.html', {
                                'formset': formset,   
                    })

            response = JsonResponse({'response': obj_data})
            return response
        
        if action == "newProductData":
            pk=request.POST.get('pk')
            if pk:
                obj=Inventory.objects.get(pk=pk)
                form = ProductForm(instance=obj)
                get_formset = inlineformset_factory(
                    Inventory, Bulletpoints, 
                    form=BulletForm,
                    extra=1, can_delete=False,
                )
                formset=get_formset(instance=obj, prefix='update')
                obj_data = render_to_string('stela_control/load-data/products/new/product-form.html', {
                            'form': form, 
                            'formset': formset,   
                            'obj': pk, 
                })
            else:
                form = ProductForm()
                get_formset = inlineformset_factory(
                    Inventory, Bulletpoints, 
                    form=BulletForm,
                    extra=1, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 

                )
                formset=get_formset()
                obj_data = render_to_string('stela_control/load-data/products/update/product-form.html', {
                                'form': form, 
                                'formset': formset,   
                    })

            response = JsonResponse({'response': obj_data})
            return response
            
        if action == "variantData":
            pk=request.POST.get('pk')
            if pk:
                obj_id=request.POST.get('variantid')
                obj=Variants.objects.get(pk=pk)
                form=VariantForm(instance=obj)
                obj_data = render_to_string('stela_control/load-data/products/new/variant-form.html', {
                                'form': form,  
                                'obj': pk  
                    })
            else:
                get_formset = formset_factory(
                    VariantForm, 
                    formset=RequiredFormSet, 
                    extra=1,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/products/update/variant-form.html', {
                                'formset': get_formset()
                    })

            response = JsonResponse({'response': obj_data})
            return response
        
        if action == "sizeData":
            pk=request.POST.get('pk')
            if pk:
                obj=Sizes.objects.get(pk=pk)
                form=SizeForm(instance=obj)

                obj_data = render_to_string('stela_control/load-data/products/new/size-form.html', {
                                'form': form,  
                                'obj': pk  
                    })
            else:
                get_formset = formset_factory(
                    SizeForm, 
                    formset=RequiredFormSet, 
                    extra=1,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/products/update/size-form.html', {
                                'form': form,    
                    })

            response = JsonResponse({'response': obj_data})
            return response
        
        if action == "colorData":
            pk=request.POST.get('pk')
            if pk:
                obj=StelaColors.objects.get(pk=pk)
                form=ColorsForm(instance=obj)

                obj_data = render_to_string('stela_control/load-data/products/new/color-form.html', {
                                'form': form,  
                                'obj': pk  
                    })
            else:
                get_formset = formset_factory(
                    ColorsForm, 
                    formset=RequiredFormSet, 
                    extra=1,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/products/update/color-form.html', {
                                'form': get_formset(),    
                    })

            response = JsonResponse({'response': obj_data})
            return response
        
        if action == "catalogData":
            pk=request.POST.get('pk')
            if pk:
                obj=VariantsImage.objects.get(pk=obj_id)
                form=VariantImageForm(instance=obj, prefix="update")
        
                get_formset = inlineformset_factory(
                    VariantsImage, Gallery, 
                    form=GalleryForm,
                    extra=0, can_delete=True,
                    )
                formset2=get_formset(instance=obj, prefix='update')
                obj_data = render_to_string('stela_control/load-data/products/new/catalog-form.html', {
                                'form': form,  
                                'formset2': formset2,  
                                'catalog': obj  
                    })
            else:
                form=VariantImageForm()
                get_formset = inlineformset_factory(
                    VariantsImage, Gallery, 
                    form=GalleryForm,
                    extra=0, 
                    can_delete=True,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/products/update/catalog-form.html', {
                                'form': form,  
                                'formset': get_formset(),   
                    })
            response = JsonResponse({'response': obj_data})
            return response

        if action == "deleteObj":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Inventory.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if form_id == "newProductForm":
            products=Inventory.objects.filter(type='Product')
            sku_count=products.count() + 1 
            form = ProductForm(request.POST, request.FILES)
            formset2 = get_formset2(request.POST, prefix='bullet')
            if all([form.is_valid(), 
                    formset2.is_valid(),
                    ]):
                    cat_id = form.cleaned_data['category']
                    category=Category.objects.get(pk=cat_id.pk)
                    get_code = str(category.type+'-'+category.slug+'-'+str(sku_count))
                    parent = form.save(commit=False)
                    parent.category = category
                    parent.sku = get_code
                    parent.owner = request.user
                    parent.type = "Product"
                    parent.lang = lang
                    parent.save()

                    for form in formset2:
                        child2 = form.save(commit=False)
                        child2.product = parent
                        child2.save()
                    
                    messages.success(request, _("Changes made successfully"))
                    return redirect('/inventory-control/products')

            else:
                print (formset.errors)
                return render(request, 'stela_control/inventory/products/index-products.html', {
                    'stock': stock,
                    'sizes': sizes,
                    'form': form,
                    'form2': form2,
                    'formset': formset, 
                    'formset2': formset2,
                    'errors': formset.errors,
                    'errors2': formset2.errors,
            })

        if form_id == "newSize":
            formset3 = get_formset3(request.POST, prefix='sizes')
            if formset3.is_valid():
                
                for form in formset3:
                        form.save()

                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print (formset3.errors)

        if form_id == "newVariant":
            formset4 = get_formset4(request.POST, request.FILES, prefix='variant')
            if formset4.is_valid():
                
                for form in formset4:
                        form.save()

                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print (formset4.errors)

        if form_id == "newCatalog":
            form2 = VariantImageForm(request.POST)
            formset=get_formset(request.POST, request.FILES, prefix='gallery')
            if all([form2.is_valid(), 
                    formset.is_valid(),
                    ]):
                
                    catalogue = form2.save(commit=False)
                    catalogue.save()

                    for form in formset:
                        child2 = form.save(commit=False)
                        child2.catalogue = catalogue
                        child2.save()
                    
                    messages.success(request, _("Changes made successfully"))
                    return redirect('/inventory-control/products')
            else:
                print (formset4.errors)

        if form_id == "Update":
            pk=request.POST.get('obj-id')
            variant=Variants.objects.get(pk=pk)

            form=VariantForm(request.POST, request.FILES, instance=variant)
            if form.is_valid():
                form.save()
                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print(formset.errors)
        
        if form_id == "sizeUpdate":
            pk=request.POST.get('size-id')
            size=Sizes.objects.get(pk=pk)

            form=SizeForm(request.POST, instance=size)
            if form.is_valid():
                form.save()
                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print(formset.errors)

        if form_id == "catalogUpdate":
            pk=request.POST.get('catalog-id')
            catalog=VariantsImage.objects.get(pk=pk)
            form=VariantImageForm(instance=catalog, prefix="update")
    
            get_formset = inlineformset_factory(
                VariantsImage, Gallery, 
                form=GalleryForm,
                extra=0, can_delete=True,
                )
           
            form = VariantImageForm(request.POST, instance=catalog, prefix="update")
            formset2 = get_formset(request.POST, request.FILES, prefix='update-gallery', instance=catalog)  
            if all([form.is_valid(),
                    formset2.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.save()
                        
                    instances2 = formset2.save(commit=False)
                            
                    for obj in formset2.deleted_objects:
                            obj.delete()
                            
                    for instance in instances2:
                        instance.catalogue = parent
                        instance.save()
                    
                    messages.success(request, _("Changes made successfully"))
                    return redirect('/inventory-control/products')
            else:
                print(
                    form.errors,
                    formset.errors,
                    formset2.errors,
                )
                return render(request, 'stela_control/inventory/products/index-products.html', {
                    'stock': stock,
                    'sizes': sizes,
                    'form': form,
                    'form2': form2,
                    'formset': formset, 
                    'formset2': formset2,
                    'formset3': formset3,
                    'formset4': formset4,
                    'errors': formset.errors,
                    'errors2': formset2.errors,
            })

        if form_id == 'colorForm':
                formset=colorform(request.POST, prefix='color')
                if formset.is_valid():

                    for loop in formset:
                        color=loop.save(commit=False)
                        color.owner=request.user
                        color.save()

                    messages.success(request, _("Changes made successfully"))
                    return redirect('stela:products')
                else:
                    print(formset.errors)

        if form_id == 'colorUpdate':
            obj_id=request.POST.get('obj-id')
            data=StelaColors.objects.get(pk=obj_id)
            form=ColorsForm(request.POST, instance=data)
            if form.is_valid():
                form.save()

                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print(form.errors)
                
        if form_id == 'categForm':
                formset=categform(request.POST, prefix='categ')
                if formset.is_valid():

                    for loop in formset:
                        category=loop.save(commit=False)
                        category.owner=request.user
                        category.save()
            
                    messages.success(request, _("Changes made successfully"))
                    return redirect('/inventory-control/products')
                else:
                    print(formset.errors)   

        if form_id == 'categUpdate':
            obj_id=request.POST.get('obj-id')
            data=Category.objects.get(pk=obj_id)
            form=categForm(request.POST, instance=data)
            if form.is_valid():
                form.save()

                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print(form.errors)

    return render(request, 'stela_control/inventory/products/index-products.html', {
        'stock': stock,
        'sizes': sizes,
        'colors': colors,
        'categ': categories,
        'call': 'Product'
        })

def updateProduct(request, id):
    product=Inventory.objects.get(id=id)
    colors = Variants.objects.raw('SELECT DISTINCT ON (color_id) * FROM stela_control_variants WHERE product_id=%s', [id])
    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id)
        if action == "dataProduct":
                obj=Inventory.objects.get(id=id)
                form=ProductForm(instance=obj, prefix="update")
        
                get_formset2 = inlineformset_factory(
                    Inventory, Bulletpoints, 
                    form=BulletForm,
                    extra=0, can_delete=True,
                    )
                formset2=get_formset2(instance=obj, prefix='update-bullet')

                obj_data = render_to_string('stela_control/load-data/products/product-modal.html', {
                                'form': form,  
                                'formset2': formset2,  
                                'product': obj  
                    })
            
                response = JsonResponse({'response': obj_data})
                return response
        
        if form_id == "productUpdate":
            product=Inventory.objects.get(id=id)
            form = ProductForm(request.POST, request.FILES, instance=product, prefix="update")
            print(form.errors)
            if form.is_valid():
                parent = form.save(commit=False)
                parent.save()
                               
                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/update-product/'+str(product.id))
            
    return render(request, 'stela_control/inventory/products/update-product.html', {
                'product': product,
                'colors': colors
            })

#metaPlattforms
def metaAPI(request):
    user=request.user
    action = request.POST.get('action')

    if action == "updateMeta": 
        status = request.POST.get('status')
        user_token = request.POST.get('access_token')
        if user_token:
            UserBase.objects.filter(username=user.username).update(meta_status=status, meta_token=user_token)
            response = JsonResponse({'status':status, 'token':'granted'})
        else:
            UserBase.objects.filter(username=user.username).update(meta_status=status, meta_token="no_token")
            response = JsonResponse({'status':status, 'token':'not_granted'})
        return response
    
    if action == "checkPage":
        pageid = request.POST.get('pageid')
        pagetoken = request.POST.get('pagetoken')
        url = f"https://graph.facebook.com/v17.0/{pageid}/instagram_accounts?"
        params= {
            'access_token': pagetoken
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            alert = render_to_string('stela_control/load-data/instagram-alert.html', {})
            response = JsonResponse({'alert': alert})
        else:
            response = JsonResponse({'success': 'add page Granted'})

        return response

    if action == "addPage": 
        name = request.POST.get('name')
        pageid = request.POST.get('pageid')
        pagetoken = request.POST.get('pagetoken')
        category = request.POST.get('category')
        FacebookAdsApi.init(
            app_id=settings.META_ID,
            app_secret=settings.META_SECRET,
            access_token=pagetoken
        )

        business_id = settings.META_BUSINESS_ID
        business = Business(business_id)
        params = {
            'page_id': pageid
        }
        business.create_owned_page(params=params)
        url = f"https://graph.facebook.com/v17.0/{pageid}?"
        params= {
            'fields': 'picture, fan_count, followers_count',
            'access_token': pagetoken
        }
        response = requests.get(url, params=params)
        data = response.json()
        image = data['picture']['data']['url']
        fans = data['fan_count']
        followers = data['followers_count']
        pages=FacebookPage.objects.filter(asset_id=pageid)
        if pages.exists():
            pages.update(
                owner=user,
                token=pagetoken,
                image=image,
                fans=fans,
                followers=followers
                )
        else:
            FacebookPage.objects.create(
                owner=user,
                name=name,
                category=category,
                asset_id=pageid,
                image=image,
                followers=followers,
                fans=fans,
                token=pagetoken
            )
        messages.success(request, _("Page added successfully"))
        response = JsonResponse({'success': 'Page added'})

        if not re.match(r'^[a-zA-Z\s]+$', name):
            response = JsonResponse({'alert':_('only letters allowed (upper and lower case)')})

        return response
    
    if action == "removePage":
        pageid = request.POST.get('pageid') 
        business_id = settings.META_BUSINESS_ID
        page = FacebookPage.objects.get(pk=pageid)
        url = f'https://graph.facebook.com/v17.0/{business_id}/pages'
        params = {
        'page_id': page.asset_id,
        'access_token': user.meta_token
        }
        response = requests.delete(url, params=params)

        FacebookPage.objects.filter(pk=pageid).delete()
        InstagramAccount.objects.filter(commerce_id=page.asset_id).delete()
        messages.success(request, _("Page removed successfully"))
        response = JsonResponse({'success': 'Page removed'})
        return response

def metaID(request):
    appid=settings.META_ID
    return JsonResponse({'appId':appid})

def igID(request):
    appid = settings.INSTAGRAM_ID        
    return JsonResponse({'appId': appid})

def metaSuite(request):
    owner=request.user
    pages=FacebookPage.objects.filter(owner=owner)
    context = {
        'pages': pages
    }
    response = render(request, 'stela_control/marketing/meta_business/index.html', context)
    response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/' 
    return response

def metaDetail(request, id):
    user=request.user
    page=FacebookPage.objects.get(asset_id=id)
    urlpage = f"https://graph.facebook.com/v17.0/{page.asset_id}?"
    paramspage= {
        'fields': 'id, access_token, category, picture, fan_count, followers_count, name',
        'access_token': user.meta_token
    }
    response = requests.get(urlpage, params=paramspage)

    if response.status_code == 200:
        print('El inicio de sesión en la API Graph de Facebook es válido.')
    else:
        print('El inicio de sesión en la API Graph de Facebook no es válido:', response.json())
        return HttpResponseRedirect('/marketing/business-suite')
    
    datapage = response.json()
    page_token=datapage['access_token']
    page_id=datapage['id']
    page_name=datapage['name']
    page_fans=datapage['fan_count']
    page_category=datapage['category']
    page_followers=datapage['followers_count']
    page_image=datapage['picture']['data']['url']
    FacebookPage.objects.filter(asset_id=id).update(
        asset_id=page_id,
        token=page_token,
        name=page_name,
        fans=page_fans,
        followers=page_followers,
        category=page_category,
        image=page_image
    )
    urlig = f"https://graph.facebook.com/v17.0/{id}?"
    paramsig= {
            'fields': 'instagram_business_account',
            'access_token': datapage['access_token']
        }
    response = requests.get(urlig, params=paramsig)
    dataig = response.json()
    if "instagram_business_account" in dataig and len(dataig["instagram_business_account"]) > 0:
        ig_id=dataig["instagram_business_account"]['id']
        urlig = f"https://graph.facebook.com/v17.0/{ig_id}?"
        paramsig= {
                'fields': 'name, username, followers_count, profile_picture_url',
                'access_token': datapage['access_token']
            }
        response = requests.get(urlig, params=paramsig)
        ig_data = response.json()
        ig_name = ig_data['name']
        ig_username = ig_data['username']
        ig_followers = ig_data['followers_count']
        ig_image = ig_data['profile_picture_url']
        ig_account=InstagramAccount.objects.filter(asset_id=ig_id)
        if ig_account.exists():
            ig_account.update(
                owner=user,
                title=ig_name,
                username=ig_username,
                commerce_id=id,
                asset_id=ig_id,
                image=ig_image,
                followers=ig_followers
            )
        else:
            InstagramAccount.objects.create(
                owner=user,
                title=ig_name,
                username=ig_username,
                commerce_id=id,
                asset_id=ig_id,
                image=ig_image,
                followers=ig_followers
            )
        ig_account=InstagramAccount.objects.get(asset_id=ig_id)
    else:
        ig_account=None

    context = {
        'page': page,
        'instagram': ig_account
    }
    response = render(request, 'stela_control/marketing/meta_business/page/page-detail.html', context)
    response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/' 
    return response    

def page(request, id):
    user=request.user
    url = 'https://graph.facebook.com/v13.0/me'
    params = {
        'access_token': user.meta_token
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print('El inicio de sesión en la API Graph de Facebook es válido.')
    else:
        print('El inicio de sesión en la API Graph de Facebook no es válido:', response.json())
        return HttpResponseRedirect('/marketing/business-suite')

    page=FacebookPage.objects.get(asset_id=id)
    posts=FacebookPostPage.objects.filter(page=page).order_by('-created')[:10]
    schedule=FacebookPostPage.objects.filter(page=page, schedule__isnull=False)
    url='https://graph.facebook.com/{version}/{endpoint}'
    epfeed=f'{id}/feed'
    epimage=f'{id}/photos'
    epvideo=f'{id}/videos'


    if request.method == 'POST':
        
        action = request.POST.get('form-id')
        call = request.POST.get('action')
        print(action)
        if action == "postform":
            form = FbPostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.page = page
                post.save()
                return JsonResponse({'postid': post.pk})
            else:
                form = FbPostForm()
        
        if action == "formUpdate":
            postid=request.POST.get('post-id')
            post=FacebookPostPage.objects.get(pk=postid)
            form = FbPostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.page = page
                post.save()
                
                return JsonResponse({'postid': post.pk})
            else:
                form = FbPostForm(instance=post)
        
        if call == "loadPages":
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            new_posts = FacebookPostPage.objects.filter(page=page).order_by('-created')[starts:ends]
            new_pages = render_to_string('stela_control/load-data/meta/fb-new-pages.html', {
                    'newposts': new_posts,
                    })
            return JsonResponse({'response': new_pages})
        
        if call == "updatePost":
            postid = request.POST.get('postid')
            page = FacebookPage.objects.get(asset_id=id)
            post = FacebookPostPage.objects.get(pk=postid)
            form = FbPostForm(instance=post)
            media = FacebookPostMedia.objects.filter(post_id=postid)
            content = render_to_string('stela_control/load-data/meta/content-pro-update/content.html', {
                    'form': form,
                    'page': page
                    })
            
            schedule = render_to_string('stela_control/load-data/meta/content-pro-update/schedule.html', {
                    'form': form,
                    'page': page
                    })
            
            media = render_to_string('stela_control/load-data/meta/content-pro-media/media.html', {
                    'media': media,
                    })
            if post.schedule:
                return JsonResponse({
                    'content': content, 
                    'schedule': schedule, 
                    'media': media, 
                    'post': post.pk
                })
            else:
                return JsonResponse({
                    'content': content,  
                    'media': media, 
                    'post': post.pk
                })

        if call == "clearPost":
            page = FacebookPage.objects.get(asset_id=id)
            form = FbPostForm()

            content = render_to_string('stela_control/load-data/meta/content-pro-update/content.html', {
                    'form': form,
                    'page': page
                    })
            
            schedule = render_to_string('stela_control/load-data/meta/content-pro-update/schedule.html', {
                    'form': form,
                    'page': page
                    })
            return JsonResponse({'content': content, 'schedule': schedule})
        
        if call == "removeMedia":
            media_id = request.POST.get('media')
            obj = FacebookPostMedia.objects.get(pk=media_id)
            media = FacebookPostMedia.objects.filter(post_id=obj.post.pk)
            obj.delete()
            media = render_to_string('stela_control/load-data/meta/content-pro-media/media.html', {
                    'media': media,
                    })
            return JsonResponse({'media': media})
        
        if call == "postPage":
            user_token = user.meta_token
            urltoken = f'https://graph.facebook.com/v17.0/{id}?fields=access_token&access_token={user_token}'
            response = requests.get(urltoken)
            data = response.json()
            page_access_token = data['access_token']     
            print('success', page_access_token)   
            postid = request.POST.get('postid')
            post=FacebookPostPage.objects.get(pk=postid)
            soup = BeautifulSoup(post.content, 'html.parser')
            message_formatted = soup.get_text("\n")
            media = FacebookPostMedia.objects.filter(post_id=postid)
            mediaIdObjects = []
            urlParams = []
            upimage = None
            if media.exists():
                if post.schedule:
                    for obj in media:
                        if obj.mp4():
                            media_params = {
                            'published':'false',
                            'access_token': page_access_token,
                            'scheduled_publish_time': post.get_schedule_timestamp(),
                            'file_url': obj.get_url(),
                            'description': message_formatted
                            }
                            upvideo = requests.post(url.format(version='v17.0', endpoint=epvideo), params=media_params)
                            data = upvideo.json()
                            FacebookPostPage.objects.filter(pk=postid).update(feed_id=data['id'], is_video=True)
                        else:
                            media_params = {
                            'published':'false',
                            'access_token': page_access_token,
                            'url': obj.get_url()
                            }
                            upimage = requests.post(url.format(version='v17.0', endpoint=epimage), params=media_params)
                            data = upimage.json()
                            print(data)
                            mediaIdObject = {'media_fbid': data['id']}
                            mediaIdObjects.append(mediaIdObject)
            
                    if upimage:
                        urlParams.append(('access_token', page_access_token))
                        urlParams.append(('published', 'false'))
                        urlParams.append(('scheduled_publish_time', post.get_schedule_timestamp()))
                        urlParams.append(('message', message_formatted))
                        for i, mediaIdObject in enumerate(mediaIdObjects):
                            urlParams.append(('attached_media[{}]'.format(i), mediaIdObject))
                        url = f'https://graph.facebook.com/{id}/feed?' + '&'.join([f'{key}={value}' for key, value in urlParams])
                        post = requests.post(url)
                        postdata = post.json()
                        FacebookPostPage.objects.filter(pk=postid).update(feed_id=postdata['id'])
                else:
                    for obj in media:
                        if obj.mp4():
                            media_params = {
                            'published':'true',
                            'access_token': page_access_token,
                            'file_url': obj.get_url(),
                            'description': message_formatted
                            }
                            upvideo = requests.post(url.format(version='v17.0', endpoint=epvideo), params=media_params)
                            data = upvideo.json()
                            FacebookPostPage.objects.filter(pk=postid).update(feed_id=data['id'], is_video=True)
                        else:
                            media_params = {
                            'published':'false',
                            'access_token': page_access_token,
                            'url': obj.get_url()
                            }
                            upimage = requests.post(url.format(version='v17.0', endpoint=epimage), params=media_params)
                            data = upimage.json()
                            print(data)
                            mediaIdObject = {'media_fbid': data['id']}
                            mediaIdObjects.append(mediaIdObject)
                        
                    if upimage:
                        urlParams.append(('access_token', page_access_token))
                        urlParams.append(('message', message_formatted))
                        for i, mediaIdObject in enumerate(mediaIdObjects):
                            urlParams.append(('attached_media[{}]'.format(i), mediaIdObject))
                        url = f'https://graph.facebook.com/{id}/feed?' + '&'.join([f'{key}={value}' for key, value in urlParams])
                        post = requests.post(url)
                        postdata = post.json()
                        FacebookPostPage.objects.filter(pk=postid).update(feed_id=postdata['id'])
            else:
                if post.schedule:
                    params = {
                            'access_token': page_access_token,
                            'published':'false',
                            'scheduled_publish_time': post.get_schedule_timestamp(),
                            'message': message_formatted
                        }
                    post = requests.post(url.format(version='v17.0', endpoint=epfeed), params=params)
                    postdata = post.json()
                    FacebookPostPage.objects.filter(pk=postid).update(feed_id=postdata['id'])
                else:
                    params = {
                            'access_token': page_access_token,
                            'message': message_formatted
                        }
                    post = requests.post(url.format(version='v17.0', endpoint=epfeed), params=params)
                    postdata = post.json()
                    FacebookPostPage.objects.filter(pk=postid).update(feed_id=postdata['id'])
                    
            return JsonResponse({'success': 'return something'})     

        if call == "postPageUpdate":
            user_token = user.meta_token
            urltoken = f'https://graph.facebook.com/v17.0/{id}?fields=access_token&access_token={user_token}'
            response = requests.get(urltoken)
            data = response.json()
            page_access_token = data['access_token']     
            print('success', page_access_token)
            postid = request.POST.get('postid')
            post=FacebookPostPage.objects.get(pk=postid)
            soup = BeautifulSoup(post.content, 'html.parser')
            message_formatted = soup.get_text("\n")
            media = FacebookPostMedia.objects.filter(post_id=postid)
            epupdate=f'{post.feed_id}?'
            if media.exists():
               for obj in media:
                    if post.schedule:
                        if obj.mp4():
                            media_params = {
                            'access_token': page_access_token,
                            'scheduled_publish_time': post.get_schedule_timestamp(),
                            'description': message_formatted
                            }
                            post = requests.post(url.format(version='v17.0', endpoint=epupdate), params=media_params)
                            postdata = post.json()
                        else:
                            params = {
                                'access_token': page_access_token,
                                'scheduled_publish_time': post.get_schedule_timestamp(),
                                'message': message_formatted
                            }
                            post = requests.post(url.format(version='v17.0', endpoint=epupdate), params=params)
                            postdata = post.json()
                    else:
                        if obj.mp4():
                            media_params = {
                            'access_token': page_access_token,
                            'description': message_formatted
                            }
                            post = requests.post(url.format(version='v17.0', endpoint=epupdate), params=media_params)
                            postdata = post.json()
                        else:
                            params = {
                                'access_token': page_access_token,
                                'message': message_formatted
                            }
                            post = requests.post(url.format(version='v17.0', endpoint=epupdate), params=params)
                            postdata = post.json()
            else:
                if post.schedule:
                    params = {
                            'access_token': page_access_token,
                            'scheduled_publish_time': post.get_schedule_timestamp(),
                            'message': message_formatted
                            }
                    post = requests.post(url.format(version='v17.0', endpoint=epupdate), params=params)
                    postdata = post.json()
                else:
                    params = {
                            'access_token': page_access_token,
                            'message': message_formatted
                            }
                    post = requests.post(url.format(version='v17.0', endpoint=epupdate), params=params)
                    postdata = post.json()
                
            return JsonResponse({'success': 'return something'})
        
        if call == "removePost":
            user_token = user.meta_token
            urltoken = f'https://graph.facebook.com/v17.0/{id}?fields=access_token&access_token={user_token}'
            response = requests.get(urltoken)
            data = response.json()
            page_access_token = data['access_token']     
            print('success', page_access_token)
            postid = request.POST.get('postid')
            post = FacebookPostPage.objects.get(pk=postid)
            epupdate=f'{post.feed_id}?'
            params = {
                'access_token': page_access_token,
                }
            response = requests.delete(url.format(version='v17.0', endpoint=epupdate), params=params)
            postdata = response.json()
            print(postdata)
            post.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
    else:
        form = FbPostForm()
    
    context = {
        'pageposts': posts,
        'schedules':schedule,
        'form': form,
        'page': page,
    }
    response = render(request, 'stela_control/marketing/meta_business/page/content-pro/main.html', context)
    response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/' 
    return response

def pageAnalythics(request, id):
    lang=request.LANGUAGE_CODE
    url='https://graph.facebook.com/{version}/{endpoint}'
    user=request.user
    user_token = user.meta_token
    urltoken = f'https://graph.facebook.com/v17.0/{id}?fields=access_token&access_token={user_token}'
    response = requests.get(urltoken)
    
    if response.status_code == 200:
        print('El inicio de sesión en la API Graph de Facebook es válido.')
    else:
        print('El inicio de sesión en la API Graph de Facebook no es válido:', response.json())
        return HttpResponseRedirect('/marketing/business-suite')

    data = response.json()
    page_access_token = data['access_token'] 
    values = []
    usage = []
    from babel.dates import format_date
    from datetime import datetime
    from datetime import timedelta
    start_time = datetime.utcnow() - timedelta(days=7)
    end_time = datetime.utcnow()
    epimpressions=f'{id}/insights?metric=page_impressions_unique'
    params = {
        'access_token': page_access_token,
        'period':'day',
        'since':start_time,
        'until':end_time,
    }
    response = requests.get(url.format(version='v17.0', endpoint=epimpressions), params=params)
    postdata = response.json()
    items = postdata['data'][0]['values']
    for item in items:
        value = item['value']
        end_time = item['end_time']
        cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
        if lang == "en":
            week_day = format_date(cleandate, format='EEEE', locale=lang)
        elif lang == "es-ve":
            week_day = format_date(cleandate, format='EEEE', locale="es")
        usage.append(value)
        values.append(week_day)
    
    page=FacebookPage.objects.get(asset_id=id)
    
    context = {
        'values': values,
        'usage': usage,
        'page': page
    }

    if request.method == 'POST':
        
        action = request.POST.get('action')

        if action == "getPosts":
            posts=FacebookPostPage.objects.filter(page=page, is_video=False).order_by('-created')[:20]
            select=render_to_string('stela_control/load-data/meta/page-analythics/post-select.html', {
                'posts': posts
            })
            return JsonResponse({'render':select})
        
        if action == "getPage":
            select=render_to_string('stela_control/load-data/meta/page-analythics/page-select.html', {})
            return JsonResponse({'render':select})

        if action == "getVideo":
            posts=FacebookPostPage.objects.filter(page=page, is_video=True).order_by('-created')[:20]
            select=render_to_string('stela_control/load-data/meta/page-analythics/video-select.html', {
                'posts': posts
            })
            return JsonResponse({'render':select})
        
        if action == "pageMetrics":
            metric=request.POST.get('metric')
            metricname=str(request.POST.get('metricname'))
            starts=request.POST.get('starts')
            values = []
            usage = []
            endpoint=f'{id}/insights?metric={metric}'
            if starts:
                startsclean = datetime.strptime(starts, '%d/%m/%Y')
                since = startsclean.strftime('%Y-%m-%d')
                end_time=request.POST.get('until')
                endclean = datetime.strptime(end_time, '%d/%m/%Y')
                until = endclean.strftime('%Y-%m-%d')
                params = {
                    'access_token': page_access_token,
                    'period':'day',
                    'since':since,
                    'until':until,
                }
            else:
               params = {
                    'access_token': page_access_token,
                } 
            response = requests.get(url.format(version='v17.0', endpoint=endpoint), params=params)
            getdata = response.json()
            if  metricname == "Top Fans Country":
                items = getdata['data']
                if items:
                    data = getdata['data'][0]['values']
                    for item in items: 
                        value = item['value']
                        country = item['country']
                        usage.append(value)
                        values.append(country)
                
                        return JsonResponse({
                            'top':'clear data',
                            'usage': usage,
                            'dates': values,
                            'labeling': _(metricname)
                            })
                else:
                    return JsonResponse({
                        'empty':'clear data',
                        'usage': usage,
                        'dates': values,
                        'labeling': _(metricname)
                        })
            elif  metricname == "Top Fans Gender Age":
                items = getdata['data']
                if items:
                    data = getdata['data'][0]['values']
                    for item in items: 
                        value = item['value']
                        country = item['country']
                        usage.append(value)
                        values.append(country)
                
                        return JsonResponse({
                            'top':'clear data',
                            'usage': usage,
                            'dates': values,
                            'labeling': _(metricname)
                            })
                else:
                    return JsonResponse({
                        'empty':'clear data',
                        'usage': usage,
                        'dates': values,
                        'labeling': _(metricname)
                        })
            
            elif  metricname == "Content Age Gender Impressions":
                items = getdata['data']
                if items:
                    data = getdata['data'][0]['values']
                    for item in items: 
                        value = item['value']
                        country = item['country']
                        usage.append(value)
                        values.append(country)
                
                        return JsonResponse({
                            'top':'clear data',
                            'usage': usage,
                            'dates': values,
                            'labeling': _(metricname)
                            })
                else:
                    return JsonResponse({
                        'empty':'clear data',
                        'usage': usage,
                        'dates': values,
                        'labeling': _(metricname)
                        })
            else:
                items = getdata['data']
                if items:
                    data = getdata['data'][0]['values']
                    for item in data:
                        value = item['value']
                        end_time = item['end_time']
                        cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                        date_formatted = cleandate.strftime('%d-%m-%Y')
                        usage.append(value)
                        values.append(date_formatted)
                    return JsonResponse({
                        'response':'clear data',
                        'usage': usage,
                        'dates': values,
                        'labeling': _(metricname)
                        })
                else:
                    return JsonResponse({
                        'empty':'clear data',
                        'usage': usage,
                        'dates': values,
                        'labeling': _(metricname)
                        })

        if action == "postMetrics":
            metricname=str(request.POST.get('metricname'))
            metric=request.POST.get('metric')
            postid=request.POST.get('postid')
            post=FacebookPostPage.objects.get(pk=postid)
            starts=request.POST.get('starts')
            values = []
            usage = []
            endpoint=f'{post.feed_id}/insights?metric={metric}'
            if starts:
                startsclean = datetime.strptime(starts, '%d/%m/%Y')
                since = startsclean.strftime('%Y-%m-%d')
                end_time=request.POST.get('until')
                endclean = datetime.strptime(end_time, '%d/%m/%Y')
                until = endclean.strftime('%Y-%m-%d')
                params = {
                    'access_token': page_access_token,
                    'period':'day',
                    'since':since,
                    'until':until,
                }
            else: 
               params = {
                    'access_token': page_access_token,
                } 
            
            response = requests.get(url.format(version='v17.0', endpoint=endpoint), params=params)
            getdata = response.json()
            items = getdata['data']
            if items:
                data = getdata['data'][0]['values']
                for item in data:
                    value = item['value']
                    if metricname == "Post Clicks":
                        values.append('Index')
                        values.append(metricname)
                        usage.append(0)
                        usage.append(value)
                    elif metricname == "Likes Total":
                        values.append('Index')
                        values.append(metricname)
                        usage.append(0)
                        usage.append(value)
                    elif metricname == "Love Total":
                        values.append('Index')
                        values.append(metricname)
                        usage.append(0)
                        usage.append(value)
                    elif metricname == "Wow Total":
                        values.append('Index')
                        values.append(metricname)
                        usage.append(0)
                        usage.append(value)
                    elif metricname == "Haha Total":
                        values.append('Index')
                        values.append(metricname)
                        usage.append(0)
                        usage.append(value)
                    elif metricname == "Sorry Total":
                        values.append('Index')
                        values.append(metricname)
                        usage.append(0)
                        usage.append(value)
                    elif metricname == "Anger Total":
                        values.append('Index')
                        values.append(metricname)
                        usage.append(0)
                        usage.append(value)
                    else:
                        end_time = item['end_time']
                        cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                        date_formatted = cleandate.strftime('%d-%m-%Y')
                        values.append(date_formatted)
                        usage.append(value)
                return JsonResponse({
                    'response':'clear data',
                    'usage': usage,
                    'dates': values,
                    'labeling': _(metricname)
                    })
            else:
                return JsonResponse({
                    'empty':'clear data',
                    'usage': usage,
                    'dates': values,
                    'labeling': _(metricname)
                    })
        
        if action == "videoMetrics":
            metricname=str(request.POST.get('metricname'))
            metric=request.POST.get('metric')
            postid=request.POST.get('postid')
            post=FacebookPostPage.objects.get(pk=postid)
            starts=request.POST.get('starts')
            values = []
            usage = []
            endpoint=f'{post.feed_id}/video_insights/{metric}'
            params = {
                'access_token': page_access_token,
                } 
            
            response = requests.get(url.format(version='v17.0', endpoint=endpoint), params=params)
            getdata = response.json()
            items = getdata['data']
            if items:
                data = getdata['data'][0]['values']
                for item in data:
                    value = item['value']
                    values.append('Index')
                    values.append(metricname)
                    usage.append(0)
                    usage.append(value)
                return JsonResponse({
                    'response':'clear data',
                    'usage': usage,
                    'dates': values,
                    'labeling': _(metricname)
                    })
            else:
                return JsonResponse({
                    'empty':'clear data',
                    'usage': usage,
                    'dates': values,
                    'labeling': _(metricname)
                    })
    
    response = render(request, 'stela_control/marketing/meta_business/page/page-analythics/main.html', context)
    response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/' 
    return response

def pageCommunity(request, id):
    today = datetime.now()
    page=FacebookPage.objects.get(asset_id=id)
    events=FacebookPageEvent.objects.filter(page=page, created__gt=today)
    form=FacebookEventsForm()
    url='https://graph.facebook.com/{version}/{endpoint}'
    user=request.user
    user_token = user.meta_token
    urltoken = f'https://graph.facebook.com/v17.0/{id}?fields=access_token&access_token={user_token}'
    response = requests.get(urltoken)
    data = response.json()
    page_access_token = data['access_token'] 
    posts=FacebookPostPage.objects.filter(page=page)
    for post in posts:
        comments=FacebookPageComments.objects.filter(post=post)

        if comments:
            if FacebookPageComments.objects.filter(update_rate__gte=today):
                for post in posts:
                    endpoint=f'{post.feed_id}/comments'
                    params = {
                        'access_token': page_access_token,
                        } 
                    
                    response = requests.get(url.format(version='v17.0', endpoint=endpoint), params=params)
                    getdata = response.json()
                    for obj in getdata['data']:
                        for comment in comments:
                            if comment.comment_id == obj['id']:
                                pass
                            else:
                                if obj['id']:
                                    FacebookPageComments.objects.create(
                                        post=post,
                                        from_user=obj['from']['name'],
                                        from_user_id=obj['from']['id'],
                                        comment=obj['message'],
                                        comment_id=obj['id']
                                    )
            else:
                pass
        else:
            for post in posts:
                endpoint=f'{post.feed_id}/comments'
                params = {
                    'access_token': page_access_token,
                    } 
                    
                response = requests.get(url.format(version='v17.0', endpoint=endpoint), params=params)
                getdata = response.json()
                for obj in getdata['data']:
                    if obj['id']:
                        FacebookPageComments.objects.create(
                            post=post,
                            from_user=obj['from']['name'],
                            from_user_id=obj['from']['id'],
                            comment=obj['message'],
                            comment_id=obj['id']
                        )

    if request.method == "POST":
        call = request.POST.get('form-id')
        action = request.POST.get('action')
        
        if call == "eventform":
            endpoint='official_events'
            form = FacebookEventsForm(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit=False)
                event.page = page
                event.save()

                obj = FacebookPageEvent.objects.get(pk=event.id)
                start_time=obj.start_time.strftime("%Y-%m-%dT%H:%M:%S")
                roles = {
                    id: "PRIMARY_PERFORMER"
                }
                cover = {
                    "source": obj.get_url(),
                    "offset_x": 0,
                    "offset_y": 0
                }

                params = {
                    'name': obj.name,
                    'description': obj.description,
                    'status': obj.status,
                    'place_id': id,
                    'type': obj.type,
                    'category': obj.category,
                    'start_time': start_time,
                    'cover': cover,
                    'roles': roles,
                    'timezone': "US/Pacific",
                    'access_token': page_access_token
                }

                response = requests.post(url.format(version='v17.0', endpoint=endpoint), json=params)
                getdata = response.json()
                print(getdata)

                return JsonResponse({'success': 'return something'})
            else:
                form = FacebookEventsForm()

        if call == "eventupdate":
            eventid = request.POST.get('parent')
            event = FacebookPageEvent.objects.get(pk=eventid)
            form = FacebookEventsForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                post = form.save(commit=False)
                post.page = page
                post.save()
                return JsonResponse({'success': 'return something'})
            else:
                form = FacebookEventsForm()

        if action == "updateEvent":
            eventid=request.POST.get('eventid')
            event=FacebookPageEvent.objects.get(pk=eventid)
            form = FacebookEventsForm(instance=event)
            formdata = render_to_string('stela_control/load-data/meta/community/formdata.html', {
                    'form': form,
                    'event': event
                    })
            return JsonResponse({'response': formdata})

        if action == "removeEvent":
            # user_token = user.meta_token
            # urltoken = f'https://graph.facebook.com/v17.0/{id}?fields=access_token&access_token={user_token}'
            # response = requests.get(urltoken)
            # data = response.json()
            # page_access_token = data['access_token']     
            # print('success', page_access_token)
            eventid = request.POST.get('eventid')
            event = FacebookPageEvent.objects.get(pk=eventid)
            # epupdate=f'{post.feed_id}?'
            # params = {
            #     'access_token': page_access_token,
            #     }
            # response = requests.delete(url.format(version='v17.0', endpoint=epupdate), params=params)
            # postdata = response.json()
            # print(postdata)
            event.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
    context = {
        'page': page,
        'form': form,
        'events': events,
        'comments': comments
    }

    response = render(request, 'stela_control/marketing/meta_business/page/community/main.html', context)
    response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/' 
    return response

def create_facebook_event(access_token, name, description, category, start_time, place_id, page_id, event_role, image_url):
    url = "https://graph.facebook.com/v2.8/official_events"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "name": "Get Started with Ticketing",
        "description": "This is the best place to buy your first ticket",
        "access_token": access_token,
        "place_id": place_id,
        "cover": {
            "source": image_url,
            "offset_x": 0,
            "offset_y": 0,
        },
        "category": "FAMILY_EVENT",
        "timezone": "US/Pacific",
        "start_time": "2012-03-24T17:45:12",  # Formato ISO 8601
        "roles": {page_id: event_role},
    }

    response = requests.post(url, json=data, headers=headers)
    return response

def process_facebook_events(events_json):
    processed_events = []
    for event in events_json:
        processed_events.append({
            'description': event.get('description'),
            'name': event.get('name'),
            'place': event.get('place', {}).get('name'),
            'location': event.get('place', {}).get('location'),
            'start_time': event.get('start_time'),
            'id': event.get('id')
        })
    return processed_events

def view_facebook_events(access_token):

    url = "https://graph.facebook.com/v14.0/<PAGE_ID>/events"
    
    params = {'access_token': 'tu_access_token'}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        events_json = response.json()
        events = process_facebook_events(events_json)
        
    return events

def insightCreative(request, id, ig):
    lang=request.LANGUAGE_CODE
    country_id = str(lang).split('-')
    get_timezone = country_timezones(country_id[1])[0]
    user=request.user
    url = 'https://graph.facebook.com/v13.0/me'
    params = {
        'access_token': user.meta_token
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print('El inicio de sesión en la API Graph de Facebook es válido.')
    else:
        print('El inicio de sesión en la API Graph de Facebook no es válido:', response.json())
        return HttpResponseRedirect('/marketing/business-suite')

    page=FacebookPage.objects.get(asset_id=id)
    ig_account=InstagramAccount.objects.get(asset_id=ig)
    url='https://graph.facebook.com/{version}/{endpoint}'
    epigpost=f'{ig}/media?'
    schedule = []
    feed=IGPost.objects.filter(parent=ig_account).order_by('-schedule')[:10]
    month_ago = timezone.now() - timedelta(weeks=4)
    feed_calendar=IGPost.objects.filter(parent=ig_account, created__gte=month_ago)
    for post in feed_calendar:
        get_media=IGMediaContent.objects.filter(post=post).order_by('id').first()
        if post.status == "publish":
            message_formatted = caption_optimizer(post.caption)
            string=message_formatted.split()
            title=" ".join(string[:4])
            titlebox=" ".join(string[:10])
            if get_media.mp4():
                if get_media.get_cover():
                    planning_data = {
                        'id': post.pk,
                        'title': title, 
                        'start': post.schedule.isoformat(), 
                        'extendedProps': {
                            'fullTitle': titlebox,
                            'mediaUrl': get_media.get_cover(),
                            'mediatype': post.mediatype,
                            'cover': 'true'
                        },
                        'allDay': False, 
                    }
                else:
                    planning_data = {
                        'id': post.pk,
                        'title': title, 
                        'start': post.schedule.isoformat(), 
                        'extendedProps': {
                            'fullTitle': titlebox,
                            'mediaUrl': get_media.get_url(),
                            'mediatype': post.mediatype,
                            'cover': 'false',
                        },
                        'allDay': False, 
                    }
            else:
                planning_data = {
                    'id': post.pk,
                    'title':title, 
                    'start': post.created.isoformat(), 
                    'extendedProps': {
                        'fullTitle': titlebox,
                        'mediaUrl': get_media.get_url(),
                        'mediatype': post.mediatype,
                    },
                    'allDay': False, 
                }
        else:
            message_formatted = caption_optimizer(post.caption)
            string=message_formatted.split()
            title=" ".join(string[:4])
            titlebox=" ".join(string[:10])
            if get_media.mp4():
                if get_media.get_cover():
                    planning_data = {
                        'id': post.pk,
                        'title': title, 
                        'start': post.schedule.isoformat(), 
                        'extendedProps': {
                            'fullTitle': titlebox,
                            'mediaUrl': get_media.get_cover(),
                            'mediatype': post.mediatype,
                            'cover': 'true'
                        },
                        'allDay': False, 
                    }
                else:
                    planning_data = {
                        'id': post.pk,
                        'title': title, 
                        'start': post.schedule.isoformat(), 
                        'extendedProps': {
                            'fullTitle': titlebox,
                            'mediaUrl': get_media.get_url(),
                            'mediatype': post.mediatype,
                            'cover': 'false',
                        },
                        'allDay': False, 
                    }
            else:
                planning_data = {
                    'id': post.pk,
                    'title': title, 
                    'start': post.schedule.isoformat(), 
                    'extendedProps': {
                        'fullTitle': titlebox,
                        'mediaUrl': get_media.get_url(),
                        'mediatype': post.mediatype,
                    },
                    'allDay': False, 
                }
        schedule.append(planning_data)
    calendar_data = json.dumps(schedule)
    form=IGPostForm()
    form2=IGMediaForm()
    formgrid=SendGridForm()

    if request.method == 'POST':
        pattern = r'^[A-Za-z \-]+$'
        action = request.POST.get('form-id')
        call = request.POST.get('action')
        print(action)
        print(call)

        if call == "postCounter":
            feed=IGPost.objects.filter(parent=ig_account).count()
            if feed >= 3:    
                return JsonResponse({'counter': 'return something'}) 
        
        if call == "metadataPost":
            pk=request.POST.get('postid')
            post=IGPost.objects.get(pk=pk)
            new_pages = render_to_string('stela_control/load-data/meta/tooltip.html', {
                            'post': post
                        })
            return JsonResponse({'response': new_pages})
            
        if call == "userTag":
            usertags=request.POST.getlist('usertag[]')
            feed_id=request.POST.get('feed')
            for user in usertags:
                if re.match(pattern, user):
                    iguser=str(user)
                    cleaniguser=iguser.replace("@", "")
                    IGUserTag.objects.create(
                        post_id=feed_id,
                        igname=cleaniguser
                    )

        if call == "audioName":
            audioname=request.POST.get('audioname')
            feed_id=request.POST.get('feed')
            if re.match(pattern, audioname):
                IGPost.objects.filter(pk=feed_id).update(audioname=audioname)
        
        if action == "postform":
            form_date_str = request.POST.get('schedule')
            form = IGPostForm(request.POST)
            form2 = IGMediaForm(request.POST, request.FILES)
            if all([form2.is_valid(),
                    form.is_valid(),
                ]):
                post = form.save(commit=False)
                post.parent = ig_account
                post.save()
                IGPost.objects.filter(pk=post.pk).update(schedule=form_date_str)

                if form2.files:
                    media = form2.save(commit=False)
                    media.post = post
                    media.save()
                
                return JsonResponse({'postid': post.pk})
            else:
                print(form.errors)
                form = IGPostForm()
        
        if action == "formUpdate":
            postid=request.POST.get('feed-id')
            form_date_str = request.POST.get('schedule')
            caption = request.POST.get('update-caption')
            igpost = get_object_or_404(IGPost, pk=postid)
            form = IGPostForm(request.POST, instance=igpost, prefix="update")
            print(caption)
            print(form.is_valid())
            if form.is_valid():
                post = form.save(commit=False)
                post.parent = ig_account
                post.caption = caption
                post.save()

                IGPost.objects.filter(pk=post.pk).update(schedule=form_date_str)
                
                return JsonResponse({'postid': igpost.pk})
            else:
                form = IGPostForm(instance=post)
                print(form.errors)
        
        if call == "updateFeed":
            feed_id=request.POST.get('feed_id')
            feed=IGPost.objects.get(pk=feed_id)
            form=IGPostForm(instance=feed, prefix="update")
            content = render_to_string('stela_control/load-data/meta/ic-update/content.html', {
                    'form': form,
                    })
                  
            return JsonResponse({
                'content': content,
                'feed_id': feed.pk,
                'getdate': feed.schedule
                }) 
        
        if call == "removeFeed":
            feed_id=request.POST.get('feed_id')
            feed=IGPost.objects.get(pk=feed_id)
            feed.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})      
        
        if call == "postIG":
            user_token = user.meta_token
            urltoken = f'https://graph.facebook.com/v17.0/{id}?fields=access_token&access_token={user_token}'
            response = requests.get(urltoken)
            data = response.json()
            page_access_token = data['access_token'] 
            feed_id=request.POST.get('feed_id')
            feed=IGPost.objects.get(pk=feed_id)
            get_feed=IGPost.objects.filter(pk=feed_id)
            message_formatted = caption_optimizer(feed.caption)
            media=IGMediaContent.objects.filter(post=feed)
            usertags=IGUserTag.objects.filter(post=feed)
            tagdata = []
            container_items = []
            if media.count() > 1:
                get_feed.update(mediatype="CAROUSEL")
            else:
                get_feed.update(mediatype=feed.mediatype)
            if feed.status == "publish": 
                if media.count() > 1:
                    for i, tag in enumerate(usertags):
                        if i == 0:
                            cleantag = {'username': tag.igname, 'x': 0.5, 'y': 0.8}
                            tagdata.append(cleantag)
                        elif i == 1:
                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.1}
                            tagdata.append(cleantag)
                        elif i == 2:
                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.1}
                            tagdata.append(cleantag)
                        elif i == 3:
                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.8}
                            tagdata.append(cleantag)
                        elif i == 4:
                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.8}
                            tagdata.append(cleantag)
                    usertaglist = json.dumps(tagdata)  
                    print(usertaglist)
                    for item in media:
                        if usertags.exists():  
                            if item.mp4():
                                media_params = {
                                    'media_type':'VIDEO',
                                    'video_url':item.get_url(),
                                    'is_carousel_item': 'true',
                                    'access_token': page_access_token,
                                    'user_tags': usertaglist,
                                }
                            else:
                                media_params = {
                                    'image_url':item.get_url(),
                                    'is_carousel_item': 'true',
                                    'access_token': page_access_token,
                                    'user_tags': usertaglist,
                                }
                        else:
                            if item.mp4():
                                media_params = {
                                    'media_type':'VIDEO',
                                    'video_url':item.get_url(),
                                    'is_carousel_item': 'true',
                                    'access_token': page_access_token,
                                    'user_tags': usertaglist,
                                }
                            else:
                                media_params = {
                                    'image_url':item.get_url(),
                                    'is_carousel_item': 'true',
                                    'access_token': page_access_token,
                                }
                        container = requests.post(url.format(version='v17.0', endpoint=epigpost), params=media_params)
                        data = container.json()
                        print(data)
                        container_items.append(data['id'])
                    containers = json.dumps(container_items)
                    item_params = {
                        "caption": message_formatted,
                        "media_type": "CAROUSEL",
                        "children": containers,
                        "location_id": id,
                        "access_token": page_access_token
                        }
                    get_feed.update(token=page_access_token)
                    carousel = requests.post(url.format(version='v17.0', endpoint=epigpost), params=item_params)
                    data = carousel.json()
                    print(data)
                    try:
                        if data['error']['message'] == "Invalid user id":
                            feed.delete()
                            return JsonResponse({'error': _('Post cannot be processed due to invalid user tagging')})
                    except:
                        pass
                   
                    creation_id=data['id']
                    epcheckpost=f'{creation_id}?'
                    params = {
                        'fields':'status_code',
                        'access_token': page_access_token,
                    }
                    upstatus = requests.get(url.format(version='v17.0', endpoint=epcheckpost), params=params)
                    updata = upstatus.json()
                    print('checkpost')
                    IGPost.objects.filter(pk=feed.pk).update(status="in_progress", container_id=creation_id, publish_status=updata['status_code'])
     
                else:
                    for item in media:
                        if feed.mediatype == "REELS":
                            get_feed.update(token=page_access_token, mediatype="REELS")
                            if item.get_cover():
                                if usertags.exists():
                                    for i, tag in enumerate(usertags):
                                        if i == 0:
                                            cleantag = {'username': tag.igname}
                                            tagdata.append(cleantag)
                                        elif i == 1:
                                            cleantag = {'username': tag.igname}
                                            tagdata.append(cleantag)
                                        elif i == 2:
                                            cleantag = {'username': tag.igname}
                                            tagdata.append(cleantag)
                                        elif i == 3:
                                            cleantag = {'username': tag.igname}
                                            tagdata.append(cleantag)
                                        elif i == 4:
                                            cleantag = {'username': tag.igname}
                                            tagdata.append(cleantag)
                                    usertaglist = json.dumps(tagdata) 
                                    print(usertaglist)
                                    media_params = {
                                        'media_type': 'REELS',
                                        'user_tags': usertaglist,
                                        'audio_name': feed.audioname,
                                        'cover_url': item.get_cover(),
                                        'share_to_feed': 'true',
                                        'video_url':item.get_url(),
                                        'caption': message_formatted,
                                        'location_id': id,
                                        'access_token': page_access_token,
                                    }
                                    
                                else:
                                    media_params = {
                                        'media_type': 'REELS',
                                        'audio_name': feed.audioname,
                                        'cover_url': item.get_cover(),
                                        'share_to_feed': 'true',
                                        'video_url':item.get_url(),
                                        'caption': message_formatted,
                                        'location_id': id,
                                        'access_token': page_access_token,
                                    }
                            else:
                                if usertags.exists():
                                    for i, tag in enumerate(usertags):
                                        if i == 0:
                                            cleantag = {'username': tag.igname, 'x': 0.5, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 1:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 2:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 3:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 4:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.8}
                                            tagdata.append(cleantag)
                                    usertaglist = json.dumps(tagdata) 
                                    print(usertaglist)
                                    media_params = {
                                        'media_type': 'REELS',
                                        'user_tags': usertaglist,
                                        'audio_name': feed.audioname,
                                        'share_to_feed': 'true',
                                        'video_url':item.get_url(),
                                        'caption': message_formatted,
                                        'location_id': id,
                                        'access_token': page_access_token,
                                    }
                                else:
                                    media_params = {
                                        'media_type': 'REELS',
                                        'audio_name': feed.audioname,
                                        'share_to_feed': 'true',
                                        'video_url':item.get_url(),
                                        'caption': message_formatted,
                                        'location_id': id,
                                        'access_token': page_access_token,
                                    }
                        elif feed.mediatype == "STORIES":
                                get_feed.update(token=page_access_token, mediatype="STORIES")
                                if usertags.exists():
                                    for i, tag in enumerate(usertags):
                                        if i == 0:
                                            cleantag = {'username': tag.igname, 'x': 0.5, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 1:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 2:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 3:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 4:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.8}
                                            tagdata.append(cleantag)
                                    usertaglist = json.dumps(tagdata) 
                                    print(usertaglist)
                                    if item.mp4():
                                        media_params = {
                                            'user_tags': usertaglist,
                                            'media_type': feed.mediatype,
                                            'video_url':item.get_url(),
                                            'caption': message_formatted,
                                            'location_id': id,
                                            'access_token': page_access_token,
                                        }
                                    else:
                                        media_params = {
                                            'user_tags': usertaglist,
                                            'media_type': feed.mediatype,
                                            'image_url':item.get_url(),
                                            'caption': message_formatted,
                                            'location_id': id,
                                            'access_token': page_access_token,
                                        }
                                else:
                                    if item.mp4():
                                        media_params = {
                                            'media_type': feed.mediatype,
                                            'video_url':item.get_url(),
                                            'caption': message_formatted,
                                            'location_id': id,
                                            'access_token': page_access_token,
                                        }
                                    else:
                                        media_params = {
                                            'media_type': feed.mediatype,
                                            'image_url':item.get_url(),
                                            'caption': message_formatted,
                                            'location_id': id,
                                            'access_token': page_access_token,
                                        }   
                        else:
                            get_feed.update(token=page_access_token, mediatype="POST")
                            if usertags.exists():
                                for tag in usertags:
                                    for i, tag in enumerate(usertags):
                                        if i == 0:
                                            cleantag = {'username': tag.igname, 'x': 0.5, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 1:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 2:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 3:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 4:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.8}
                                            tagdata.append(cleantag)
                                usertaglist = json.dumps(tagdata)
                                print(usertaglist)
                                media_params = {
                                    'user_tags': usertaglist,
                                    'image_url':item.get_url(),
                                    'caption': message_formatted,
                                    'location_id': id,
                                    'access_token': page_access_token,
                                }
                            else:
                                media_params = {
                                    'image_url':item.get_url(),
                                    'caption': message_formatted,
                                    'location_id': id,
                                    'access_token': page_access_token,
                                }
                        container = requests.post(url.format(version='v17.0', endpoint=epigpost), params=media_params)
                        data = container.json()
                        print(data)
                        try:
                            if data['error']['message'] == "Invalid user id":
                                feed.delete()
                                return JsonResponse({'error': _('Post cannot be processed due to invalid user tagging')})
                        except:
                            pass
                        creation_id=data['id']
                        epcheckpost=f'{creation_id}?'
                        params = {
                            'fields':'status_code',
                            'access_token': page_access_token,
                        }
                        upstatus = requests.get(url.format(version='v17.0', endpoint=epcheckpost), params=params)
                        updata = upstatus.json()
                        IGPost.objects.filter(pk=feed.pk).update(status="in_progress", container_id=creation_id, publish_status=updata['status_code'])
                
                return JsonResponse({'success': _('Your post will be active check here in a minute')}) 
            return JsonResponse({'success': _('Your post will be archived in draft')}) 
        
        
        if call == "updateIG":
            user_token = user.meta_token
            urltoken = f'https://graph.facebook.com/v17.0/{id}?fields=access_token&access_token={user_token}'
            response = requests.get(urltoken)
            data = response.json()
            page_access_token = data['access_token'] 
            feed_id=request.POST.get('feed_id')
            feed=IGPost.objects.get(pk=feed_id)
            get_feed=IGPost.objects.filter(pk=feed_id)
            message_formatted = caption_optimizer(feed.caption)
            media=IGMediaContent.objects.filter(post=feed)
            usertags=IGUserTag.objects.filter(post=feed)
            tagdata = []
            container_items = []
            if feed.status == "publish": 
                if media.count() > 1:
                    for i, tag in enumerate(usertags):
                        if i == 0:
                            cleantag = {'username': tag.igname, 'x': 0.5, 'y': 0.8}
                            tagdata.append(cleantag)
                        elif i == 1:
                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.1}
                            tagdata.append(cleantag)
                        elif i == 2:
                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.1}
                            tagdata.append(cleantag)
                        elif i == 3:
                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.8}
                            tagdata.append(cleantag)
                        elif i == 4:
                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.8}
                            tagdata.append(cleantag)
                    usertaglist = json.dumps(tagdata)  
                    print(usertaglist)
                    for item in media:
                        if usertags.exists():  
                            if item.mp4():
                                media_params = {
                                    'media_type':'VIDEO',
                                    'video_url':item.get_url(),
                                    'is_carousel_item': 'true',
                                    'access_token': page_access_token,
                                    'user_tags': usertaglist,
                                }
                            else:
                                media_params = {
                                    'image_url':item.get_url(),
                                    'is_carousel_item': 'true',
                                    'access_token': page_access_token,
                                    'user_tags': usertaglist,
                                }
                        else:
                            if item.mp4():
                                media_params = {
                                    'media_type':'VIDEO',
                                    'video_url':item.get_url(),
                                    'is_carousel_item': 'true',
                                    'access_token': page_access_token,
                                    'user_tags': usertaglist,
                                }
                            else:
                                media_params = {
                                    'image_url':item.get_url(),
                                    'is_carousel_item': 'true',
                                    'access_token': page_access_token,
                                }
                        container = requests.post(url.format(version='v17.0', endpoint=epigpost), params=media_params)
                        data = container.json()
                        print(data)
                        container_items.append(data['id'])
                    containers = json.dumps(container_items)
                    item_params = {
                        "caption": message_formatted,
                        "media_type": "CAROUSEL",
                        "children": containers,
                        "location_id": id,
                        "access_token": page_access_token
                        }
                    get_feed.update(token=page_access_token)
                    carousel = requests.post(url.format(version='v17.0', endpoint=epigpost), params=item_params)
                    data = carousel.json()
                    print(data)
                    try:
                        if data['error']['message'] == "Invalid user id":
                            feed.delete()
                            return JsonResponse({'error': _('Post cannot be processed due to invalid user tagging')})
                    except:
                        pass
                   
                    creation_id=data['id']
                    epcheckpost=f'{creation_id}?'
                    params = {
                        'fields':'status_code',
                        'access_token': page_access_token,
                    }
                    upstatus = requests.get(url.format(version='v17.0', endpoint=epcheckpost), params=params)
                    updata = upstatus.json()
                    print('checkpost')
                    IGPost.objects.filter(pk=feed.pk).update(status="in_progress", container_id=creation_id, publish_status=updata['status_code'])
     
                else:
                    for item in media:
                        if feed.mediatype == "REELS":
                            get_feed.update(token=page_access_token, mediatype="REELS")
                            if item.get_cover():
                                if usertags.exists():
                                    for i, tag in enumerate(usertags):
                                        if i == 0:
                                            cleantag = {'username': tag.igname}
                                            tagdata.append(cleantag)
                                        elif i == 1:
                                            cleantag = {'username': tag.igname}
                                            tagdata.append(cleantag)
                                        elif i == 2:
                                            cleantag = {'username': tag.igname}
                                            tagdata.append(cleantag)
                                        elif i == 3:
                                            cleantag = {'username': tag.igname}
                                            tagdata.append(cleantag)
                                        elif i == 4:
                                            cleantag = {'username': tag.igname}
                                            tagdata.append(cleantag)
                                    usertaglist = json.dumps(tagdata) 
                                    print(usertaglist)
                                    media_params = {
                                        'media_type': 'REELS',
                                        'user_tags': usertaglist,
                                        'audio_name': feed.audioname,
                                        'cover_url': item.get_cover(),
                                        'share_to_feed': 'true',
                                        'video_url':item.get_url(),
                                        'caption': message_formatted,
                                        'location_id': id,
                                        'access_token': page_access_token,
                                    }
                                    
                                else:
                                    media_params = {
                                        'media_type': 'REELS',
                                        'audio_name': feed.audioname,
                                        'cover_url': item.get_cover(),
                                        'share_to_feed': 'true',
                                        'video_url':item.get_url(),
                                        'caption': message_formatted,
                                        'location_id': id,
                                        'access_token': page_access_token,
                                    }
                            else:
                                if usertags.exists():
                                    for i, tag in enumerate(usertags):
                                        if i == 0:
                                            cleantag = {'username': tag.igname, 'x': 0.5, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 1:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 2:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 3:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 4:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.8}
                                            tagdata.append(cleantag)
                                    usertaglist = json.dumps(tagdata) 
                                    print(usertaglist)
                                    media_params = {
                                        'media_type': 'REELS',
                                        'user_tags': usertaglist,
                                        'audio_name': feed.audioname,
                                        'share_to_feed': 'true',
                                        'video_url':item.get_url(),
                                        'caption': message_formatted,
                                        'location_id': id,
                                        'access_token': page_access_token,
                                    }
                                else:
                                    media_params = {
                                        'media_type': 'REELS',
                                        'audio_name': feed.audioname,
                                        'share_to_feed': 'true',
                                        'video_url':item.get_url(),
                                        'caption': message_formatted,
                                        'location_id': id,
                                        'access_token': page_access_token,
                                    }
                        elif feed.mediatype == "STORIES":
                                get_feed.update(token=page_access_token, mediatype="STORIES")
                                if usertags.exists():
                                    for i, tag in enumerate(usertags):
                                        if i == 0:
                                            cleantag = {'username': tag.igname, 'x': 0.5, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 1:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 2:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 3:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 4:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.8}
                                            tagdata.append(cleantag)
                                    usertaglist = json.dumps(tagdata) 
                                    print(usertaglist)
                                    if item.mp4():
                                        media_params = {
                                            'user_tags': usertaglist,
                                            'media_type': feed.mediatype,
                                            'video_url':item.get_url(),
                                            'caption': message_formatted,
                                            'location_id': id,
                                            'access_token': page_access_token,
                                        }
                                    else:
                                        media_params = {
                                            'user_tags': usertaglist,
                                            'media_type': feed.mediatype,
                                            'image_url':item.get_url(),
                                            'caption': message_formatted,
                                            'location_id': id,
                                            'access_token': page_access_token,
                                        }
                                else:
                                    if item.mp4():
                                        media_params = {
                                            'media_type': feed.mediatype,
                                            'video_url':item.get_url(),
                                            'caption': message_formatted,
                                            'location_id': id,
                                            'access_token': page_access_token,
                                        }
                                    else:
                                        media_params = {
                                            'media_type': feed.mediatype,
                                            'image_url':item.get_url(),
                                            'caption': message_formatted,
                                            'location_id': id,
                                            'access_token': page_access_token,
                                        }   
                        else:
                            get_feed.update(token=page_access_token, mediatype="POST")
                            if usertags.exists():
                                for tag in usertags:
                                    for i, tag in enumerate(usertags):
                                        if i == 0:
                                            cleantag = {'username': tag.igname, 'x': 0.5, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 1:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 2:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.1}
                                            tagdata.append(cleantag)
                                        elif i == 3:
                                            cleantag = {'username': tag.igname, 'x': 0.8, 'y': 0.8}
                                            tagdata.append(cleantag)
                                        elif i == 4:
                                            cleantag = {'username': tag.igname, 'x': 0.1, 'y': 0.8}
                                            tagdata.append(cleantag)
                                usertaglist = json.dumps(tagdata)
                                print(usertaglist)
                                media_params = {
                                    'user_tags': usertaglist,
                                    'image_url':item.get_url(),
                                    'caption': message_formatted,
                                    'location_id': id,
                                    'access_token': page_access_token,
                                }
                            else:
                                media_params = {
                                    'image_url':item.get_url(),
                                    'caption': message_formatted,
                                    'location_id': id,
                                    'access_token': page_access_token,
                                }
                        container = requests.post(url.format(version='v17.0', endpoint=epigpost), params=media_params)
                        data = container.json()
                        print(data)
                        try:
                            if data['error']['message'] == "Invalid user id":
                                feed.delete()
                                return JsonResponse({'error': _('Post cannot be processed due to invalid user tagging')})
                        except:
                            pass
                        creation_id=data['id']
                        epcheckpost=f'{creation_id}?'
                        params = {
                            'fields':'status_code',
                            'access_token': page_access_token,
                        }
                        upstatus = requests.get(url.format(version='v17.0', endpoint=epcheckpost), params=params)
                        updata = upstatus.json()
                        IGPost.objects.filter(pk=feed.pk).update(status="in_progress", container_id=creation_id, publish_status=updata['status_code'])
                
                return JsonResponse({'success': _('Your post will be active check here in a minute')}) 
            return JsonResponse({'success': _('Your post will be archived in draft')}) 
        
        if action == "sendgrid-form":
            site_cookie=SiteData(request)
            form = SendGridForm(request.POST)
            if form.is_valid():
                html_content = render_to_string('stela_control/emails-template/marketing/content-planner-email.html', {
                    'client':form.cleaned_data['client'],
                    'report':form.cleaned_data['message'],
                    'id_page':id,
                    'lang': lang,
                    'id_instagram':ig,
                    'company': site_cookie.company_public()
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            form.cleaned_data['subject'],
                            text_content,
                            settings.STELA_EMAIL,
                            [form.cleaned_data['email']]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return JsonResponse({'success':_('Your content grid was sent successfully')})
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})
        
    context = {
        'calendar_data': calendar_data,
        'page': page,
        'feed': feed,
        'instagram': ig_account,
        'form': form,
        'form2': form2,
        'formgrid': formgrid,
        'usertz': get_timezone,
    }

    response = render(request, 'stela_control/marketing/meta_business/instagram/insight-creative/main.html', context)
    response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/' 
    return response

def igAnalyzer(request, id, ig):
    lang=request.LANGUAGE_CODE
    page=FacebookPage.objects.get(asset_id=id)
    account=InstagramAccount.objects.get(asset_id=ig)
    url='https://graph.facebook.com/{version}/{endpoint}'
    user=request.user
    user_token = user.meta_token
    urltoken = f'https://graph.facebook.com/v17.0/{id}?fields=access_token&access_token={user_token}'
    response = requests.get(urltoken)
    formgrid=SendGridForm()
    
    if response.status_code == 200:
        print('El inicio de sesión en la API Graph de Facebook es válido.')
    else:
        print('El inicio de sesión en la API Graph de Facebook no es válido:', response.json())
        return HttpResponseRedirect('/marketing/business-suite')

    data = response.json()
    page_access_token = data['access_token'] 
    values_reach = []
    usage_reach = []
    total_reach = 0
    values_followers = []
    usage_followers = []
    total_followers = 0
    usage_linkclicks = []
    values_linkclicks = []
    total_linkclicks = 0
    usage_impressions = []
    values_impressions = []
    total_impressions = 0
    usage_profile_views = []
    values_profile_views = []
    total_profile_views = 0
    usage_male = []
    usage_female = []
    values_gender = []
    label_gender = []
    values_gender_calc = []
    label_city = []
    qty_city_values = []
    label_country = []
    qty_country_values = []
    total_count = 0 
    total_count2 = 0 
    total_count3 = 0 
    total_count4 = 0 
    total_count5 = 0 
    avg_reach = 0
    avg_followers = 0
    avg_linkclicks = 0
    avg_profile_views = 0
    avg_impressions = 0
    call = ""

    from babel.dates import format_date
    from datetime import datetime
    from datetime import timedelta
    start_time = datetime.utcnow() - timedelta(days=14)
    end_time = datetime.utcnow()
    epmetrics=f'{ig}/insights?metric=follower_count,reach,website_clicks,impressions,profile_views'
    params = {
        'access_token': page_access_token,
        'period':'day',
        'since':start_time,
        'until':end_time,
    }
    response = requests.get(url.format(version='v17.0', endpoint=epmetrics), params=params)
    postdata = response.json()
    for retrieve in postdata['data']:
        if retrieve['name'] == 'reach':
            reach = retrieve['values']
            for item in reach:
                value = item['value']
                end_time = item['end_time']
                cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                if lang == "en":
                    week_day = format_date(cleandate, format='MMM d, \'YY', locale=lang)
                elif lang == "es-ve":
                    week_day = format_date(cleandate, format='MMM d, \'YY', locale="es")
                usage_reach.append(value)
                values_reach.append(week_day)
                total_reach += value
                total_count2 += 1
            if total_reach > 0:
                avg2 = total_reach / total_count2
                avg_reach = round(avg2, 2)

        elif retrieve['name'] == 'follower_count':
            followers = retrieve['values']
            for item in followers:
                value = item['value']
                end_time = item['end_time']
                cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                if lang == "en":
                    week_day = format_date(cleandate, format='MMM d, \'YY', locale=lang)
                elif lang == "es-ve":
                    week_day = format_date(cleandate, format='MMM d, \'YY', locale="es")
                usage_followers.append(value)
                values_followers.append(week_day)
                total_followers += value
                total_count += 1
            if total_followers > 0:
                avg = total_followers / total_count
                avg_followers = round(avg, 2)

        elif retrieve['name'] == 'website_clicks':
            link_clicks = retrieve['values']
            for item in link_clicks:
                value = item['value']
                end_time = item['end_time']
                cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                if lang == "en":
                    week_day = format_date(cleandate, format='MMM d, \'YY', locale=lang)
                elif lang == "es-ve":
                    week_day = format_date(cleandate, format='MMM d, \'YY', locale="es")
                usage_linkclicks.append(value)
                values_linkclicks.append(week_day)
                total_linkclicks += value
                total_count3 += 1    
            if total_linkclicks > 0:
                avg3 = total_linkclicks / total_count3
                avg_linkclicks = round(avg3, 2)
            

        elif retrieve['name'] == 'impressions':
            impressions = retrieve['values']
            for item in impressions:
                value = item['value']
                end_time = item['end_time']
                cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                if lang == "en":
                    week_day = format_date(cleandate, format='MMM d, \'YY', locale=lang)
                elif lang == "es-ve":
                    week_day = format_date(cleandate, format='MMM d, \'YY', locale="es")
                usage_impressions.append(value)
                values_impressions.append(week_day)
                total_impressions += value
                total_count4 += 1
            if total_impressions > 0:
                avg4 = total_impressions / total_count4
                avg_impressions = round(avg4, 2)
            
    
        elif retrieve['name'] == 'profile_views':
            profile_views = retrieve['values']
            for item in profile_views:
                value = item['value']
                end_time = item['end_time']
                cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                if lang == "en":
                    week_day = format_date(cleandate, format='MMM d, \'YY', locale=lang)
                elif lang == "es-ve":
                    week_day = format_date(cleandate, format='MMM d, \'YY', locale="es")
                usage_profile_views.append(value)
                values_profile_views.append(week_day)
                total_profile_views += value
                total_count5 += 1
            if total_profile_views > 0:
                avg5 = total_profile_views / total_count5
                avg_profile_views = round(avg5, 2)

    epsocial=f'{ig}/insights?metric=audience_gender_age,audience_city,audience_country'
    params2 = {
        'access_token': page_access_token,
        'period':'lifetime',
    }
    response2 = requests.get(url.format(version='v17.0', endpoint=epsocial), params=params2)
    socialdata = response2.json()

    if account.followers > 100:
        gender_age = socialdata['data'][0]['values']
        for data in gender_age:
            male = sum([data['value'][key] for key in data['value'] if key.startswith('M.')])
            female = sum([data['value'][key] for key in data['value'] if key.startswith('F.')])

        total = male + female
        calc_male = (male / total) * 100
        calc_female = (female / total) * 100
        values_gender_calc.append(round(calc_male, 2))
        values_gender_calc.append(round(calc_female, 2))
        label_gender.append(_('Male'))
        label_gender.append(_('Female'))
        
        
        range_female = {}
        range_male = {}

        for key, value in socialdata['data'][0]['values'][0]['value'].items():
            gender, range = key.split('.') 
            if gender == 'F':
                if range in range_female:
                    range_female[range] += value
                else:
                    range_female[range] = value
            elif gender == 'M':
                if range in range_male:
                    range_male[range] += value
            else:
               range_male[range] = value

        total_female = sum(range_female.values())
        total_male = sum(range_male.values())

        for range, s in range_female.items():
            percentage = (s / total_female) * 100
            values_gender.append(range)
            usage_female.append(round(percentage, 2))

        for range, s in range_male.items():
            percentage = (s / total_male) * 100
            usage_male.append(round(percentage, 2))

        sorted_data = sorted(socialdata['data'][1]['values'][0]['value'].items(), key=lambda x: x[1], reverse=True)
        
        total = sum(value for city, value in sorted_data)

        percentages = [(city, value / total * 100) for city, value in sorted_data]

        for city, percentage in percentages[:5]:
            label_city.append(city)
            qty_city_values.append(round(percentage, 2))
        
        sorted_country = sorted(socialdata['data'][2]['values'][0]['value'].items(), key=lambda x: x[1], reverse=True)

        total_country = sum(value for code, value in sorted_country)

        per_country = [(code, value / total_country * 100) for code, value in sorted_country]

        for code, percentage in per_country[:5]:
            country=Country.objects.get(code2=code)
            label_country.append(country.name)
            qty_country_values.append(round(percentage, 2))

    if request.method == 'POST':
        action = request.POST.get('action')
        print(action)

        if action == "dateReach":
            new_date=[]
            new_value=[]
            total=0
            count=0
            avg=0
            start_time = request.POST.get('startdate')
            end_time = request.POST.get('endtime')
            epcustom_metrics=f'{ig}/insights?metric=reach'
            custom_params = {
                'access_token': page_access_token,
                'period':'day',
                'since':start_time,
                'until':end_time,
            }
            dataload = requests.get(url.format(version='v17.0', endpoint= epcustom_metrics), params=custom_params)
            getdata = dataload.json()
            items = getdata['data']
            if items:
                for retrieve in getdata['data']:
                    if retrieve['name'] == 'reach':
                        data = retrieve['values']
                        for item in data:
                            value = item['value']
                            end_time = item['end_time']
                            cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                            if lang == "en":
                                week_day = format_date(cleandate, format='MMM d, \'YY', locale=lang)
                            elif lang == "es-ve":
                                week_day = format_date(cleandate, format='MMM d, \'YY', locale="es")
                            new_value.append(value)
                            new_date.append(str(week_day))
                            total += value
                            count += 1
                        if total > 0:
                            avg_clean = total / count
                            avg = round(avg_clean, 2)

                return JsonResponse({
                            'success':'clear data',
                            'label': _('Reach'),
                            'usage': new_value,
                            'dates': new_date,
                            'avg': avg,
                            'total': total,
                            }) 
            else:
                return JsonResponse({'empty':'clear data'})
            
        if action == "dateFollowers":
                new_date=[]
                new_value=[]
                total=0
                count=0
                avg=0
                start_time = request.POST.get('startdate')
                end_time = request.POST.get('endtime')
                epcustom_metrics=f'{ig}/insights?metric=follower_count'
                custom_params = {
                    'access_token': page_access_token,
                    'period':'day',
                    'since':start_time,
                    'until':end_time,
                }
                dataload = requests.get(url.format(version='v17.0', endpoint= epcustom_metrics), params=custom_params)
                getdata = dataload.json()
                items = getdata['data']
                if items:
                    for retrieve in getdata['data']:
                        if retrieve['name'] == 'follower_count':
                            data = retrieve['values']
                            for item in data:
                                value = item['value']
                                end_time = item['end_time']
                                cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                                if lang == "en":
                                    week_day = format_date(cleandate, format='MMM d, \'YY', locale=lang)
                                elif lang == "es-ve":
                                    week_day = format_date(cleandate, format='MMM d, \'YY', locale="es")
                                new_value.append(value)
                                new_date.append(str(week_day))
                                total += value
                                count += 1
                            if total > 0:
                                avg_clean = total / count
                                avg = round(avg_clean, 2)

                    return JsonResponse({
                                'success':'clear data',
                                'label': _('New followers'),
                                'usage': new_value,
                                'dates': new_date,
                                'avg': avg,
                                'total': total,
                                }) 
                else:
                    return JsonResponse({'empty':'clear data'})
        
        if action == "dateLinkClick":
            new_date=[]
            new_value=[]
            total=0
            count=0
            avg=0
            start_time = request.POST.get('startdate')
            end_time = request.POST.get('endtime')
            epcustom_metrics=f'{ig}/insights?metric=website_clicks'
            custom_params = {
                'access_token': page_access_token,
                'period':'day',
                'since':start_time,
                'until':end_time,
            }
            dataload = requests.get(url.format(version='v17.0', endpoint= epcustom_metrics), params=custom_params)
            getdata = dataload.json()
            items = getdata['data']
            if items:
                for retrieve in getdata['data']:
                    if retrieve['name'] == 'website_clicks':
                        data = retrieve['values']
                        for item in data:
                            value = item['value']
                            end_time = item['end_time']
                            cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                            if lang == "en":
                                week_day = format_date(cleandate, format='MMM d, \'YY', locale=lang)
                            elif lang == "es-ve":
                                week_day = format_date(cleandate, format='MMM d, \'YY', locale="es")
                            new_value.append(value)
                            new_date.append(str(week_day))
                            total += value
                            count += 1
                        if total > 0:
                            avg_clean = total / count
                            avg = round(avg_clean, 2)

                return JsonResponse({
                            'success':'clear data',
                            'label': _('Link Click'),
                            'usage': new_value,
                            'dates': new_date,
                            'avg': avg,
                            'total': total,
                            }) 
            else:
                return JsonResponse({'empty':'clear data'})
        
        if action == "dateViews":
            new_date=[]
            new_value=[]
            total=0
            count=0
            avg=0
            start_time = request.POST.get('startdate')
            end_time = request.POST.get('endtime')
            epcustom_metrics=f'{ig}/insights?metric=profile_views'
            custom_params = {
                'access_token': page_access_token,
                'period':'day',
                'since':start_time,
                'until':end_time,
            }
            dataload = requests.get(url.format(version='v17.0', endpoint= epcustom_metrics), params=custom_params)
            getdata = dataload.json()
            items = getdata['data']
            if items:
                for retrieve in getdata['data']:
                    if retrieve['name'] == 'profile_views':
                        data = retrieve['values']
                        for item in data:
                            value = item['value']
                            end_time = item['end_time']
                            cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                            if lang == "en":
                                week_day = format_date(cleandate, format='MMM d, \'YY', locale=lang)
                            elif lang == "es-ve":
                                week_day = format_date(cleandate, format='MMM d, \'YY', locale="es")
                            new_value.append(value)
                            new_date.append(str(week_day))
                            total += value
                            count += 1
                        if total > 0:
                            avg_clean = total / count
                            avg = round(avg_clean, 2)

                return JsonResponse({
                            'success':'clear data',
                            'label': _('Profile visits'),
                            'usage': new_value,
                            'dates': new_date,
                            'avg': avg,
                            'total': total,
                            }) 
            else:
                return JsonResponse({'empty':'clear data'})
            
        if action == "datePrint":
            new_date=[]
            new_value=[]
            total=0
            count=0
            avg=0
            start_time = request.POST.get('startdate')
            end_time = request.POST.get('endtime')
            epcustom_metrics=f'{ig}/insights?metric=impressions'
            custom_params = {
                'access_token': page_access_token,
                'period':'day',
                'since':start_time,
                'until':end_time,
            }
            dataload = requests.get(url.format(version='v17.0', endpoint= epcustom_metrics), params=custom_params)
            getdata = dataload.json()
            items = getdata['data']
            if items:
                for retrieve in getdata['data']:
                    if retrieve['name'] == 'impressions':
                        data = retrieve['values']
                        for item in data:
                            value = item['value']
                            end_time = item['end_time']
                            cleandate = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                            if lang == "en":
                                week_day = format_date(cleandate, format='MMM d, \'YY', locale=lang)
                            elif lang == "es-ve":
                                week_day = format_date(cleandate, format='MMM d, \'YY', locale="es")
                            new_value.append(value)
                            new_date.append(str(week_day))
                            total += value
                            count += 1
                        if total > 0:
                            avg_clean = total / count
                            avg = round(avg_clean, 2)

                return JsonResponse({
                            'success':'clear data',
                            'label': _('Impressions (Content Views)'),
                            'usage': new_value,
                            'dates': new_date,
                            'avg': avg,
                            'total': total,
                            }) 
            else:
                return JsonResponse({'empty':'clear data'})
        
        if action == "sendgrid-form":
            site_cookie=SiteData(request)
            form = SendGridForm(request.POST)
            if form.is_valid():
                html_content = render_to_string('stela_control/emails-template/marketing/content-planner-email.html', {
                    'client':form.cleaned_data['client'],
                    'report':form.cleaned_data['message'],
                    'id_page':id,
                    'lang': lang,
                    'id_instagram':ig,
                    'company': site_cookie.company_public()
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            form.cleaned_data['subject'],
                            text_content,
                            settings.STELA_EMAIL,
                            [form.cleaned_data['email']]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return JsonResponse({'success':_('Your content grid was sent successfully')})
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})

        if action == "loadContentMetric": 
            feed=IGPost.objects.filter(parent=account, publish_status="PUBLISHED", created__range=(start_time, timezone.localtime(timezone.now()))).order_by('-created')
            for obj in feed:
                if obj.mediatype == "POST":
                    post=IGPostMetric.objects.filter(post=obj)
                    epfeed_metric=f'{obj.feed_id}/insights?metric=engagement,impressions,reach,saved,video_views'
                    post_params = {
                        'access_token': page_access_token,
                    }
                    response = requests.get(url.format(version='v17.0', endpoint=epfeed_metric), params=post_params)
                    getdata = response.json()
                    try:

                        for data in getdata['data']:
                            if data['name'] == "engagement":
                                engagement=data['values'][0]['value']
                                if post.exists():
                                    post.update(engagement=engagement)
                                else:
                                    IGPostMetric.objects.create(
                                        post=obj,
                                        engagement=engagement
                                    )
                            elif data['name'] == "impressions":
                                impressions=data['values'][0]['value']
                                if post.exists():
                                    post.update(impressions=impressions)
                                else:
                                    IGPostMetric.objects.create(
                                        post=obj,
                                        impressions=impressions
                                    )
                            elif data['name'] == "reach":
                                reach=data['values'][0]['value']
                                if post.exists():
                                    post.update(reach=reach)
                                else:
                                    IGPostMetric.objects.create(
                                        post=obj,
                                        reach=reach    
                                    )
                            elif data['name'] == "saved":
                                saved=data['values'][0]['value']
                                if post.exists():
                                    post.update(saved=saved)
                                else:
                                    IGPostMetric.objects.create(
                                        post=obj,
                                        saved=saved
                                    )
                            elif data['name'] == "video_views":
                                video_views=data['values'][0]['value']
                                if post.exists():
                                    post.update(video_views=video_views)
                                else:
                                    IGPostMetric.objects.create(
                                        post=obj,
                                        video_views=video_views
                                    )
                        post_max_reach=IGPostMetric.objects.filter(post=obj).order_by('reach').first()
                        post_max_engagement=IGPostMetric.objects.filter(post=obj).order_by('engagement').first()
                    except:
                        print(getdata['error']['message'])

                elif obj.mediatype == "REELS":
                    post=IGReelMetric.objects.filter(post=obj)
                    epfeed_metric=f'{obj.feed_id}/insights?metric=comments,likes,plays,reach,saved,shares,total_interactions'
                    post_params = {
                        'access_token': page_access_token,
                    }
                    response = requests.get(url.format(version='v17.0', endpoint=epfeed_metric), params=post_params)
                    getdata = response.json()
                    try:
                        for data in getdata['data']:
                            if data['name'] == "comments":
                                comments=data['values'][0]['value']
                                if post.exists():
                                    post.update(comments=comments)
                                else:
                                    IGReelMetric.objects.create(
                                        post=obj,
                                        comments=comments
                                    )
                            elif data['name'] == "likes":
                                likes=data['values'][0]['value']
                                if post.exists():
                                    post.update(likes=likes)
                                else:
                                    IGReelMetric.objects.create(
                                        post=obj,
                                        likes=likes
                                    )
                            elif data['name'] == "reach":
                                reach=data['values'][0]['value']
                                if post.exists():
                                    post.update(reach=reach)
                                else:
                                    IGReelMetric.objects.create(
                                        post=obj,
                                        reach=reach    
                                    )
                            elif data['name'] == "saved":
                                saved=data['values'][0]['value']
                                if post.exists():
                                    post.update(saved=saved)
                                else:
                                    IGReelMetric.objects.create(
                                        post=obj,
                                        saved=saved
                                    )
                            elif data['name'] == "plays":
                                plays=data['values'][0]['value']
                                if post.exists():
                                    post.update(plays=plays)
                                else:
                                    IGReelMetric.objects.create(
                                        post=obj,
                                        plays=plays
                                    )
                            elif data['name'] == "shares":
                                shares=data['values'][0]['value']
                                if post.exists():
                                    post.update(shares=shares)
                                else:
                                    IGReelMetric.objects.create(
                                        post=obj,
                                        shares=shares
                                    )
                            elif data['name'] == "total_interactions":
                                total_interactions=data['values'][0]['value']
                                if post.exists():
                                    post.update(total_interactions=total_interactions)
                                else:
                                    IGReelMetric.objects.create(
                                        post=obj,
                                        total_interactions=total_interactions
                                    )
                        reel_max_reach=IGReelMetric.objects.filter(post=obj).order_by('reach').first()
                        reel_max_engagement=IGReelMetric.objects.filter(post=obj).order_by('likes').first()
                    except:
                        print(getdata['error']['message'])

                elif obj.mediatype == "CAROUSEL":
                    post=IGCarouselMetric.objects.filter(post=obj)
                    epfeed_metric=f'{obj.feed_id}/insights?metric=carousel_album_engagement,carousel_album_impressions,carousel_album_reach,carousel_album_saved,carousel_album_video_views'
                    post_params = {
                        'access_token': page_access_token,
                    }
                    response = requests.get(url.format(version='v17.0', endpoint=epfeed_metric), params=post_params)
                    getdata = response.json()
                    try:
                        for data in getdata['data']:
                            if data['name'] == "carousel_album_engagement":
                                carousel_album_engagement=data['values'][0]['value']
                                if post.exists():
                                    post.update(album_engagement=carousel_album_engagement)
                                else:
                                    IGCarouselMetric.objects.create(
                                        post=obj,
                                        album_engagement=carousel_album_engagement
                                    )
                            elif data['name'] == "carousel_album_impressions":
                                carousel_album_impressions=data['values'][0]['value']
                                if post.exists():
                                    post.update(album_impressions=carousel_album_impressions)
                                else:
                                    IGCarouselMetric.objects.create(
                                        post=obj,
                                        album_impressions=carousel_album_impressions
                                    )
                            elif data['name'] == "carousel_album_reach":
                                carousel_album_reach=data['values'][0]['value']
                                if post.exists():
                                    post.update(album_reach=carousel_album_reach)
                                else:
                                    IGCarouselMetric.objects.create(
                                        post=obj,
                                        album_reach=carousel_album_reach    
                                    )
                            elif data['name'] == "saved":
                                saved=data['values'][0]['value']
                                if post.exists():
                                    post.update(album_saved=saved)
                                else:
                                    IGCarouselMetric.objects.create(
                                        post=obj,
                                        album_saved=saved
                                    )
                            elif data['name'] == "video_views":
                                video_views=data['values'][0]['value']
                                if post.exists():
                                    post.update(album_video_views=video_views)
                                else:
                                    IGCarouselMetric.objects.create(
                                        post=obj,
                                        album_video_views=video_views
                                    )
                        carousel_max_reach=IGCarouselMetric.objects.filter(post=obj).order_by('album_reach').first()
                        carousel_max_engagement=IGCarouselMetric.objects.filter(post=obj).order_by('album_engagement').first()
                    except:
                        print(getdata['error']['message'])

                elif obj.mediatype == "STORIES":
                    post=IGStoriesMetric.objects.filter(post=obj)
                    epfeed_metric=f'{obj.feed_id}/insights?metric=exits,impressions,reach,replies,taps_forward,taps_back'
                    post_params = {
                        'access_token': page_access_token,
                    }
                    response = requests.get(url.format(version='v17.0', endpoint=epfeed_metric), params=post_params)
                    getdata = response.json()
                    try:
                        for data in getdata['data']:
                            if data['name'] == "exits":
                                exits=data['values'][0]['value']
                                if post.exists():
                                    post.update(exits=exits)
                                else:
                                    IGStoriesMetric.objects.create(
                                        post=obj,
                                        exits=exits
                                    )
                            elif data['name'] == "impressions":
                                impressions=data['values'][0]['value']
                                if post.exists():
                                    post.update(impressions=impressions)
                                else:
                                    IGStoriesMetric.objects.create(
                                        post=obj,
                                        impressions=impressions
                                    )
                            elif data['name'] == "replies":
                                replies=data['values'][0]['value']
                                if post.exists():
                                    post.update(replies=replies)
                                else:
                                    IGStoriesMetric.objects.create(
                                        post=obj,
                                        replies=replies    
                                    )
                            elif data['name'] == "taps_forward":
                                taps_forward=data['values'][0]['value']
                                if post.exists():
                                    post.update(taps_forward=taps_forward)
                                else:
                                    IGStoriesMetric.objects.create(
                                        post=obj,
                                        taps_forward=taps_forward
                                    )
                            elif data['name'] == "taps_back":
                                taps_back=data['values'][0]['value']
                                if post.exists():
                                    post.update(taps_back=taps_back)
                                else:
                                    IGStoriesMetric.objects.create(
                                        post=obj,
                                        taps_back=taps_back
                                    )
                    except:
                        print(getdata['error']['message'])
                
                else:
                    call = "No Content"

            if not feed:
                call = "No Content"

            try:
                if post_max_reach.reach > carousel_max_reach.album_reach and post_max_reach.reach > reel_max_reach.reach:
                    best_performance = post_max_reach

                elif carousel_max_reach.album_reach > post_max_reach.reach and carousel_max_reach.album_reach > reel_max_reach.reach:
                    best_performance = carousel_max_reach

                else:
                    best_performance = reel_max_reach

            except:
                try:
                    if post_max_reach:
                        best_performance = post_max_reach
                    
                    elif carousel_max_reach:
                        best_performance = carousel_max_reach
                    
                    elif reel_max_reach:
                        best_performance = reel_max_reach
                except:
                    best_performance = None
                    best_engagement = None
            try:
                if post_max_engagement.engagement > carousel_max_engagement.album_engagement and post_max_engagement.engagement > reel_max_engagement.likes:
                    best_engagement = post_max_engagement

                elif carousel_max_engagement.album_engagement > post_max_engagement.engagement and carousel_max_engagement.album_engagement > reel_max_engagement.likes:
                    best_engagement = carousel_max_engagement

                else:
                    best_engagement = reel_max_engagement
            except:
                try:
                    if post_max_engagement:
                        best_engagement = post_max_reach
                    
                    elif carousel_max_engagement:
                        best_engagement = carousel_max_engagement
                    
                    elif reel_max_engagement:
                        best_engagement = reel_max_engagement
                except:
                    best_performance = None
                    best_engagement = None
                    
            render_content = render_to_string('stela_control/load-data/meta/ig-analythics/content-render.html', {
                            'feed': feed,
                            'performance': best_performance,
                            'engagement': best_engagement,
                            'call': call
                })

            response = JsonResponse({'success': render_content})
            return response
        
        if action == "dateReels":
            start_time = request.POST.get('startdate')
            end_time = request.POST.get('endtime')
            feed=IGPost.objects.filter(parent=account, publish_status="PUBLISHED", created__range=(start_time, end_time)).order_by('-created')
            if feed.exists():
                for obj in feed:
                    if obj.mediatype == "REELS":
                        post=IGReelMetric.objects.filter(post=obj)
                        epfeed_metric=f'{obj.feed_id}/insights?metric=comments,likes,plays,reach,saved,shares,total_interactions'
                        post_params = {
                            'access_token': page_access_token,
                        }
                        response = requests.get(url.format(version='v17.0', endpoint=epfeed_metric), params=post_params)
                        getdata = response.json()
                        try:
                            for data in getdata['data']:
                                if data['name'] == "comments":
                                    comments=data['values'][0]['value']
                                    if post.exists():
                                        post.update(comments=comments)
                                    else:
                                        IGReelMetric.objects.create(
                                            post=obj,
                                            comments=comments
                                        )
                                elif data['name'] == "likes":
                                    likes=data['values'][0]['value']
                                    if post.exists():
                                        post.update(likes=likes)
                                    else:
                                        IGReelMetric.objects.create(
                                            post=obj,
                                            likes=likes
                                        )
                                elif data['name'] == "reach":
                                    reach=data['values'][0]['value']
                                    if post.exists():
                                        post.update(reach=reach)
                                    else:
                                        IGReelMetric.objects.create(
                                            post=obj,
                                            reach=reach    
                                        )
                                elif data['name'] == "saved":
                                    saved=data['values'][0]['value']
                                    if post.exists():
                                        post.update(saved=saved)
                                    else:
                                        IGReelMetric.objects.create(
                                            post=obj,
                                            saved=saved
                                        )
                                elif data['name'] == "plays":
                                    plays=data['values'][0]['value']
                                    if post.exists():
                                        post.update(plays=plays)
                                    else:
                                        IGReelMetric.objects.create(
                                            post=obj,
                                            plays=plays
                                        )
                                elif data['name'] == "shares":
                                    shares=data['values'][0]['value']
                                    if post.exists():
                                        post.update(shares=shares)
                                    else:
                                        IGReelMetric.objects.create(
                                            post=obj,
                                            shares=shares
                                        )
                                elif data['name'] == "total_interactions":
                                    total_interactions=data['values'][0]['value']
                                    if post.exists():
                                        post.update(total_interactions=total_interactions)
                                    else:
                                        IGReelMetric.objects.create(
                                            post=obj,
                                            total_interactions=total_interactions
                                        )
                            render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-reels.html', {
                                    'update_feed': feed,
                                })
                            return JsonResponse({'response': render_content})
                        except:
                            render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-reels.html', {
                                'update_feed': feed,
                            })
                            return JsonResponse({'response': render_content})
                    else:
                        render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-reels.html', {
                                'update_feed': feed,
                            })
                        return JsonResponse({'response': render_content})
            else:
                render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-reels.html', {
                    'update_feed': feed,
                    })
                return JsonResponse({'response': render_content})

        if action == "datePosts":
            start_time = request.POST.get('startdate')
            end_time = request.POST.get('endtime')
            feed=IGPost.objects.filter(parent=account, publish_status="PUBLISHED", created__range=(start_time, end_time)).order_by('-created')
            if feed.exists():
                for obj in feed:
                    if obj.mediatype == "POST":
                        post=IGPostMetric.objects.filter(post=obj)
                        epfeed_metric=f'{obj.feed_id}/insights?metric=engagement,impressions,reach,saved,video_views'
                        post_params = {
                            'access_token': page_access_token,
                        }
                        response = requests.get(url.format(version='v17.0', endpoint=epfeed_metric), params=post_params)
                        getdata = response.json()
                        try:
                            for data in getdata['data']:
                                if data['name'] == "engagement":
                                    engagement=data['values'][0]['value']
                                    if post.exists():
                                        post.update(engagement=engagement)
                                    else:
                                        IGPostMetric.objects.create(
                                            post=obj,
                                            engagement=engagement
                                        )
                                elif data['name'] == "impressions":
                                    impressions=data['values'][0]['value']
                                    if post.exists():
                                        post.update(impressions=impressions)
                                    else:
                                        IGPostMetric.objects.create(
                                            post=obj,
                                            impressions=impressions
                                        )
                                elif data['name'] == "reach":
                                    reach=data['values'][0]['value']
                                    if post.exists():
                                        post.update(reach=reach)
                                    else:
                                        IGPostMetric.objects.create(
                                            post=obj,
                                            reach=reach    
                                        )
                                elif data['name'] == "saved":
                                    saved=data['values'][0]['value']
                                    if post.exists():
                                        post.update(saved=saved)
                                    else:
                                        IGPostMetric.objects.create(
                                            post=obj,
                                            saved=saved
                                        )
                                elif data['name'] == "video_views":
                                    video_views=data['values'][0]['value']
                                    if post.exists():
                                        post.update(video_views=video_views)
                                    else:
                                        IGPostMetric.objects.create(
                                            post=obj,
                                            video_views=video_views
                                        )
                            render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-post.html', {
                                'update_feed': feed,
                            })
                            return JsonResponse({'response': render_content})
                        except:
                            render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-post.html', {
                                'update_feed': feed,
                            })
                            return JsonResponse({'response': render_content})
                    else:
                        render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-post.html', {
                                'update_feed': feed,
                            })
                        return JsonResponse({'response': render_content})
            else:
                render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-post.html', {
                    'update_feed': feed,
                    })
                return JsonResponse({'response': render_content})
        
        if action == "dateCarousels":
            start_time = request.POST.get('startdate')
            end_time = request.POST.get('endtime')
            feed=IGPost.objects.filter(parent=account, publish_status="PUBLISHED", created__range=(start_time, end_time)).order_by('-created')
            if feed.exists():
                for obj in feed:
                    if obj.mediatype == "CAROUSEL":
                        post=IGCarouselMetric.objects.filter(post=obj)
                        epfeed_metric=f'{obj.feed_id}/insights?metric=carousel_album_engagement,carousel_album_impressions,carousel_album_reach,carousel_album_saved,carousel_album_video_views'
                        post_params = {
                            'access_token': page_access_token,
                        }
                        response = requests.get(url.format(version='v17.0', endpoint=epfeed_metric), params=post_params)
                        getdata = response.json()
                        try:
                            for data in getdata['data']:
                                if data['name'] == "carousel_album_engagement":
                                    carousel_album_engagement=data['values'][0]['value']
                                    if post.exists():
                                        post.update(album_engagement=carousel_album_engagement)
                                    else:
                                        IGCarouselMetric.objects.create(
                                            post=obj,
                                            album_engagement=carousel_album_engagement
                                        )
                                elif data['name'] == "carousel_album_impressions":
                                    carousel_album_impressions=data['values'][0]['value']
                                    if post.exists():
                                        post.update(album_impressions=carousel_album_impressions)
                                    else:
                                        IGCarouselMetric.objects.create(
                                            post=obj,
                                            album_impressions=carousel_album_impressions
                                        )
                                elif data['name'] == "carousel_album_reach":
                                    carousel_album_reach=data['values'][0]['value']
                                    if post.exists():
                                        post.update(album_reach=carousel_album_reach)
                                    else:
                                        IGCarouselMetric.objects.create(
                                            post=obj,
                                            album_reach=carousel_album_reach    
                                        )
                                elif data['name'] == "saved":
                                    saved=data['values'][0]['value']
                                    if post.exists():
                                        post.update(album_saved=saved)
                                    else:
                                        IGCarouselMetric.objects.create(
                                            post=obj,
                                            album_saved=saved
                                        )
                                elif data['name'] == "video_views":
                                    video_views=data['values'][0]['value']
                                    if post.exists():
                                        post.update(album_video_views=video_views)
                                    else:
                                        IGCarouselMetric.objects.create(
                                            post=obj,
                                            album_video_views=video_views
                                        )
                            render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-carousels.html', {
                                    'update_feed': feed,
                                })
                            return JsonResponse({'response': render_content})
                        except:
                            render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-carousels.html', {
                                'update_feed': feed,
                            })
                            return JsonResponse({'response': render_content})
                    else:
                        render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-carousels.html', {
                                'update_feed': feed,
                            })
                        return JsonResponse({'response': render_content})
            else:
                render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-carousels.html', {
                    'update_feed': feed,
                    })
                return JsonResponse({'response': render_content})

        if action == "dateStories":
            start_time = request.POST.get('startdate')
            end_time = request.POST.get('endtime')
            feed=IGPost.objects.filter(parent=account, publish_status="PUBLISHED", created__range=(start_time, end_time)).order_by('-created')
            if feed.exists():
                for obj in feed:
                    if obj.mediatype == "STORIES":
                        post=IGStoriesMetric.objects.filter(post=obj)
                        epfeed_metric=f'{obj.feed_id}/insights?metric=exits,impressions,reach,replies,taps_forward,taps_back'
                        post_params = {
                            'access_token': page_access_token,
                        }
                        response = requests.get(url.format(version='v17.0', endpoint=epfeed_metric), params=post_params)
                        getdata = response.json()
                        try:
                            for data in getdata['data']:
                                if data['name'] == "exits":
                                    exits=data['values'][0]['value']
                                    if post.exists():
                                        post.update(exits=exits)
                                    else:
                                        IGStoriesMetric.objects.create(
                                            post=obj,
                                            exits=exits
                                        )
                                elif data['name'] == "impressions":
                                    impressions=data['values'][0]['value']
                                    if post.exists():
                                        post.update(impressions=impressions)
                                    else:
                                        IGStoriesMetric.objects.create(
                                            post=obj,
                                            impressions=impressions
                                        )
                                elif data['name'] == "replies":
                                    replies=data['values'][0]['value']
                                    if post.exists():
                                        post.update(replies=replies)
                                    else:
                                        IGStoriesMetric.objects.create(
                                            post=obj,
                                            replies=replies    
                                        )
                                elif data['name'] == "taps_forward":
                                    taps_forward=data['values'][0]['value']
                                    if post.exists():
                                        post.update(taps_forward=taps_forward)
                                    else:
                                        IGStoriesMetric.objects.create(
                                            post=obj,
                                            taps_forward=taps_forward
                                        )
                                elif data['name'] == "taps_back":
                                    taps_back=data['values'][0]['value']
                                    if post.exists():
                                        post.update(taps_back=taps_back)
                                    else:
                                        IGStoriesMetric.objects.create(
                                            post=obj,
                                            taps_back=taps_back
                                        )
                            render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-stories.html', {
                                    'update_feed': feed,
                                })
                            return JsonResponse({'response': render_content})
                        except:
                            render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-stories.html', {
                                'update_feed': feed,
                            })
                            return JsonResponse({'response': render_content})
                    else:
                        render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-stories.html', {
                                'update_feed': feed,
                            })
                        return JsonResponse({'response': render_content})
            else:
                render_content = render_to_string('stela_control/load-data/meta/ig-analythics/table-metric-stories.html', {
                    'update_feed': feed,
                    })
                return JsonResponse({'response': render_content})

    context = {
        'usage_followers': usage_followers,
        'values_followers': values_followers,
        'followers_count': total_followers,
        'usage_reach': usage_reach,
        'values_reach': values_reach,
        'reach_count': total_reach,
        'usage_linkclicks': usage_linkclicks,
        'values_linkclicks': values_linkclicks,
        'linkclicks_count': total_linkclicks,
        'usage_impressions': usage_impressions,
        'values_impressions': values_impressions,
        'impressions_count': total_impressions,
        'usage_profile_views': usage_profile_views,
        'values_profile_views': values_profile_views,
        'profile_views_count': total_profile_views,
        'usage_female': usage_female,
        'values_gender': values_gender,
        'usage_male': usage_male,
        'values_gender_calc': values_gender_calc,
        'label_gender': label_gender,
        'label_city': label_city,
        'qty_city_values': qty_city_values,
        'label_country': label_country,
        'qty_country_values': qty_country_values,
        'avg_followers': avg_followers,
        'avg_reach': avg_reach,
        'avg_linkclicks': avg_linkclicks,
        'avg_profile_views': avg_profile_views,
        'avg_impressions': avg_impressions,
        'account': account,
        'formgrid': formgrid,
        'page': page,
    }

    response = render(request, 'stela_control/marketing/meta_business/instagram/ig-analyzer/main.html', context)
    response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/' 
    return response

def fbmedia(request):
    if request.method == 'POST':
        postid= request.POST.get('post-id')
        for media in request.FILES.getlist('media'):
            FacebookPostMedia.objects.create(
                post_id=postid,
                media=media
            )
        response_data = {
            'message': 'Media uploaded successfully'
        }
        return JsonResponse(response_data, status=200)
    else:
        response_data = {
        'message': 'Invalid request method'
        }
        return JsonResponse(response_data, status=400)

def igmedia(request):
    if request.method == 'POST':
        postid= request.POST.get('post-id')
        for media in request.FILES.getlist('media'):
            IGMediaContent.objects.create(
                post_id=postid,
                media=media
            )
        response_data = {
            'message': 'Media uploaded successfully'
        }
        return JsonResponse(response_data, status=200)
    else:
        response_data = {
        'message': 'Invalid request method'
        }
        return JsonResponse(response_data, status=400)

def igCounter(request, id):
    ig_account=InstagramAccount.objects.get(asset_id=id)
    feed=IGPost.objects.filter(parent=ig_account).count()
    if feed >= 4:
        return JsonResponse({'counter':feed})
    else:
        return JsonResponse({'empty':'return something'})
    
def igCheckPost(request, id):
    call = request.POST.get('action')
    url='https://graph.facebook.com/{version}/{endpoint}'
    ig_account=InstagramAccount.objects.get(asset_id=id)
    epigpublish=f'{ig_account.asset_id}/media_publish?'

    if call == "checkIGPost": 
            feeds=IGPost.objects.filter(parent=ig_account)
            for feed in feeds:
                epcheckpost=f'{feed.container_id}?'
                if feed.publish_status == "IN_PROGRESS":
                    params = {
                        'fields':'status_code',
                        'access_token': feed.token,
                    }
                    upstatus = requests.get(url.format(version='v17.0', endpoint=epcheckpost), params=params)
                    updata = upstatus.json()
                    IGPost.objects.filter(pk=feed.pk).update(publish_status=updata['status_code'])
                    return JsonResponse({'inProgress': _('Instagram upload successfull')})

                elif feed.publish_status == "FINISHED":
                    publish_params = {
                        'creation_id': feed.container_id,
                        'access_token': feed.token,
                    }
                    publish = requests.post(url.format(version='v17.0', endpoint=epigpublish), params=publish_params)
                    data = publish.json()
                    params = {
                        'fields':'status_code',
                        'access_token': feed.token,
                    }
                    upstatus = requests.get(url.format(version='v17.0', endpoint=epcheckpost), params=params)
                    updata = upstatus.json()  
                    print(updata) 
                    IGPost.objects.filter(pk=feed.pk).update(status="publish", publish_status=updata['status_code'], feed_id=data['id'])
                    return JsonResponse({'success': _('Instagram upload successfull')})
            return JsonResponse({'noPendingPost': _('Instagram upload successfull')})

def grid(request,id,ig):
    lang=request.LANGUAGE_CODE
    country_id = str(lang).split('-')
    get_timezone = country_timezones(country_id[1])[0]
    page=FacebookPage.objects.get(asset_id=id)
    ig_account=InstagramAccount.objects.get(asset_id=ig)
    schedule = []
    last_month = timezone.now() - timedelta(days=32)
    month_ahead = timezone.now() + timedelta(days=32)
    feed = IGPost.objects.filter(parent=ig_account, schedule__gte=last_month, schedule__lt=month_ahead).order_by('-schedule')[:10]
    calendar = IGPost.objects.filter(parent=ig_account, schedule__gte=last_month, schedule__lt=month_ahead).order_by('-schedule')
    for post in calendar:
        get_media=IGMediaContent.objects.filter(post=post).order_by('id').first()
        if post.status == "publish":
            message_formatted = caption_optimizer(post.caption)
            string=message_formatted.split()
            title=" ".join(string[:4])
            titlebox=" ".join(string[:10])
            if get_media.mp4():
                if get_media.get_cover():
                    planning_data = {
                        'id': post.pk,
                        'title': title, 
                        'start': post.schedule.isoformat(), 
                        'extendedProps': {
                            'fullTitle': titlebox,
                            'mediaUrl': get_media.get_cover(),
                            'mediatype': post.mediatype,
                            'cover': 'true'
                        },
                        'allDay': False, 
                    }
                else:
                    planning_data = {
                        'id': post.pk,
                        'title': title, 
                        'start': post.schedule.isoformat(), 
                        'extendedProps': {
                            'fullTitle': titlebox,
                            'mediaUrl': get_media.get_url(),
                            'mediatype': post.mediatype,
                            'cover': 'false',
                        },
                        'allDay': False, 
                    }
            else:
                planning_data = {
                    'id': post.pk,
                    'title':title, 
                    'start': post.schedule.isoformat(), 
                    'extendedProps': {
                        'fullTitle': titlebox,
                        'mediaUrl': get_media.get_url(),
                        'mediatype': post.mediatype,
                    },
                    'allDay': False, 
                }
        else:
            message_formatted = caption_optimizer(post.caption)
            string=message_formatted.split()
            title=" ".join(string[:4])
            titlebox=" ".join(string[:10])
            if get_media.mp4():
                if get_media.get_cover():
                    planning_data = {
                        'id': post.pk,
                        'title': title, 
                        'start': post.schedule.isoformat(), 
                        'extendedProps': {
                            'fullTitle': titlebox,
                            'mediaUrl': get_media.get_cover(),
                            'mediatype': post.mediatype,
                            'cover': 'true'
                        },
                        'allDay': False, 
                    }
                else:
                    planning_data = {
                        'id': post.pk,
                        'title': title, 
                        'start': post.schedule.isoformat(), 
                        'extendedProps': {
                            'fullTitle': titlebox,
                            'mediaUrl': get_media.get_url(),
                            'mediatype': post.mediatype,
                            'cover': 'false',
                        },
                        'allDay': False, 
                    }
            else:
                planning_data = {
                    'id': post.pk,
                    'title': title, 
                    'start': post.schedule.isoformat(), 
                    'extendedProps': {
                        'fullTitle': titlebox,
                        'mediaUrl': get_media.get_url(),
                        'mediatype': post.mediatype,
                    },
                    'allDay': False, 
                }
        schedule.append(planning_data)
    calendar_data = json.dumps(schedule)

    if request.method == 'POST':
        action = request.POST.get('form-id')
        call = request.POST.get('action')
        print(action)
        print(call)

        if call == "loadPages":
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            new_posts = IGPost.objects.filter(parent=ig_account, schedule__gte=last_month, schedule__lt=month_ahead).order_by('-schedule')[starts:ends]
            print(new_posts)
            new_pages = render_to_string('stela_control/load-data/meta/ig-new-page-grid.html', {
                    'newposts': new_posts,
                    'instagram': ig_account,
                    'usertz': get_timezone,
                    })
            return JsonResponse({'response': new_pages})
    
    context = {
        'calendar_data': calendar_data,
        'page': page,
        'feed': feed,
        'instagram': ig_account,
        'usertz': get_timezone,
    }

    response = render(request, 'stela_control/marketing/meta_business/instagram/grid/index.html', context)
    response['X-Frame-Options'] = 'ALLOW-FROM https://www.facebook.com/' 
    return response

def IcreativeActions(request, id, ig):
    lang=request.LANGUAGE_CODE
    ig_account=InstagramAccount.objects.get(asset_id=ig)

    if request.method == 'POST':
        action = request.POST.get('form-id')
        call = request.POST.get('action')
        print(action)
        print(call)

        if action == "sendgrid-form":
            site_cookie=SiteData(request)
            form = SendGridForm(request.POST)
            if form.is_valid():
                html_content = render_to_string('stela_control/emails-template/marketing/content-planner-email.html', {
                    'client':form.cleaned_data['client'],
                    'report':form.cleaned_data['message'],
                    'id_page':id,
                    'lang': lang,
                    'id_instagram':ig,
                    'date': timezone.now(),
                    'company': site_cookie.company_public()
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            form.cleaned_data['subject'],
                            text_content,
                            settings.STELA_EMAIL,
                            [form.cleaned_data['email']]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return JsonResponse({'success':_('Your content grid was sent successfully')})
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})
        
        if action == "sendmetric-form":
            site_cookie=SiteData(request)
            form = SendGridForm(request.POST)
            if form.is_valid():
                html_content = render_to_string('stela_control/emails-template/marketing/content-planner-email.html', {
                    'client':form.cleaned_data['client'],
                    'report':form.cleaned_data['message'],
                    'id_page':id,
                    'lang': lang,
                    'id_instagram':ig,
                    'company': site_cookie.company_public()
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            form.cleaned_data['subject'],
                            text_content,
                            settings.STELA_EMAIL,
                            [form.cleaned_data['email']]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return JsonResponse({'success':_('Your IG Analyzer was sent successfully')})
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})
        
        if call == "loadPages":
            get_timezone = request.POST.get('zone') 
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            new_posts = IGPost.objects.filter(parent=ig_account).order_by('-schedule')[starts:ends]
            new_pages = render_to_string('stela_control/load-data/meta/ig-new-pages.html', {
                    'newposts': new_posts,
                    'instagram': ig_account,
                    'usertz': get_timezone,
                    })
            return JsonResponse({'response': new_pages})

#googlePlattforms
@login_required
def googleAuth(request):
    from django.http import JsonResponse
    from django.utils import timezone
    from datetime import timedelta
    from requests_oauthlib import OAuth2Session
    from oauthlib.oauth2 import WebApplicationClient
    from .models import YouTubeToken

    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_SECRET
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    scope = ['https://www.googleapis.com/auth/youtube.force-ssl']

    client = WebApplicationClient(client_id)
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope, client=client)
    
    code = request.GET.get('code')
    
    if code:
        try:
            token = oauth.fetch_token(
                'https://oauth2.googleapis.com/token',
                code=code,
                client_secret=client_secret)
            
            expires_at = timezone.now() + timedelta(seconds=token.get('expires_in'))
            
            youtube_token, created = YouTubeToken.objects.update_or_create(
                user=request.user,
                defaults={
                    'access_token': token['access_token'],
                    'refresh_token': token.get('refresh_token'),
                    'token_type': token['token_type'],
                    'expires_in': expires_at,
                    'scope': ",".join(token['scope'])
                }
            )
            return JsonResponse({'success': True, 'message': 'Authentication successful.'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    else:
        return JsonResponse({'success': False, 'message': 'No code provided.'})

def get_youtube_playlist_videos(playlist_id):
    api_key = settings.GCP_API_KEY
    videos = []
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    try:
        api_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=20  
        )
        response = api_request.execute()
        
        for item in response.get('items', []):
            video = {
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'video_id': item['snippet']['resourceId']['videoId']
            }
            videos.append(video)
    except HttpError as e:
        print(f'An error occurred: {e.resp.status}, {e.content}')
    
    return videos

#amazonAffiliate
def amazonSearchEngine():
    from amazon_paapi import AmazonApi
    results=[]
    access_key = settings.AWS_ACCESS_KEY_ID
    secret_key = settings.AWS_SECRET_ACCESS_KEY
    partner_tag = settings.AMAZON_PARTNER_TAG
    region = "US"
    amazon = AmazonApi(access_key, secret_key, partner_tag, region)
    search_result = amazon.search_items(keywords='nintendo')

    for item in search_result.items:

        results.append(item.item_info.product_info)

    return results

#operationsModule
def orders(request):
    orders = Order.objects.all().order_by('-id')
    
    if request.method=='POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id)
        print(action)

        if action == 'deleteOrder':
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Order.objects.get(pk=id)
                obj.delete()
            response = JsonResponse({'success': 'return something'})
            return response

    context = {
        'orders':orders,
    }

    return render(request, 'stela_control/orders/list_view.html', context)

def orders_update(request, id):
    order = Order.objects.get(id=id)
    try:
        path_control = PathControl.objects.get(order_id=order.id)
    except PathControl.DoesNotExist:
        path_control = None
    
    context = {
        'order': order,
        'path': path_control,
    }
    return render(request, 'stela_control/orders/order_update.html', context)

def orders_requests(request):
    master_owner=UserBase.objects.get(username="emmerut")
    
    if request.POST.get('action') == 'step1':
        orderid = request.POST.get('orderid')
        cloud_id = request.POST.get('cloudid')
        order = Order.objects.get(pk=orderid)
        customer=Customer.objects.get(pk=order.customer.pk)
        path = PathControl.objects.filter(order_id=orderid)
        items = OrderItems.objects.get(order_id=orderid)

        if path.exists():
            path.update(step="Step 2")

        else:
            PathControl.objects.create(
                order_id=orderid,
                step="Step 2"
            )
        Notifications.objects.create (
            user = order.owner,
            status = "No Read",
            title = _("Cloud Init Complete"),
            description =_("Finished cloud architecture"),
            section = _("Path Project"),
            url = "https://emmerut.com/console/websites" 
        )
        print(cloud_id)
        UserBase.objects.filter(email=customer.email).update(cloud_id=cloud_id, cloud_services=True)
        response = JsonResponse({'success':'return something'})
        return response

    if request.POST.get('action') == 'step2':
        orderid = request.POST.get('orderid')
        order = Order.objects.get(pk=orderid)
        path = PathControl.objects.filter(order_id=orderid).update(step="Step 3")
        items = OrderItems.objects.get(order_id=orderid)
        Notifications.objects.create (
            user = order.owner,
            status = "No Read",
            title = _("Your Zone DNS is ready"),
            description =_("Host Active"),
            section = order.section,
            url = "https://emmerut.com/console/websites" 
        )
        
        response = JsonResponse({'success':'return something'})
        return response
    
    if request.POST.get('action') == 'step3':
        orderid = request.POST.get('orderid')
        order = Order.objects.get(pk=orderid)
        path = PathControl.objects.filter(order_id=orderid).update(step="Step 4")
        items = OrderItems.objects.get(order_id=orderid)
        alert=Notifications.objects.create (
                            user = order.owner,
                            status = "No Read",
                            title =_("Your credentials are set"),
                            description =_("Stela account are created"),
                            section = order.section,
                            url = "https://emmerut.com/console/websites" 
                        )
        
        response = JsonResponse({'success':'return something'})
        return response
    
    if request.POST.get('action') == 'step4':
        orderid = request.POST.get('orderid')
        superuser = request.POST.get('username')
        password = request.POST.get('password')
        url = request.POST.get('access')
        get_control_number=BillingRecipt.objects.filter(is_generated=True, is_budget=False, payment_option="USD",).count()
        control_number = get_control_number + 1
        invoice_number = "DB"+"-"+str(control_number)
        order = Order.objects.get(pk=orderid)
        path = PathControl.objects.filter(order_id=orderid).update (
            superuser=superuser,
            password=password,
            url=url,
            step="Complete"
        )
        subtotal = order.subtotal / 2
        tax=subtotal * Decimal(0.10)
        Order.objects.filter(pk=orderid).update(status="Pending Final Payment")
        items=OrderItems.objects.get(order_id=orderid)
        services=StelaSelection.objects.filter(pk=items.stela_selection.pk)
        alert=Notifications.objects.create (
                            user = order.owner,
                            status = "No Read",
                            title = _("Project Ready"),
                            description =_("Deploy complete"),
                            section = order.section,
                            url = "https://emmerut.com/console/websites" 
                        )

        VirtualCloud.objects.filter(
            owner=order.owner
        ).update(status="Running")
        CloudStorage.objects.filter(
            owner=order.owner
        ).update(status="Running")
        ResquetsCloud.objects.filter(
            owner=order.owner
        ).update(status="Running")
        ZoneDNS.objects.filter(
            owner=order.owner
        ).update(status="Running")
    
        invoice = BillingRecipt.objects.create(
            is_generated=True,
            owner=master_owner,
            customer=order.customer,
            option="Final Stela Websites",
            amount=subtotal,
            tax=tax
        )
        inv_con=InvoiceControl.objects.create(
                order=Order.objects.get(pk=orderid),
                recipt=invoice,
                control_id= invoice_number

            )
        html_content = render_to_string('stela_control/emails-template/orders/stela_credentials.html', {
                'order': order,
                'inv': inv_con, 
            })

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
                    'Your Project is Ready',
                    text_content,
                    settings.STELA_EMAIL,
                    [order.email]
                                    
                )
        email.attach_alternative(html_content, "text/html")
        email.send()

        
        response = JsonResponse({'success':'return something'})
        return response

def reviews(request):
    reviews = Reviews.objects.all()
    
    if request.method == 'POST':
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id)
        print(action)
        
        if action == "data":
            obj_id=request.POST.get('objid')
            obj=Reviews.objects.get(pk=obj_id)
            form=ReviewsForm(instance=obj, prefix="update")
        
            obj_data = render_to_string('stela_control/load-data/form-base.html', {
                            'form': form, 
                            'obj': obj  
                })

            response = JsonResponse({'response': obj_data})
            return response

        if form_id == "Update":
            obj_id=request.POST.get('obj-id')
            obj=Reviews.objects.get(pk=obj_id)
            form=ReviewsForm(request.POST, instance=obj, prefix="update")
            if form.is_valid():
                parent = form.save(commit=False)
                parent.save()
                        
                return redirect('/reviews')
            else:
                print(form.errors)
        
        if action == "deleteObj":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Reviews.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
    context={
        'reviews':reviews
    }

    return render(request, 'stela_control/reviews/reviews.html', context)

#usersModule
@login_required
def users(request):
    localuser = UserBase.objects.filter(is_subscribed=False)
   
    if request.method=='POST':

        action = request.POST.get('action')
        print(action)

        if action == "localuser":
            user_ids = request.POST.getlist('id[]')
            for id in user_ids:
                user = UserBase.objects.get(pk=id)
                user.delete()
                
                if DataEmail.objects.filter(email=user.email).exists():
                    user_newsletter = DataEmail.objects.get(email=user.email)
                    user_newsletter.delete()
                    
            response = JsonResponse({'success': 'return something'})
            return response
    
    context={
        'users':localuser,
    }

    return render(request, 'stela_control/users/users_list.html', context)

@login_required
def update_users(request, id):
    user = UserBase.objects.get(id=id)
    form = UserForm(instance=user)
    orders = Order.objects.filter(owner=user, section="Stela Websites")
    
    try:
        stela=Order.objects.filter(owner=user, section="Stela Websites").aggregate(purchase=(Sum('total_paid')))
    except:
        stela=0

    try:
        cloud=Order.objects.filter(owner=user, section="Cloud Services").aggregate(purchase=(Sum('total_paid')))
    except:
        cloud=0

    try:
        store=Order.objects.filter(owner=user, section="Store").aggregate(purchase=(Sum('total_paid')))
    except:
        store=0

    try:
        total = Order.objects.filter(owner=user).aggregate(purchase=(Sum('total_paid')))
    except: 
        total = 0

    site = get_current_site(request)
    host = site.domain

    if request.method == 'POST':
        form_id=request.POST.get('form-id')
        print(form_id)

        if form_id == 'updateUser':
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                try:
                    user=form.save(commit=False)
                    user.save()
                except Exception as e:
                    print(e)
            else:
                print(form.errors)
            messages.success(request, "Changes Made Successfully")
            return redirect('/users/' + str(user.id) + '/')

    context={
       'userdata': user,
       'form': form,
       'cloud': cloud,
       'store': store,
       'stela': stela,
       'total': total,
       'orders': orders,
    }

    return render(request, 'stela_control/users/update_user.html', context)

def subscribers(request):
    lineusers = UserBase.objects.filter(is_subscribed=True)

    if request.method=='POST':

        action = request.POST.get('action')
        print(action)

        if action == "lineuser":
            user_ids = request.POST.getlist('id[]')
            for id in user_ids:
                user = UserBase.objects.filter(pk=id)
                user.delete()
                
            messages.success(request, "Changes Made Successfully")
        
    context={
        'lineusers': lineusers,
    }

    return render(request, 'stela_control/users/subs_list.html', context)

@login_required
def update_subscribers(request, id):
    getsub=UserBase.objects.get(id=id)
    try:
        customer=Customer.objects.get(email=getsub.email)
        pay=BillingRecipt.objects.filter(customer=customer, option="Stela Subscription").last()
    except:
        customer=None
        pay=None
    form2=BillingFormSuscription()
    get_formset = inlineformset_factory(
        BillingRecipt, ItemServices, 
        form=BillingChargeFormDynamic, 
        extra=1, can_delete=False,
        )
    formset_kwargs = {'form_kwargs': {'request': request}}
    formset = get_formset(prefix="form", **formset_kwargs)
    get_formset2 = inlineformset_factory(
        BillingRecipt, ItemDiscount, 
        form=BillingDiscountForm, 
        extra=0, can_delete=False,
    )
    formset2=get_formset2(prefix='discounts')
    user = UserBase.objects.get(id=id)
    superuser = UserBase.objects.get(pk=request.user.id, is_superuser=True)
    form = UserForm(instance=user)
    orders = Order.objects.filter(owner=user, section="Stela Websites")
    
    try:
        stela=Order.objects.filter(owner=user, section="Stela Websites").aggregate(purchase=(Sum('total_paid')))
    except:
        stela=0

    try:
        cloud=Order.objects.filter(owner=user, section="Cloud Services").aggregate(purchase=(Sum('total_paid')))
    except:
        cloud=0

    try:
        store=Order.objects.filter(owner=user, section="Store").aggregate(purchase=(Sum('total_paid')))
    except:
        store=0

    try:
        total = Order.objects.filter(owner=user).aggregate(purchase=(Sum('total_paid')))
    except: 
        total = 0

    site = get_current_site(request)
    host = site.domain

    if request.method == 'POST':
        form_id=request.POST.get('form-id')
        print(form_id)

        if form_id == 'NewSuscription':
            form2=BillingFormSuscription(request.POST) 
            formset=get_formset(request.POST, prefix="form", **formset_kwargs)
            formset2=get_formset2(request.POST, prefix='discounts')
            
            if all([form2.is_valid(),
                formset.is_valid(),
                formset2.is_valid()
                ]):

                full_name = user.full_name
                address = user.address
                phone = user.phone_number
                email = user.email

                customer = Customer.objects.filter(email=email)

                if customer.exists():
                    customer.update(
                        owner=request.user,
                        full_name=full_name,
                        address=address,
                        phone=phone,
                        email=email,
                    )
                else:
                    Customer.objects.create(
                        owner=request.user,
                        full_name=full_name,
                        address=address,
                        phone=phone,
                        email=email,
                    )   
                get_costumer = Customer.objects.get(email=email)
            
                parent = form2.save(commit=False)
                parent.owner = superuser
                parent.option = 'Monthly charge'
                parent.customer = get_costumer
                parent.save()
        
                for form in formset:
                    get_service = str(form.cleaned_data['field'])
                    text_splitted = get_service.split(' - ')
                    get_qty = form.cleaned_data['qty']
                    service = Modules.objects.get(title=text_splitted[0])
                    amount = service.price * get_qty
                    child = form.save(commit=False)
                    child.recipt_id = parent.id
                    child.fied_id = service.id
                    child.amount = amount
                    child.save()
                
                for form in formset2:
                    child = form.save(commit=False)
                    child.recipt_id = parent.id
                    child.save()
                

                get_amount = ItemServices.objects.filter(recipt=parent).aggregate(total=(Sum('amount')))
                get_discounts = ItemDiscount.objects.filter(recipt=parent).aggregate(total=(Sum('amount')))
                
                amount = get_amount['total']

                taxes = amount * Decimal(0.10)

                if get_discounts['total']:
                    discount = get_discounts['total']
                    BillingRecipt.objects.filter(id=parent.id).update(amount=amount, discount=discount)
                    recipt = BillingRecipt.objects.get(id=parent.id)
                    
                else:
                    discount = ''

                BillingRecipt.objects.filter(id=parent.id).update(tax=taxes)

                BillingRecipt.objects.filter(id=parent.id).update(amount=amount)

                recipt = BillingRecipt.objects.get(id=parent.id)

                messages.success(request, _("Changes made successfully"))
                return redirect('/billings/preview/' + str(recipt.id))

        if form_id == 'updateUser':
            form = UserForm(request.POST, instance=user)
            if form.is_valid():
                email=form.cleaned_data['email']
                master_user=UserBase.objects.get(username="emmerut")
                name=form.cleaned_data['full_name']
                address=form.cleaned_data['address']
                phone=form.cleaned_data['phone_number']
                try:
                    user=form.save(commit=False)

                    user.save()
                    cust=Customer.objects.filter(email=email)
                    if cust.exists():
                        cust.update(
                            full_name=name,
                            email=email,
                            address=address,
                            phone=phone
                        )
                    else:
                        Customer.objects.create(
                            owner=master_user,
                            full_name=name,
                            email=email,
                            address=address,
                            phone=phone
                        )
                except Exception as e:
                    print(e)
            else:
                print(form.errors)
            messages.success(request, "Changes Made Successfully")
            return redirect('/subscribers-control/' + str(user.id) + '/')

    context={
       'userdata': user,
       'form': form,
       'form2': form2,
       'formset': formset,
       'formset2': formset2,
       'cloud': cloud,
       'store': store,
       'stela': stela,
       'total': total,
       'orders': orders,
       'last_pay': pay,
       'call': 'subs'
    }

    return render(request, 'stela_control/users/update_user.html', context)

#financeModule
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def paymentsHome(request):
    username=request.user.username
    user=UserBase.objects.get(username=username)
    if Wallet.objects.filter(user=user).exists():
        wallet = Wallet.objects.get(user=user)
    else:
        wallet = None
    payments = SendMoney.objects.filter(user=request.user).order_by('-date')[:5]
    today = timezone.localtime(timezone.now())
    last_year = today - relativedelta(years=1)
    date_min = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=int(0)), datetime.time.min)
    history1=today-timedelta(days=30) 
    history2=today-timedelta(days=60)   
    history3=today-timedelta(days=365)
    yesterday=today-timedelta(days=1)
    
    values = []
    profit = []
    select_values = []
    
    select_values.append(today.year)
    select_values.append(last_year.year)
    

    profit1 = StelaPayments.objects.filter(user=user, created__range=(history3, today)).aggregate(get_profit=Sum('profit'))
    values.append(today.year)
    profit.append((profit1))

    profit2 = StelaPayments.objects.filter(user=user, created=history2).aggregate(get_profit=Sum('profit'))
    values.append(date(history2, 'F'))
    profit.append((profit2))

    profit3 = StelaPayments.objects.filter(user=user, created=history1).aggregate(get_profit=Sum('profit'))
    values.append(date(history1, 'F'))
    profit.append((profit3))

    profit4 = StelaPayments.objects.filter(user=user, created__range=(history1, today)).aggregate(get_profit=Sum('profit'))
    values.append(date(today, 'F'))
    profit.append((profit4))
    
    profit_last_year = StelaPayments.objects.filter(user=user, created=last_year).aggregate(get_profit=(Sum('profit')))
    
    if profit_last_year['get_profit'] and profit1['get_profit'] > 0 :
        growth = (profit_last_year['get_profit'] * profit1['get_profit'] / 100)
    else:
        growth = 0
    
    if Order.objects.filter(owner=request.user).order_by('-id').count() > 0:
        orders = Order.objects.all().order_by('-id').count()
    else:
        orders = 0

    if OrderItems.objects.all().exists():
        total_sales = Order.objects.filter(owner=request.user).aggregate(total=(Sum('total_paid')))
        today_sales = Order.objects.filter(owner=request.user, status="Payeed", created__range=[date_min, today]).aggregate(get_total=(Sum('total_paid')))
        last_day_sales = Order.objects.filter(owner=request.user, status="Payeed", created__range=(yesterday, today)).aggregate(get_total=(Sum('total_paid')))
        
        if not today_sales['get_total']:
            increase_pure = 0
        else:
            increase_pure = (last_day_sales['get_total'] * today_sales['get_total'] / 100)
            
        increase = round(increase_pure, 2)
        get_totals = OrderItems.objects.filter(order__owner=request.user).values('product__product__title').annotate(total=Sum('amount'))
        budget = Budget.objects.filter(date__range=(history1, today)).aggregate(total=(Sum('amount')))
        
        data = ([round(item['total'] / total_sales['total'] * 100, 2 )for item in get_totals])
        
    else:
        total_sales = 0
        data = OrderItems.objects.all() 
        get_totals = OrderItems.objects.all()
        budget = 0
        today_sales = 0
        increase = 0
    if StelaPayments.objects.filter(user=user).exists():
        total_profit = StelaPayments.objects.filter(user=user).aggregate(get_profit=(Sum('profit')))
        year_taxes = StelaPayments.objects.filter(user=user, created__range=(history3, today)).aggregate(get_taxes=(Sum('taxes')))
        total_paid = StelaPayments.objects.filter(user=user).aggregate(get_total=(Sum('total_paid')))
        total_pay = SendMoney.objects.filter(user=request.user).aggregate(total=(Sum('amount')))
    else:
        total_profit = 0
        year_taxes = 0
        total_paid = 0
        total_pay = 0

    context = {
        'today_sales': today_sales,
        'budget': budget,
        'wallet': wallet,
        'payments': payments,
        'total_pay': total_pay,
        'select_values': select_values,
        'values':values,
        'profit':profit,
        'current': profit1,
        'last': profit_last_year,
        'growth': growth,
        'order_count': orders,
        'orderitems': get_totals,
        'total_sales': total_sales,
        'data': data,
        'total_profit':total_profit,
        'year_taxes':year_taxes,
        'total_paid':total_paid,
        'increase': increase
    }
    
    return render(request, 'stela_control/payments/homebrew.html', context)

def addWallet(request):
    username=request.user.username
    terms=SitePolicy.objects.using('control').filter(policy="stelacontrodynamic.com", section="Payments Policy")
    form=WalletForm()
    context = {
        'form': form,
        'terms': terms
    }
    if request.method == 'POST':
        form=WalletForm(request.POST)
        if form.is_valid():
            wallet=form.save(commit=False)
            wallet.user = UserBase.objects.get(username=username)
            wallet.save(using="master")

            messages.success(request, _("Changes made successfully"))
            return redirect('stela:wallets')
        
    return render(request, 'stela_control/payments/register-wallet.html', context)

def Wallets(request):
    username=request.user.username
    user=UserBase.objects.get(username=username)
    if Wallet.objects.filter(user=user).exists():
        wallet = Wallet.objects.filter(user=user)
    else:
        wallet = None
    context = {
        'wallets': wallet
    }
    action = request.POST.get('action')
    if action == "deleteWallet":
        pk=request.POST.get('walletid')
        obj=Wallet.objects.get(pk=pk)
        obj.delete()
        response = JsonResponse({'success': 'return something'})
        return response
    
    return render(request, 'stela_control/payments/wallet-list.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/')      
@login_required       
def withdrawals(request):
    today = timezone.localtime(timezone.now())
    history1=today-timedelta(days=30) 
    user = request.user
    bank= Wallet.objects.get(default=True)
    budget = Budget.objects.filter(user=user)
    total_budget = Budget.objects.filter(date__range=(history1, today)).aggregate(total=(Sum('amount')))
    
    if request.POST.get('action') == 'post':
        
        bank = int(request.POST.get('bankid'))
        ip = request.META.get('REMOTE_ADDR')
        send_amount = total_budget['total']
        bank_data = SendMoney.objects.create(
            user=user,
            bank_account_id=bank,
            ipadress=ip,
            amount=send_amount,
        )
        budget.delete()
        html_content = render_to_string('stela_control/emails-template/withdrawals.html', {
                        'bank': bank_data.bank_account.bank_name,
                        'account': bank_data.bank_account.account_number,
                        'amount': bank_data.amount,
                        'date': bank_data.date,
                        })

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
                'Your withdrawal has been processed successfully',
                text_content,
                settings.STELA_EMAIL,
                [settings.DEFAULT_EMAIL]
                                
            )
        email.attach_alternative(html_content, "text/html")
        email.send()

        return redirect('stela:homebrew')

    context = {
        'bank': bank,
        'budget': total_budget,

    }

    return render(request, 'stela_control/payments/withdraw.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def stelaBilling(request):
    recipt = BillingRecipt.objects.filter(owner=request.user)
    subtotal = BillingRecipt.objects.filter(status="Dynamic Billing").aggregate(billing=(Sum('amount')))
    tax = BillingRecipt.objects.filter(status="Dynamic Billing").aggregate(billing=(Sum('tax')))
    discounts = BillingRecipt.objects.filter(status="Dynamic Billing").aggregate(billing=(Sum('discount')))

    if BillingRecipt.objects.filter(status="Dynamic Billing").exists():
        
        if not discounts['billing']:
            total = subtotal['billing'] + tax['billing']
        else:
            total = subtotal['billing'] + tax['billing'] - discounts['billing']
    else:
        total = None
    get_formset = inlineformset_factory(
    BillingRecipt, ItemProducts, 
    form=BillingChargeFormPOS, 
    extra=1, can_delete=False,
    )
    formset_kwargs = {'form_kwargs': {'request': request}}
    formset = get_formset(**formset_kwargs, prefix='charge')
    formset2 = inlineformset_factory(
        BillingRecipt, ItemDiscount, 
        form=BillingDiscountForm, 
        extra=0, can_delete=False,
    )
 
    if request.method == 'POST':

        action = request.POST.get('action')
        print(action)

        if action == 'delete':
            objects_ids = request.POST.getlist('id[]')
            for id in objects_ids:
                object=BillingRecipt.objects.get(id=id)
                object.delete()
                try:
                    order=Order.objects.get(billing=id)
                    order.delete()
                except:
                    pass
                try:
                    payment=StelaPayments.objects.get(billing=id)
                    payment.delete(using="master")
                except:
                    pass
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if action == 'cancelRecipt':
            try:
                reciptid=request.POST.get('reciptid')
                recipt=BillingRecipt.objects.filter(pk=reciptid).update(status='Cancelled')
                    
                response = JsonResponse({'success': _('Cancellation request successful')})
                return response
            except Exception as e:
                response = JsonResponse({'failed': e})
                return response
        
        if action == 'Payeed':
            try:
                reciptid=request.POST.get('reciptid')
                recipt=BillingRecipt.objects.filter(pk=reciptid).update(status='Payeed')
                getRecipt=BillingRecipt.objects.get(id=reciptid)
                get_code=str('DP')+get_random_string(8).upper()
                validator=get_random_string(20).lower()
                subtotal=getRecipt.amount 
                taxes=subtotal * Decimal(0.1)
                total=subtotal+taxes
                username=request.user.username
                user=UserBase.objects.get(username=username)
                fetch=StelaPayments(
                    user=user,
                    key_validator=validator,
                    transaction_id=get_code,
                    payment_option='Direct Pay',
                    subtotal=subtotal,
                    taxes=taxes,
                    total_paid=total,
                    profit=subtotal * Decimal(0.30),
                    host="Emmerut"
                )
                fetch.save()
                response = JsonResponse({'success': _('Cancellation request successful')})
                return response
            except Exception as e:
                response = JsonResponse({'failed': e})
                return response

        if action == 'customer':
            userid=request.POST.get('userid')
            customer = Customer.objects.filter(userid=userid)
            
            if customer.exists():
                customer_data = render_to_string('stela_control/billing/sections/data-customer.html', {
                            'customer': customer,      
                })
                response = JsonResponse({'costumer': customer_data})
                return response
            else:
                response = JsonResponse({'notfound': _('The client is not in your records.')})
                return response
        
        if action == 'billCust':
            userid=request.POST.get('userid')
            form=BillingForm()
            customer = Customer.objects.filter(userid=userid)
            countries = Country.objects.all()
            
            if customer.exists():
                customer_data = render_to_string('stela_control/billing/sections/bill-data-customer.html', {
                            'customer': customer, 
                            'form': form,
                            'countries': countries      
                })
                response = JsonResponse({'costumer': customer_data})
                return response
            else:
                response = JsonResponse({'notfound': _('The client is not in your records.')})
                return response
            
        full_name = request.POST.get('client')
        userid = request.POST.get('userid')
        phone = request.POST.get('phone')
        address = request.POST.get('address')  
        if all([full_name,
                userid,
                phone,
                address]):                    
            try:
                formset = get_formset(request.POST, prefix='charge', **formset_kwargs)
                formset2 = formset2(request.POST)
                if all([formset.is_valid(),
                    formset2.is_valid()
                    ]):
                    costumer = Customer.objects.filter(userid=userid)
                    if costumer.exists():
                        pass
                    else:
                        Customer.objects.create(
                            owner=request.user,
                            full_name=full_name,
                            userid=userid,
                            address=address,
                            phone=phone
                        )
                    get_customer = Customer.objects.get(userid=userid)
                    parent=BillingRecipt.objects.create(
                        owner=request.user,
                        customer_id=get_customer.pk,
                        option="POS System",
                        payment_option = "USD"
                    )
                
                    for form in formset:
                        get_product = form.cleaned_data['field']
                        product = Variants.objects.get(pk=get_product.pk)
                        get_qty = form.cleaned_data['qty']
                        child = form.save(commit=False)
                        if product.quantity < get_qty:
                            get_qty = product.quantity
                            child.qty = get_qty
                        amount = product.price * get_qty
                        child.recipt_id = parent.pk
                        child.fied_id = product.pk
                        child.amount = amount
                        child.save()
                    
                    for form in formset2:
                        child = form.save(commit=False)
                        child.recipt_id = parent.id
                        child.save()
                        

                    get_amount = ItemProducts.objects.filter(recipt=parent).aggregate(total=(Sum('amount')))
                    get_discounts = ItemDiscount.objects.filter(recipt=parent).aggregate(total=(Sum('amount')))
                        
                    amount = get_amount['total']

                    taxes = amount * Decimal(0.10)

                    if get_discounts['total']:
                        discount = get_discounts['total'] 
                    else:
                            discount = None
                 
                    BillingRecipt.objects.filter(id=parent.id).update(tax=taxes)

                    BillingRecipt.objects.filter(id=parent.id).update(amount=amount, discount=discount)

                    recipt = BillingRecipt.objects.get(id=parent.id)

                    messages.success(request, _("Changes made successfully"))
                    return redirect('/billings/checkout/' + str(recipt.id))
                else:
                    print(formset.errors, formset2.errors)
            except Exception as e:
                print(e)
                return render(request, 'stela_control/billing/homebrew.html', {
                'formset': formset,
                'formset2': formset2,
                'call': "error", 
                'error': _("Please, fill at least one RECIPT CHARGES to continue"),
            })
        else:
            return render(request, 'stela_control/billing/homebrew.html', {
                'formset': formset,
                'formset2': formset2,
                'call': "error", 
                'error': _('Please, Fill all CUSTOMER DATA fields to continue')
            })

    context = {
        'pages': recipt,
        'total': total,
        'formset': formset,
        'formset2': formset2,
        'call': "home",
    }

    return render(request, 'stela_control/billing/homebrew.html', context)

def createBill(request):
    lang=request.LANGUAGE_CODE
    form=BillingForm()
    countries=Country.objects.all()
    get_formset = inlineformset_factory(
        BillingRecipt, ItemServices, 
        form=BillingChargeFormDynamic, 
        extra=1, can_delete=False,
        )
    formset_kwargs = {'form_kwargs': {'request': request}}
    formset = get_formset(**formset_kwargs, prefix='charge')
    formset2 = inlineformset_factory(
        BillingRecipt, ItemDiscount, 
        form=BillingDiscountForm, 
        extra=0, can_delete=False,
    )
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        userid = request.POST.get('userid')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        country = request.POST.get('country')
        form = BillingForm(request.POST)
        formset = get_formset(request.POST, **formset_kwargs, prefix='charge')
        formset2 = formset2(request.POST)
        
        if all([form.is_valid(),
                formset.is_valid(),
                formset2.is_valid()
            ]):
            costumer = Customer.objects.filter(userid=userid)
            if costumer.exists():
                costumer.update(
                    owner=request.user,
                    full_name=full_name,
                    userid=userid,
                    address=address,
                    phone=phone,
                    email=email,
                    country=country,
                )
            else:
                Customer.objects.create(
                    owner=request.user,
                    full_name=full_name,
                    userid=userid,
                    address=address,
                    phone=phone,
                    email=email,
                    country=country,
                )
            get_costumer = Customer.objects.get(userid=userid)
            
            parent = form.save(commit=False)
            parent.owner = request.user
            parent.customer = get_costumer
            parent.payment_option = "USD"
            parent.save()
    
            for form in formset:
                get_service = str(form.cleaned_data['field'])
                text_splitted = get_service.split(' - ')
                get_qty = form.cleaned_data['qty']
                service = Modules.objects.filter(title=text_splitted[0], parent__yearly=False, parent__type="Service", parent__lang=lang).exclude(price=0).first()
                amount = service.price * get_qty
                child = form.save(commit=False)
                child.recipt_id = parent.id
                child.fied_id = service.pk
                child.amount = amount
                child.save()
            
            for form in formset2:
                child = form.save(commit=False)
                child.recipt_id = parent.id
                child.save()
            

            get_amount = ItemServices.objects.filter(recipt=parent).aggregate(total=(Sum('amount')))
            get_discounts = ItemDiscount.objects.filter(recipt=parent).aggregate(total=(Sum('amount')))
            
            amount = get_amount['total']

            if get_costumer.country == "Venezuela":
                taxes = amount * Decimal(0.16)
            else:
                taxes = amount * Decimal(0.10)

            if get_discounts['total']:
                discount = get_discounts['total']
                BillingRecipt.objects.filter(id=parent.id).update(amount=amount, discount=discount)
                recipt = BillingRecipt.objects.get(id=parent.id)
                
            else:
                discount = ''

            if parent.option == "Budget":
                pass
            else:
                BillingRecipt.objects.filter(id=parent.id).update(tax=taxes)

            BillingRecipt.objects.filter(id=parent.id).update(amount=amount)

            recipt = BillingRecipt.objects.get(id=parent.id)

            

            messages.success(request, _("Changes made successfully"))
            return redirect('/billings/preview/' + str(recipt.id))
    
    context = {
        'form': form,
        'formset': formset,
        'formset2': formset2,
        'countries': countries,
        'call': "billing"
    }

    return render(request, 'stela_control/billing/homebrew.html', context)

def previewBilling(request, id):
    lang=request.LANGUAGE_CODE
    recipt = BillingRecipt.objects.get(id=id)
    
    if request.method == 'POST':

        if request.POST.get('action') == 'generate':
            get_recipt=BillingRecipt.objects.filter(pk=id)
            controlbudget=BillingRecipt.objects.filter(is_budget=True, is_generated=True, payment_option="USD").count() + 1
            controlbilling=BillingRecipt.objects.filter(is_generated=True, payment_option="USD").exclude(is_budget=True).count() + 1
            
            if recipt.option == 'budget_design':
                control_id='BU-'+ str(controlbudget)            
                control_bu=InvoiceControl.objects.filter(control_id=control_id)
                if control_bu.exists():
                    
                    response = JsonResponse({'budget': _('This budget is registered')})
                    return response
                else:
                    InvoiceControl.objects.create(
                        recipt=recipt,
                        control_id=control_id,                  
                        )
                    get_recipt.update(
                        status="Dynamic Billing",
                        is_generated=True,
                        is_budget=True
                    )
                    response = JsonResponse({'success': _('Budget Generated Successfully')})
                    return response

            elif recipt.option == "budget_marketing":
                control_id='BU-'+ str(controlbudget)            
                control_bu=InvoiceControl.objects.filter(control_id=control_id)
                if control_bu.exists():
                    
                    response = JsonResponse({'budget': _('This budget is registered')})
                    return response
                else:
                    InvoiceControl.objects.create(
                        recipt=recipt,
                        control_id=control_id,                  
                        )
                    get_recipt.update(
                        status="Dynamic Billing",
                        is_generated=True,
                        is_budget=True
                    )
                    response = JsonResponse({'success': _('Budget Generated Successfully')})
                    return response

            elif recipt.option == "budget_development":
                control_id='BU-'+ str(controlbudget)            
                control_bu=InvoiceControl.objects.filter(control_id=control_id)
                if control_bu.exists():
                    
                    response = JsonResponse({'budget': _('This budget is registered')})
                    return response
                else:
                    InvoiceControl.objects.create(
                        recipt=recipt,
                        control_id=control_id,                  
                        )
                    get_recipt.update(
                        status="Dynamic Billing",
                        is_generated=True,
                        is_budget=True
                    )
                    response = JsonResponse({'success': _('Budget Generated Successfully')})
                    return response
            else: 
                control_id='DB-'+ str(controlbilling)            
                control_in=InvoiceControl.objects.filter(control_id=control_id)
                if control_in.exists():

                    response = JsonResponse({'invoice': _('This invoice is registered')})
                    return response
                
                else:
                    InvoiceControl.objects.create(
                        recipt=recipt,
                        control_id=control_id,
                    )
                    get_recipt.update(
                        status="Dynamic Billing",
                        is_generated=True
                        
                    )
                    response = JsonResponse({'success': _('invoice Generated Successfully')})
                    return response

    if recipt.tax:

        if recipt.discount:
            total = recipt.amount + recipt.tax - recipt.discount
        else:
            total = recipt.amount + recipt.tax
    else:
        if recipt.discount:
            total = recipt.amount - recipt.discount
        else:
            total = recipt.amount
    control=BillingRecipt.objects.filter(is_generated=True).count() + 1
    context = {
        'recipt': recipt,
        'total': total,
        'control': control
    }
    change = request.POST.get('term')
    
    if change:
        BillingRecipt.objects.filter(id=id).update(status=change)

        messages.success(request, "Changes made successfully")
        return redirect('/billings/home')

    return render(request, 'stela_control/billing/sections/preview-recipt.html', context)

def get_billing(request, id):
    recipt = InvoiceControl.objects.get(recipt_id=id)

    if recipt.recipt.tax:

        if recipt.recipt.discount:
            total = recipt.recipt.amount + recipt.recipt.tax - recipt.recipt.discount
        else:
            total = recipt.recipt.amount + recipt.recipt.tax
    else:
        if recipt.recipt.discount:
            total = recipt.recipt.amount - recipt.recipt.discount
        else:
            total = recipt.recipt.amount

    if request.POST.get('action') == 'emailSend':

        html_content = render_to_string('stela_control/billing/sections/invoice-copy.html', {
                'total': total,
                'recipt': recipt,
                })

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
                'Recipt sent successfully',
                text_content,
                settings.STELA_EMAIL,
                [settings.MAIN_EMAIL]
                                
            )
        email.attach_alternative(html_content, "text/html")
        email.send()

        html_content = render_to_string('stela_control/billing/sections/invoice.html', {
                'total': total,
                'recipt': recipt,
                })

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
                'Billing Notification',
                text_content,
                settings.STELA_EMAIL,
                [recipt.recipt.customer.email]             
            )
    
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        response = JsonResponse({'success': 'return something'})
        return response


    context= {
        'recipt': recipt,
        'total': total,
        'call': 'getRecipt'
    }

    return render(request, 'stela_control/billing/homebrew.html', context)

def intentExpress(request):

    if request.method == 'POST':
        body = json.loads(request.body)
        total = body["total"]
        total = str(json.dumps(total))
        total = total.replace('.','')
        total = int(total)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='usd',
            metadata={
                'userid': "annonimous"
                },
            automatic_payment_methods={
                    'enabled': True,
                },
        )
        return JsonResponse({
                'clientSecret': intent['client_secret']
            })

def paymentLoader(request, id):
    recipt = BillingRecipt.objects.get(pk=id)
    return render(request, 'stela_control/billing/homebrew.html', {
        'call': 'payload',
        'inv': recipt
    })

def orderPlaced(request):
    
    
    return render(request, 'stela_control/billing/sections/order-placed.html', {
        
    })

def paymentComplete(request):
    
    
    return render(request, 'stela_control/billing/homebrew.html', {
        'call': 'purchase'
    })

def editBill(request, id):
    recipt = BillingRecipt.objects.get(id=id)
    form=BillingForm(instance=recipt)
    
    get_formset = inlineformset_factory(
        BillingRecipt, ItemServices, 
        form=BillingChargeFormDynamic, 
        extra=0, can_delete=True,
        )
    formset_kwargs = {'form_kwargs': {'request': request}}
    
    get_formset2 = inlineformset_factory(
        BillingRecipt, ItemDiscount, 
        form=BillingDiscountForm, 
        extra=0, can_delete=True,
        )
    
    formset = get_formset(instance=recipt, **formset_kwargs, prefix='charge')
    formset2 = get_formset2(instance=recipt)

    if request.method == 'POST':
            full_name = request.POST.get('full_name')
            userid = request.POST.get('userid')
            phone = request.POST.get('phone')
            address = request.POST.get('address')  
            email = request.POST.get('email')
            if all([full_name,
                    email,
                    phone,
                    address]):
                customer=Customer.objects.filter(email=email)
                if customer.exists():
                    customer.update(
                    full_name=full_name,
                    address=address,
                    phone=phone,
                    email=email,
                )
                else:
                    Customer.objects.create(
                        full_name=full_name,
                        address=address,
                        phone=phone,
                        email=email,
                    )
                get_costumer = Customer.objects.get(userid=userid)
                try:
                    form = BillingForm(request.POST, instance=recipt)
                    formset = get_formset(request.POST, **formset_kwargs, prefix='charge', instance=recipt)
                    formset2 = get_formset2(request.POST, instance=recipt)
                    if all([
                        form.is_valid(),
                        formset.is_valid(),
                        formset2.is_valid()
                        ]):

                        parent = form.save(commit=False)
                        parent.customer_id = get_costumer.id
                        parent.save()
                        print('here form')

                        instances = formset.save(commit=False)
                            
                        for obj in formset.deleted_objects:
                            obj.delete()
                            
                        for instance in instances:
                            get_service = str(instance.field)
                            text_splitted = get_service.split(' - ')
                            service = Modules.objects.get(title=text_splitted[0]) 
                            get_qty = instance.qty
                            amount = service.price * get_qty
                            instance.amount = amount
                            instance.save()

                        print('here formset')
                        instances2 = formset2.save(commit=False)

                        for obj in formset2.deleted_objects:
                            obj.delete()

                        for instance in instances2:
                            instance.save()
                        
                        print('here')
                        get_amount = ItemServices.objects.filter(recipt=recipt).aggregate(total=(Sum('amount')))
                        get_discounts = ItemDiscount.objects.filter(recipt=recipt).aggregate(total=(Sum('amount')))
                        
                        amount = get_amount['total']

                        taxes = amount * Decimal(0.10)

                        if get_discounts['total']:
                            discount = get_discounts['total'] 
                        else:
                            discount = None
                        
                        BillingRecipt.objects.filter(id=recipt.id).update(amount=amount, discount=discount)
                        recipt = BillingRecipt.objects.get(id=recipt.id)

                        BillingRecipt.objects.filter(id=recipt.id).update(tax=taxes)

                        BillingRecipt.objects.filter(id=recipt.id).update(amount=amount)

                        messages.success(request, _("Changes made successfully"))
                        return redirect('/billings/preview/' + str(recipt.id))

                except Exception as e:
                    print(form.errors, formset.errors, formset2.errors, e)
                    return render(request, 'stela_control/billing/homebrew.html', {
                            
                            'recipt': recipt,
                            'form': form,
                            'formset': formset,
                            'formset2': formset2,
                            'call': "errorUpdateBill", 
                            'error': _("Please, fill at least one RECIPT CHARGES to continue"),
                })

            else:
                return render(request, 'stela_control/billing/homebrew.html', {
                    'recipt': recipt,
                    'form': form,
                    'formset': formset,
                    'formset2': formset2,
                    'call': "error", 
                    'error': _('Please, Fill all CUSTOMER DATA fields to continue')
                })
                
        
    return render(request, 'stela_control/billing/homebrew.html',
    {   
        'recipt': recipt,
        'form': form,
        'formset': formset,
        'formset2': formset2,
        'call': "edit bill"
        }
        
    )

def get_invoice(request, id):
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
        'total': total
    }

    return render(request, 'stela_control/billing/sections/recipt-detail.html', context)

def get_invoice_ves(request, id):
    invoice = ControlFacturacion.objects.get(pk=id)

    context = {
        'inv': invoice,
    }

    return render(request, 'stela_control/billing/sections/recipt-detail-ves.html', context)

#CronActions 
def basicSubscription():
    master_user=UserBase.objects.get(username="emmerut")
    service=Inventory.objects.get(title="Stela Basic")
    get_control_number=BillingRecipt.objects.filter(is_generated=True).count()
    control_number = get_control_number + 1
    invoice_number = "IN"+"-"+"0"+str(control_number)
    subtotal=service.price
    tax=subtotal * Decimal(0.10)
    modules=Modules.objects.filter(parent=service)
    
    try:
        userlist=UserBase.objects.filter(is_basic=True)

        for row in userlist:
            customer=Customer.objects.filter(email=row.email)
            for cust in customer:
                invoice=BillingRecipt.objects.create(
                            owner=master_user,
                            customer=cust,
                            option="Basic Subscription",
                            amount=service.price,
                            tax=tax
                        )
            for module in modules:
                ItemServices.objects.create(
                    recipt=invoice,
                    field=module,
                    amount=module.price,
                    qty=1
                )
            recipt=InvoiceControl.objects.create(
                        recipt=invoice,
                        control_id=invoice_number
                    )
            BillingRecipt.objects.filter(pk=invoice.pk).update(
                        is_generated=True
                    )
            
            if recipt.recipt.tax:
                if recipt.recipt.discount:
                    total = recipt.recipt.amount + recipt.recipt.tax - recipt.recipt.discount
                else:
                    total = recipt.recipt.amount + recipt.recipt.tax
            else:
                if recipt.recipt.discount:
                    total = recipt.recipt.amount - recipt.recipt.discount
                else:
                    total = recipt.recipt.amount

            html_content = render_to_string('stela_control/billing/sections/invoice-copy.html', {
                    'total': total,
                    'recipt': recipt,
                    })

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                    _('Recipt sent successfully'),
                    text_content,
                    settings.STELA_EMAIL,
                    [settings.MAIN_EMAIL]
                                    
                )
            email.attach_alternative(html_content, "text/html")
            email.send()

            html_content = render_to_string('stela_control/billing/sections/invoice.html', {
                    'total': total,
                    'recipt': recipt,
                    })

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                    _('Billing Notification'),
                    text_content,
                    settings.STELA_EMAIL,
                    [recipt.recipt.owner.email]             
                )
            email.attach_alternative(html_content, "text/html")
            email.send()
    except:
        pass

def midSubscription():
    
    master_user=UserBase.objects.get(username="emmerut")
    service=Inventory.objects.get(title="Stela Business")
    get_control_number=BillingRecipt.objects.filter(is_generated=True).count()
    control_number = get_control_number + 1
    invoice_number = "IN"+"-"+"0"+str(control_number)
    subtotal=service.price
    tax=subtotal * Decimal(0.10)
    modules=Modules.objects.filter(parent=service)
    master_user=UserBase.objects.get(username="emmerut")

    try:
        userlist=UserBase.objects.filter(is_business=True)
        
        for row in userlist:
            customer=Customer.objects.filter(email=row.email)
            for cust in customer:
                invoice=BillingRecipt.objects.create(
                            owner=master_user,
                            customer=cust,
                            option="Business Subscription",
                            amount=service.price,
                            tax=tax
                        )
                for module in modules:
                    ItemServices.objects.create(
                        recipt=invoice,
                        field=module,
                        amount=module.price,
                        qty=1
                    )
                recipt=InvoiceControl.objects.create(
                            recipt=invoice,
                            control_id=invoice_number
                        )
                BillingRecipt.objects.filter(pk=invoice.pk).update(
                            is_generated=True
                        )
                    
                if recipt.recipt.tax:
                    if recipt.recipt.discount:
                        total = recipt.recipt.amount + recipt.recipt.tax - recipt.recipt.discount
                    else:
                        total = recipt.recipt.amount + recipt.recipt.tax
                else:
                    if recipt.recipt.discount:
                        total = recipt.recipt.amount - recipt.recipt.discount
                    else:
                        total = recipt.recipt.amount

                html_content = render_to_string('stela_control/billing/sections/invoice-copy.html', {
                        'total': total,
                        'recipt': recipt,
                        })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                        _('Recipt sent successfully'),
                        text_content,
                        settings.STELA_EMAIL,
                        [settings.MAIN_EMAIL]
                                            
                    )
                email.attach_alternative(html_content, "text/html")
                email.send()

                html_content = render_to_string('stela_control/billing/sections/invoice.html', {
                        'total': total,
                        'recipt': recipt,
                        })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                        _('Billing Notification'),
                        text_content,
                        settings.STELA_EMAIL,
                        [recipt.recipt.owner.email]             
                    )
                email.attach_alternative(html_content, "text/html")
                email.send()
    except:
        pass    

def instanceHoursUsage():
    master_user=UserBase.objects.get(username="emmerut")
    get_control_number=BillingRecipt.objects.filter(is_generated=True, is_budget=False, payment_option="USD",).count()
    control_number = get_control_number + 1
    invoice_number = "DB"+"-"+"0"+str(control_number)
    from datetime import date
    current = date.today()
    first_day_of_month = date(current.year, current.month, 1)   
    cloud_users=UserBase.objects.filter(cloud_services=True)
    if cloud_users.exists():
        for user in cloud_users:
            customer= Customer.objects.get(
                email=user.email,
            )
            invoice=BillingRecipt.objects.create(
                owner=master_user,
                customer=customer,
                payment_option="USD",
                option="Cloud Subscription",
            )
            time_period = {
                'Start': str(first_day_of_month),
                'End': str(current)
            }
            granularity = 'MONTHLY'
            metrics = [
            'BlendedCost',
            'UnblendedCost',
            'UsageQuantity'
            ]
            group_by = [
            {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
            }
            ]
            filter = {
                'Dimensions': {
                'Key': 'LINKED_ACCOUNT',
                'Values': [user.cloud_id]
                }
            }

            # Define las credenciales de autenticación
            session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            ce = session.client('ce')

            # Haz la llamada a la API de Cost Explorer
            response = ce.get_cost_and_usage(
                TimePeriod=time_period,
                Granularity=granularity,
                Metrics=metrics,
                GroupBy=group_by,
                Filter=filter
            )

            # Procesa los datos de la respuesta
            for result_by_time in response['ResultsByTime']:
                for group in result_by_time['Groups']:

                    cloudservice=group['Keys'][0] == "Amazon Elastic Compute Cloud - Compute"
                    storageservices=group['Keys'][0] == "EC2 - Other"
                    contentservice=group['Keys'][0] == "Amazon Simple Storage Service"
                    servicedns=group['Keys'][0] == "Amazon Route 53"    

                    if cloudservice:
                        vc=VirtualCloud.objects.get(owner_id=user.id)
                        module=Modules.objects.get(title=vc.module, parent__title="Stela Cloud Services")
                        cost=round(Decimal(group['Metrics']['BlendedCost']['Amount']), 2)
                        usage=round(Decimal(group['Metrics']['UsageQuantity']['Amount']), 0)
                        profit=cost * Decimal(1.00)
                        price=cost+profit
                        unit=price/usage
                        ItemServices.objects.create(
                            recipt=invoice,
                            field=module,
                            amount=price,
                            qty=usage
                        )
                        UsageCloud.objects.create(
                            cloudstorage=vc,
                            usage=round(Decimal(group['Metrics']['UsageQuantity']['Amount']), 0),
                            monthy_cost=price
                        )
                        Modules.objects.filter(pk=module.pk).update(price=unit)

                    if storageservices:
                        cstorage=CloudStorage.objects.get(owner_id=user.id)
                        module=Modules.objects.get(title=cstorage.module, parent__title="Stela Cloud Services")
                        cost=round(Decimal(group['Metrics']['BlendedCost']['Amount']), 2)
                        print(cost)
                        usage=round(Decimal(group['Metrics']['UsageQuantity']['Amount']), 0)
                        profit=cost * Decimal(0.30)
                        price=cost+profit
                        unit=price/usage
                        ItemServices.objects.create(
                            recipt=invoice,
                            field=module,
                            amount=price,
                            qty=usage
                        )
                        UsageCloud.objects.create(
                            cloudstorage=cstorage,
                            usage=round(Decimal(group['Metrics']['UsageQuantity']['Amount']), 0),
                            monthy_cost=price
                        )
                    
                    if contentservice:
                        crequest=ResquetsCloud.objects.get(owner_id=user.id)
                        module=Modules.objects.get(title=crequest.module, parent__title="Stela Cloud Services")
                        cost=round(Decimal(group['Metrics']['BlendedCost']['Amount']), 2)
                        usage=round(Decimal(group['Metrics']['UsageQuantity']['Amount']), 0)
                        profit=cost * Decimal(0.30)
                        price=cost+profit
                        unit=price/3
                        ItemServices.objects.create(
                            recipt=invoice,
                            field=module,
                            amount=price,
                            qty=usage
                        )
                        UsageCloud.objects.create(
                            cloudstorage=crequest,
                            usage=round(Decimal(group['Metrics']['UsageQuantity']['Amount']), 0),
                            monthy_cost=price
                        )
                        Modules.objects.filter(pk=module.pk).update(price=unit)
                    
                    if servicedns:
                        domains=Domains.objects.filter(owner=user).count()
                        dns=ZoneDNS.objects.get(owner_id=user.id)
                        module=Modules.objects.get(title=dns.module, parent__title="Stela Cloud Services")
                        cost=round(Decimal(group['Metrics']['BlendedCost']['Amount']), 2)
                        usage=round(Decimal(group['Metrics']['UsageQuantity']['Amount']), 0)
                        profit=cost * Decimal(0.30)
                        price=cost+profit
                        print(domains)
                        unit=price/domains
                        ItemServices.objects.create(
                            recipt=invoice,
                            field=module,
                            amount=price,
                            qty=usage
                        )
                        UsageCloud.objects.create(
                            cloudstorage=dns,
                            usage=round(Decimal(group['Metrics']['UsageQuantity']['Amount']), 0),
                            monthy_cost=price
                        )
                        Modules.objects.filter(pk=module.pk).update(price=unit)
                    
            
            get_amount = ItemServices.objects.filter(recipt=invoice).aggregate(total=(Sum('amount')))
                
            amount = get_amount['total']

            taxes = amount * Decimal(0.10)

            BillingRecipt.objects.filter(pk=invoice.pk).update(
                        is_generated=True,
                        amount=amount,
                        tax=taxes,
                    )
            recipt=InvoiceControl.objects.create(
                        recipt=invoice,
                        control_id=invoice_number
                    )
                
            if recipt.recipt.tax:
                if recipt.recipt.discount:
                    total = recipt.recipt.amount + recipt.recipt.tax - recipt.recipt.discount
                else:
                    total = recipt.recipt.amount + recipt.recipt.tax
            else:
                if recipt.recipt.discount:
                    total = recipt.recipt.amount - recipt.recipt.discount
                else:
                    total = recipt.recipt.amount

            html_content = render_to_string('stela_control/billing/sections/invoice-copy.html', {
                    'total': total,
                    'recipt': recipt,
                    })

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                    _('Recipt sent successfully'),
                    text_content,
                    settings.STELA_EMAIL,
                    [settings.MAIN_EMAIL]
                                        
                )
            email.attach_alternative(html_content, "text/html")
            email.send()

            html_content = render_to_string('stela_control/billing/sections/invoice.html', {
                    'total': total,
                    'recipt': recipt,
                    })

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                    _('Billing Notification'),
                    text_content,
                    settings.STELA_EMAIL,
                    [recipt.recipt.owner.email]             
                )
            email.attach_alternative(html_content, "text/html")
            email.send()
  
def test(request):
    
    
    context = {
        
    }
    return render(request, 'test.html', context)