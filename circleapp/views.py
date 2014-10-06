# -*- coding: utf-8 -*-

from models import Member, Group, Circle, Topic, Decision, Opinion
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth import authenticate
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import datetime

from forms import LoginForm

from jsonrpc import jsonrpc_method


@login_required
def home(request):
    return render_to_response('home.django', {'userlist': get_userlist()})


@login_required
def begin_circle(request):
    return render_to_response('home.django', {})


@login_required
def end_circle(request):
    return render_to_response('home.django', {})


@login_required
def current_circle(request):
    return render_to_response('current_circle.django', {})


@login_required
def show_circle(request, circle_id):
    return render_to_response('home.django', {})

@login_required
def list_circles(request):
    circles = Circle.objects.all().order_by('-circle_id')
    return render_to_response('list_circles.django', {'circles': circles, 'userlist': get_userlist()}, context_instance=RequestContext(request))

@jsonrpc_method('list_circles')
def list_circles_rpc(request):
    return [circle.circle_id for circle in Circle.objects.all().order_by('-circle_id')]


@login_required
def list_topics(request):
    topics = Topic.objects.all()#.order_by('-circle_id')
    return render_to_response('list_topics.django', {'topics': topics, 'userlist': get_userlist()}, context_instance=RequestContext(request))

def auth_login(request):
    redirect_to = request.REQUEST.get('next', '') or '/'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login_auth(request, user)
                    return HttpResponseRedirect(redirect_to)
    else:
        form = LoginForm()
    return render_to_response('login.django', RequestContext(request,
                                                             locals()))


def auth_logout(request):
    redirect_to = request.REQUEST.get('next', '') or '/'
    logout_auth(request)
    return HttpResponseRedirect(redirect_to)

def get_userlist():
    # Query all non-expired sessions
    sessions = Session.objects.filter(expire_date__gte=datetime.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)


# nächster circle wird automatisch angelegt, wenn der aktuelle circle beendet wird.
# alle topics, die keinem circle zugordnet sind, werden automatisch dem neuen circle zugeordnet
