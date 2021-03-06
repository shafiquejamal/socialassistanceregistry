from django.conf.urls import patterns, include, url
from django.conf import settings
from accounts.forms import EditProfileForm2
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView
from userena import views as userena_views
from userena.forms import (SignupForm, AuthenticationForm)

from django.conf.urls.i18n import i18n_patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

form_signup = SignupForm
form_signin = AuthenticationForm

urlpatterns = patterns('',
	(r'^i18n/', include('django.conf.urls.i18n')),
	(r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
)

urlpatterns += i18n_patterns('',
    # Examples:
    # url(r'^$', 'nr.views.home', name='home'),
    # url(r'^nr/', include('nr.foo.urls')),

    # I want the user to be redirected to the edit profile form after activation. This also generates the suite number
	#	automatically.
    url(r'^accounts/activate/(?P<activation_key>\w+)/$', 'userena.views.activate', {'success_url': '/applicants/', }, name='userena_activate'),
    #url(r'^accounts/signin/$', userena_views.signin, {'success_url': 'applicants', }, name='userena_signin'),

    # For django-userena
    url(r'^accounts/signin/$', 'nr.views.signin', name='userena_signin'),
    url(r'^accounts/signup/$', 'nr.views.signup', name='userena_signup'),
    (r'^accounts/', include('userena.urls')), 
    url(r'^$', 'nr.views.home', name='home'),

    # My my applicants app
    (r'^applicants/', include('applicants.urls', namespace="applicants")), 

    # The contact form - its just a page with an email address
    url(r'^contact/$', login_required(TemplateView.as_view(template_name="contact.html")), name="contact"),
    url(r'^faq/$', TemplateView.as_view(template_name="faq.html"), name="faq"),
    url(r'^termsandconditions/$', TemplateView.as_view(template_name="termsandconditions.html"), name="termsandconditions"),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# urlpatterns += patterns('', (r'^static/(.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT }), ) 
urlpatterns += i18n_patterns('', (r'^static/(.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT }), ) 
urlpatterns += i18n_patterns('', (r'^media/(.*)$', 'django.views.static.serve',  { 'document_root': settings.MEDIA_ROOT }), ) 
