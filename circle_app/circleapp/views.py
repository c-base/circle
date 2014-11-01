# -*- coding: utf-8 -*-

from models import Circle, Topic, Voting, Poll
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth import authenticate
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy

#from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import datetime

from forms import LoginForm, MemberForm

from jsonrpc import jsonrpc_method
from rest_framework import viewsets


from serializers import CircleSerializer, TopicSerializer


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
    circle = Circle.objects.current()
    return render(request, 'current_circle.django', {'circle': circle})


@login_required
def show_circle(request, circle_id):
    return render_to_response('home.django', {})

@login_required
def list_circles(request):
    circles = Circle.objects.all().order_by('-date')
    return render_to_response('list_circles.django', {'circles': circles, 'userlist': get_userlist()}, context_instance=RequestContext(request))

@jsonrpc_method('list_circles')
def list_circles_rpc(request):
    return [circle.date for circle in Circle.objects.all().order_by('-date')]

@login_required
def list_topics(request):
    topics = Topic.objects.all()#.order_by('-circle_id')
    print topics
    return render_to_response('list_topics.django', {'topics': topics, 'userlist': get_userlist()}, context_instance=RequestContext(request))

@login_required
def show_topic(request, topic_uuid):
    return render(request, 'show_topic.django', {'topic': Topic.objects.get(uuid=topic_uuid)})

@login_required
def topic_pad(request, topic_uuid):
    return HttpResponseRedirect(Topic.objects.get(uuid=topic_uuid).etherpad_link)

def add_topic(request):
    return render(request, 'edit_topic.django', {})

@login_required
def select_user(request):
    return render(request, 'select_user.django', {})

@login_required
def add_user(request):
    return render(request, 'select_user.django', {})

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


# API views
class CircleViewSet(viewsets.ModelViewSet):
    """
    Viewset for /api/v1/circles/ and /api/v1/circles/:id/
    """
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer


circle_list = snippet_list = CircleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

circle_detail = CircleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

class CurrentCircleViewSet(viewsets.ModelViewSet):
    """
    Viewset for api/circles/current/
    """
    serializer_class = CircleSerializer

    def get_object(self, queryset=None):
        return Circle.objects.current()


current_circle_detail = CurrentCircleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


class TopicViewSet(viewsets.ModelViewSet):
    """
    Viewset for api/topic/:uuid/
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    lookup_field = 'uuid'

topic_list = snippet_list = TopicViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

topic_detail = TopicViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

class AjaxTemplateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)

class AddUserFormView(AjaxTemplateMixin, FormView):
    template_name = 'select_user.django'
    ajax_template_name = "select_user.django"
    form_class = MemberForm
    success_url = reverse_lazy('home')
    success_message = "Way to go!"

#https://github.com/d-m/django-modal-forms/blob/master/test_app/urls.py
#class HomeView(TemplateView):
    #template_name = 'test_app/home.html'

