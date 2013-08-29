from django.forms import ModelForm, DateField
from applicants.models import Applicant, Householdmember

class ApplicantForm(ModelForm):
	
	class Meta:
		model = Applicant

class HouseholdmemberForm(ModelForm):

	class Meta:
		model = Householdmember
		

	#date_of_birth = DateField(input_formats=['Y-m-d'])
	