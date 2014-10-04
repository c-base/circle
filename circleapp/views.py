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

def home(request):
    return render_to_response('circle/home.django', {})
