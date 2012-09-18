from django.conf import settings
from django.conf.urls import patterns, include, url
from apps.main.views import home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #            {'document_root': settings.STATIC_ROOT}),
    
    
    url(r'^$', home, name='home'),
    
    url(r'^risk-assessments/', include('apps.riskassessments.urls')),
    url(r'^dashboard/', include('apps.dashboard.urls')),
    #url(r'^accounts/', include('apps.accounts.urls')),
    #url(r'^intake/', include('apps.intake.urls')),
    
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()