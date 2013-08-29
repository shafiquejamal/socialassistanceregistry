# Create your views here.
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from applicants.models import Applicant, Householdmember
from applicants.forms import ApplicantForm, HouseholdmemberForm
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from nr.formulas import mask_toggle # I want to hide the pk

from django.http import HttpResponse
import time, datetime, csv

from django.forms.models import inlineformset_factory # this is for adding fields for the items (inline)

@login_required
def create(request):
	
	# check to see that user has not exceeded daily limit
	"""
	if Pkg.packages_created_since_X_hours_classmethod(request.user, settings.PKGS_X_HOURS) > settings.PKGS_MAX_PACKAGES_REGISTER_PER_X_HOURS:
		#return HttpResponse("packages created in last 24 hours too many!: %s" % Pkg.packages_created_since_X_hours_classmethod(request.user))
		context = { 'PKGS_MAX_PACKAGES_REGISTER_PER_X_HOURS': settings.PKGS_MAX_PACKAGES_REGISTER_PER_X_HOURS,
					'PKGS_X_HOURS': settings.PKGS_X_HOURS,}
		return render(request, "pkgs/toomany.html", context)
	"""

	if request.method == 'POST': 
		form = ApplicantForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			form.instance.user = request.user
			form.save() 
			return HttpResponseRedirect(reverse('applicants:update', kwargs={'pk_masked':mask_toggle(form.instance.pk)}))
	else:
		form = ApplicantForm() # An unbound form
	return render(request, 'applicants/create.html', { 'form': form,})
	#return render(request, reverse('pkgs:create', kwargs={ 'form': form,}))

@login_required	
def update(request, pk_masked):
	pk = mask_toggle(pk_masked)
	try:
		applicant = Applicant.objects.filter(user=request.user).get(pk=pk) # make sure user can edit only own package that has not yet reached U.S. warehouse
	except:
		raise Http404

	HouseholdmemberInlineFormSet = inlineformset_factory(Applicant, Householdmember, form=HouseholdmemberForm, 
														extra=settings.APPLICANTS_EXTRA_HOUSEHOLDMEMBER_FIELD, 
														can_order=False,
														max_num=settings.INLINEFORMSET_MAXNUM
		)
	if request.method == "POST":
		formset_householdmember = HouseholdmemberInlineFormSet(request.POST, request.FILES, instance=applicant)
		form_applicant = ApplicantForm(request.POST)
		if formset_householdmember.is_valid():
			formset_householdmember.save()
			if "saveandaddmore" in request.POST:
				#return HttpResponseRedirect(reverse('pkgs:update', kwargs={'pk':pk}))
				return HttpResponseRedirect(reverse('applicants:update', kwargs={'pk_masked':pk_masked}))
			else:
				#return HttpResponseRedirect(reverse('pkgs:detail', kwargs={'pk':pk}))
				return HttpResponseRedirect(reverse('applicants:detail', kwargs={'pk_masked':pk_masked}))
		else:
			pass
	else:
		formset_householdmember = HouseholdmemberInlineFormSet(instance=applicant)
		form_applicant = ApplicantForm()
	return render_to_response("applicants/update.html", { "formset_householdmember": formset_householdmember, "applicant": applicant, "pk_masked": pk_masked,}, context_instance=RequestContext(request))
	
@login_required	
def delete(request, pk_masked):
	pk = mask_toggle(pk_masked)
	try:
		applicant = Applicant.objects.filter(user=request.user).get(pk=pk)
	except:
		raise Http404

	try:
		applicant.delete()
	except:
		raise Http404
		
	return HttpResponseRedirect(reverse('applicants:index'))

@login_required	
def update_applicant(request, pk_masked):
	pk = mask_toggle(pk_masked)
	try:
		applicant = Applicant.objects.filter(user=request.user).get(pk=pk)
	except:
		raise Http404

	if request.method == "POST":
		form = ApplicantForm(request.POST, instance=applicant) 
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('applicants:detail', kwargs={'pk_masked':pk_masked}))
	else:
		form = ApplicantForm(instance=applicant)
	return render_to_response('applicants/update_applicant.html', {'form': form, 'pk_masked': pk_masked,}, context_instance=RequestContext(request)) 


@login_required	
def download_all(request):
	
	today = datetime.datetime.now()
	localtime = today.strftime('m%m_d%d_%Y_%H:%M:%S')
	filename = "applicants_"+localtime+".csv"
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="'+filename+'"'

	if (Applicant.objects.all().count()) == 0:
		return response

	applicants = Applicant.objects.all()

	# field names for Applicant
	field_names = Applicant._meta.get_all_field_names()
	field_names.remove('householdmember') # don't know how to keep this from getting in there
	# add in field names that are categories/choices with key-value pair dictionaries
	
	field_names_getdisplay = []
	for field in field_names:
		temp_field = "get_"+str(field)+"_display"
		# check whether the field has choices
		try:
			temp_text = getattr(applicants[0],temp_field)()
			field_names_getdisplay.append(temp_field)
		except:
			pass
	# this adds properties	
	field_names.extend([name for name in dir(Applicant) if isinstance(getattr(Applicant, name), property)])

	# field names for Householdmember
	field_names_hhm = Householdmember._meta.get_all_field_names()
	field_names_hhm_getdisplay = []
	householdmember = Householdmember.objects.get(pk=1) # this is a hack, that I should fix. Should get from the model, not an instace. Same as above. What if there are no records for Householdmember?
	for field in field_names_hhm:
		temp_field = "get_"+str(field)+"_display"
		# check whether the field has choices
		try:
			temp_text = getattr(householdmember,temp_field)()
			field_names_hhm_getdisplay.append(temp_field)
		except:
			pass

	writer = csv.writer(response, quoting=csv.QUOTE_ALL)
	#writer.writerow(field_names+user_data_label)
	writer.writerow(field_names+field_names_getdisplay+field_names_hhm+field_names_hhm_getdisplay)

	for applicant in applicants:
		# this is applicant-level (household-level) data
		data_applicant = [unicode(getattr(applicant, field)).encode('utf-8') for field in field_names]
		data_applicant_getdisplay = [unicode(getattr(applicant, field)()).encode('utf-8') for field in field_names_getdisplay]
		data_applicant += data_applicant_getdisplay
		try:
			householdmembers = Householdmember.objects.all().filter(applicant=applicant)
			# this is individual-level data
			for householdmember in householdmembers:
				data_householdmember = [unicode(getattr(householdmember, field)).encode('utf-8') for field in field_names_hhm]
				data_householdmember_getdisplay = [unicode(getattr(householdmember, field)()).encode('utf-8') for field in field_names_hhm_getdisplay]
				data_householdmember += data_householdmember_getdisplay
				data_applicant_and_householdmember = data_applicant+data_householdmember
				writer.writerow(data_applicant_and_householdmember)
			else:
				data_householdmember = ['-']*len(field_names_hhm+field_names_hhm_getdisplay)
				data_applicant_and_householdmember = data_applicant+data_householdmember
				writer.writerow(data_applicant_and_householdmember)
		except:
			data_householdmember = ['-']*len(field_names_hhm+field_names_hhm_getdisplay)
			data_applicant_and_householdmember = data_applicant+data_householdmember
			writer.writerow(data_applicant_and_householdmember)
			 
	return response