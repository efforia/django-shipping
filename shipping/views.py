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

from django.http import HttpResponse as response
from django.http import JsonResponse
from django.views import View

from .email import send_invoice
from .core import Mail, Deliveries

class DeliveriesView(View):
    def get(self, request):
        return JsonResponse({'deliveries': 'success'})

def mail_send(request):
	return send_invoice(request)

def mail(request):
    m = Mail()
    if request.method == 'GET':
        return m.postal_code(request)

def delivery(request):
    deliver = Deliveries()
    if request.method == 'GET':
        return deliver.view_package(request)
    elif request.method == 'POST':
        return deliver.create_package(request)