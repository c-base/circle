# -*- coding: utf-8 -*-

#from jsonrpc import jsonrpc_method
from models import Member, Group, Circle, Topic, Decision, Opinion
from datetime import datetime, timedelta, date
from django.utils import timezone
#from jsonrpc.proxy import ServiceProxy
#import cbeamdcfg as cfg

from django.template import Context, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth import authenticate
#from forms import LoginForm, MissionForm, StripeForm, UserForm, LogActivityForm, ActivityLogCommentForm
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from jsonrpc import jsonrpc_method
import json

def home(request):
    return render_to_response('home.django', {})

def begin_circle(request):
    day = timezone.now().day
    if day != 1 and day != 14:
        return render_to_response('no_circle_date_error', {})
    return render_to_response('home.django', {})

def end_circle(request):
    return render_to_response('home.django', {})

def current_circle(request):
    return render_to_response('home.django', {})

def list_circles(request):
    circles = Circle.objects.all().order_by('-circle_id')
    return render_to_response('list_circles.django', {'circles': circles})

@jsonrpc_method('list_circles')
def list_circles_rpc(request):
    return [ circle.circle_id for circle in Circle.objects.all().order_by('-circle_id') ]


# nächster circle wird automatisch angelegt, wenn der aktuelle circle beendet wird.
# alle topics, die keinem circle zugordnet sind, werden automatisch dem neuen circle zugeordnet
