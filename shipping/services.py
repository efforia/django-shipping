#!/usr/bin/python
#
# This file is part of django-ship project.
#
# Copyright (C) 2011-2020 William Oliveira de Lagos <william.lagos@icloud.com>
#
# Shipping is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shipping is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Shipping. If not, see <http://www.gnu.org/licenses/>.
#

from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse as response
from django.core.mail import send_mail

def user(name): 
    return User.objects.filter(username=name)[0]

def superuser(): 
    return User.objects.filter(is_superuser=True)[0]

def send_invoice(request):
	send_mail('Subject here', 'Here is the message.','contato@efforia.com.br',
    ['william.lagos1@gmail.com'], fail_silently=False)
	return response('E-mail sended.')

class ShippingService:

    def __init__(self): 
        pass

    def verify_permissions(self, request):
        perm = 'super'
        if 'permissions' in request.COOKIES:
            perm = request.COOKIES['permissions']
        permissions = True if 'super' in perm else False
        return permissions

    def start(self, request):
        # Painel do usuario
        u = user('efforia'); 
        permissions = self.verify_permissions(request)
        actions = settings.EFFORIA_ACTIONS; apps = []
        for a in settings.EFFORIA_APPS: apps.append(actions[a])
        return render(request,'interface.html',{'static_url':settings.STATIC_URL,
                                            'user':user('efforia'),'perm':permissions,
                                            'name':'%s %s' % (u.first_name,u.last_name),'apps':apps
                                            },content_type='text/html')
        # Pagina inicial
        #p = list(Page.objects.filter(user=superuser()))
        #return render(request,'index.html',{'static_url':settings.STATIC_URL},content_type='text/html')

    def external(self, request):
        u = self.current_user(request)
        sellables = Sellable.objects.filter(user=u)
        for s in sellables: s.paid = True
        return self.redirect('/')

    def profile_view(self, request, name):
        if len(list(User.objects.filter(username=name))) > 0: request.session['user'] = name
        r = redirect('/')
        r.set_cookie('permissions','view_only')
        return r

    def json_decode(self, string):
        j = json.loads(string,'utf-8')
        return ast.literal_eval(j)

    def url_request(self, url, data=None, headers={}):
        request = urllib.request.Request(url=url,data=data,headers=headers)
        request_open = urllib.request.urlopen(request)
        return request_open.geturl()

    def do_request(self, url, data=None, headers={}):
        response = ''
        request = urllib.request.Request(url=url,data=data,headers=headers)
        try:
            request_open = urllib.request.urlopen(request)
            response = request_open.read()
            request_open.close()
        except urllib.error.HTTPError as e:
            print(url)
            print(data)
            print(headers)
            print(e.code)
            print(e.msg)
            print(e.hdrs)
            print(e.fp)
        return response

    def object_token(self, token):
        relations = settings.EFFORIA_TOKENS
        typobject = relations[token]
        return typobject

    def object_byid(self, token, ident):
        obj = self.object_token(token)
        return globals()[obj].objects.filter(id=ident)[0]

    def convert_datetime(self, date_value):
        d = time.strptime(date_value,'%d/%m/%Y')
        return datetime.fromtimestamp(time.mktime(d))

    def authenticate(self, username, password):
        exists = User.objects.filter(username=username)
        if exists:
            if exists[0].check_password(password): 
                return exists
        else: return None

    def authenticated(self):
        name = self.get_current_user()
        if not name: 
            #self.redirect('login')
            self.render('templates/enter.html',STATIC_URL=settings.STATIC_URL)
            return False
        else:
            return True

    def accumulate_points(self, points,request=None):
        if request is None: u = self.current_user()
        else: u = self.current_user(request)
        current_profile = Profile.objects.all().filter(user=u)[0]
        current_profile.points += points
        current_profile.save()

    # Correios class code

    def postal_code(self, request):
        u = self.current_user(request)
        s = ''; mail_code = request.GET['address']
        q = self.consulta(mail_code)[0]
        d = fretefacil.create_deliverable('91350-180',mail_code,'30','30','30','0.5')
        value = fretefacil.delivery_value(d)
        formatted = '<div>Valor do frete: R$ <div style="display:inline;" class="delivery">%s</div></div>' % value
        for i in q.values(): s += '<div>%s\n</div>' % i
        s += formatted
        now,objs,rels = self.get_object_bydate(request.GET['object'],'$$')
        obj = globals()[objs].objects.all().filter(date=now)[0]
        deliverable = Deliverable(product=obj,buyer=u,mail_code=mail_code,code=d['sender'],receiver=d['receiver'],
        height=int(d['height']),length=int(d['length']),width=int(d['width']),weight=int(float(d['weight'][0])*1000.0),value=value)
        deliverable.save()
        return response(s)

    # Deliveries class code

    def view_package(self, request):
        u = self.current_user(request)
        form = DeliveryForm()
        form.fields['address'].label = 'CEP'
        if 'quantity' in request.GET:
            quantity = request.GET['quantity']
            credit = int(request.GET['credit'])
        else:
            quantity = 1; credit = 1
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "1.00",
            "item_name": "Produto do Plethora",
            "invoice": "unique-invoice-id",
            "notify_url": "http://www.efforia.com.br/paypal",
            "return_url": "http://www.efforia.com.br/delivery",
            "cancel_return": "http://www.efforia.com.br/cancel",
            'currency_code': 'BRL',
            'quantity': quantity,
        }
        payments = PayPalPaymentsForm(initial=paypal_dict)
        diff = credit-u.profile.credit
        if diff < 0: diff = 0
        return render(request,"delivery.pug",{
                                               'payments':payments,
                                               'credit':diff,
                                               'form':form
                                               },content_type='text/html')

    def create_package(self, request):
        u = self.current_user(request)
        Cart.objects.all().filter(user=u).delete()
        return self.redirect('/')