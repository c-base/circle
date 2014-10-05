from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from jsonrpc import jsonrpc_site

import circleapp.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'circleapp.views.home', name='home'),
    url(r'^circle/begin$', 'circleapp.views.begin_circle', name="begin_circle"),
    url(r'^circle/end$', 'circleapp.views.end_circle', name="end_circle"),
    url(r'^circle/current$', 'circleapp.views.current_circle', name="current_circle"),
    url(r'^circles$', 'circleapp.views.list_circles', name="list_circles"),
    url(r'^circle/(?P<circle_id>\d{4}-\d{2}-\d{2})$', 'circleapp.views.show_circle', name="show_circle"),
    # url(r'^circle/', include('circle.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^rpc/browse/', 'jsonrpc.views.browse', name="jsonrpc_browser"), # for the graphical browser/web console only, omissible
    url(r'^rpc/', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
    #(r'^rpc/(?P<method>[a-zA-Z0-9.]+)$', jsonrpc_site.dispatch) # for HTTP GET only, also omissible

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#urlpatterns += patterns('', (r'^rpc/', jsonrpc_site.dispatch))
