from django.conf.urls import patterns, url
from applicants import views
from django.views.generic import DetailView, ListView
from applicants.models import Applicant, Householdmember
from django.contrib.auth.decorators import login_required
from nr.formulas import mask_toggle


class ListViewApplicants(ListView):
	paginate_by = 100
	def get_queryset(self):
		return Applicant.objects.all()
	
class DetailViewUnmask(DetailView):
	def get_object(self):
		return self.get_queryset().get(pk=mask_toggle(self.kwargs.get("pk_masked")))


urlpatterns = patterns('',

	url(r'^$',
		login_required(ListViewApplicants.as_view( 
							template_name='applicants/index.html',
							#context_object_name='form',
							)),
		name='index'),

	url(r'^(?P<pk_masked>\d+)/$',
		login_required(DetailViewUnmask.as_view( model=Applicant,
							template_name='applicants/detail.html'
							)), 
		name='detail'),

	url(r'^create/$','applicants.views.create', name='create'),

	# Should be able to do these only if status is not 0 (i.e. package is not yet at U.S. warehouse)
	url(r'^update/(?P<pk_masked>\d+)/$','applicants.views.update', name='update'),
	url(r'^update_applicant/(?P<pk_masked>\d+)/$','applicants.views.update_applicant', name='update_applicant'),
	url(r'^delete/(?P<pk_masked>\d+)/$','applicants.views.delete', name='delete'),
	url(r'^download_all/$','applicants.views.download_all', name='download_all'),		
	)
