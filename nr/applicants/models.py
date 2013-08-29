from django.db import models

# Create your models here.
from django.contrib.auth.models import User  
from django.utils.translation import ugettext as _  
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from nr.formulas import mask_toggle

from datetime import date, timedelta, datetime
from django.utils.timezone import utc

class Applicant(models.Model):

	TIRANA=20
	ELBASAN=30
	DURRES=40
	SITE_CHOICES = (
		(TIRANA,_('Tirana')),
		(ELBASAN,_('Elbasan')),
		(DURRES,_('Durres')),
		)
	d_site = dict(SITE_CHOICES)
	PRIVATE_HOME = 10
	APARTMENT = 20
	DWELLINGTYPE_CHOICES = (
		(PRIVATE_HOME,_('Single Family house or private home')),
		(APARTMENT, _('Apartment')),
		)
	VERY_GOOD_CONDITION = 10
	APPROPRIATE_FOR_LIVING = 20
	INAPPROPRIATE_FOR_LIVING = 30
	UNDER_CONSTRUCTION = 40
	DWELLINGCONDITION_CHOICES = (
		(VERY_GOOD_CONDITION, _('Very good condition')),
		(APPROPRIATE_FOR_LIVING, _('Appropriate for living')),
		(INAPPROPRIATE_FOR_LIVING, _('Inappropriate for living')),
		(UNDER_CONSTRUCTION, _('Under construction')),
		)

	YES = 1
	NO = 0
	YESNO_CHOICES = (
		(YES,_('Yes')),
		(NO,_('No')),
		)

	URBAN = 1
	RURAL = 0
	AREA_CHOICES = (
		(URBAN,_('Urban')),
		(RURAL,_('Rural')),
		)
	
	SLATE = 1
	TIN = 2
	OTHER = 3
	ROOFMATERIAL_CHOICES = (
		(SLATE, _('Slate roof')),
		(TIN, _('Tin material roof')),
		(OTHER, _('Something else')),
		)
 	d_site = dict(SITE_CHOICES)
 	d_dwellingtype = dict(DWELLINGTYPE_CHOICES)
 	d_dwellingcondition = dict(DWELLINGCONDITION_CHOICES)
 	d_yesno = dict(YESNO_CHOICES)
 	d_area = dict(AREA_CHOICES)

	user 			  = models.ForeignKey(User, editable=False)
	bank_card_number  = models.CharField(_('Bank card number'),max_length=50, unique=True)
	site_of_interview = models.IntegerField(_('Site of interview'), choices = SITE_CHOICES, default=TIRANA, blank=False)
	housenumber		  = models.CharField(_('House Number'),max_length=8)
	address_line1 	  = models.CharField(_('Address line 1'),max_length=50)
	address_line2 	  = models.CharField(_('Apt #'),max_length=50,blank=True) 
	municipality 	  = models.CharField(_('Municipality/commune'),max_length=25)
	district 		  = models.CharField(_('District'),max_length=25,blank=True)
	urban			  = models.IntegerField(_('Area (urban/rural)'), choices = AREA_CHOICES, blank=False)
	postal 			  = models.CharField(_('Postal code'),max_length=25,blank=True) 
	home_phone   	  = models.CharField(_('Home telephone'),max_length=15)
	mobile_phone	  = models.CharField(_('Mobile telephone'),max_length=15)
	dwelling_type     = models.IntegerField(_('Dwelling type'), choices = DWELLINGTYPE_CHOICES, blank=False)
	rooms 			  = models.IntegerField(_('Number of rooms that your family occupies'), blank=False)
	condition         = models.IntegerField(_('What is the condition of the dwelling?'), choices = DWELLINGCONDITION_CHOICES, blank=False)
	roof_material	  = models.IntegerField(_('Roof Material?'), choices = ROOFMATERIAL_CHOICES, blank=False)
	gas_for_lighting  = models.IntegerField(_('Does your household use gas for lighting?'), choices = YESNO_CHOICES, blank=False)
	gas_for_heating   = models.IntegerField(_('Does your household use gas for heating?'), choices = YESNO_CHOICES, blank=False)
	gas_for_cooking   = models.IntegerField(_('Does your household use gas for cooking?'), choices = YESNO_CHOICES, blank=False)
	gas_for_other  	  = models.IntegerField(_('Does your household use gas for other appliances?'), choices = YESNO_CHOICES, blank=False)
	a_color_tv   	  = models.IntegerField(_('Does your household have a color TV?'), choices = YESNO_CHOICES, blank=False)
	a_washing_machine = models.IntegerField(_('Does your household have a washing machine?'), choices = YESNO_CHOICES, blank=False)
	q_cows			  = models.IntegerField(_('How many cows does your household own?'), blank=False, validators=[MinValueValidator(0), MaxValueValidator(10000000)])
	q_pigs			  = models.IntegerField(_('How many pigs does your household own?'), blank=False, validators=[MinValueValidator(0), MaxValueValidator(10000000)])
	sp_ne_amount	  = models.IntegerField(_('How much did your household receive from NE for the last payment?'), blank=False, validators=[MinValueValidator(0), MaxValueValidator(10000000)])
	sp_ne_months	  = models.IntegerField(_('How many months was this NE payment for?'), blank=False, validators=[MinValueValidator(0), MaxValueValidator(10000000)])
	sp_ne_last12m	  = models.IntegerField(_('How much did your household receive from NE for the last 12 months?'), blank=False, validators=[MinValueValidator(0), MaxValueValidator(10000000)])
	sp_dp_amount	  = models.IntegerField(_('How much did your household receive from Disability Pension for the last payment?'), blank=False, validators=[MinValueValidator(0), MaxValueValidator(10000000)])
	sp_dp_months	  = models.IntegerField(_('How many months was this Disability Pension payment for?'), blank=False, validators=[MinValueValidator(0), MaxValueValidator(10000000)])
	sp_dp_last12m	  = models.IntegerField(_('How much did your household receive from Disability Pension for the last 12 months?'), blank=False, validators=[MinValueValidator(0), MaxValueValidator(10000000)])
	oi_remit		  = models.IntegerField(_('How much did your household receive in total from remittances in the last 12 months, including the value of any gift or payment in the form of goods?'), blank=False, validators=[MinValueValidator(0), MaxValueValidator(10000000)])
	oi_rent			  = models.IntegerField(_('How much did your household receive in total from rent from land in the last 12 months, including the value of any gift or payment in the form of goods?'), blank=False, validators=[MinValueValidator(0), MaxValueValidator(10000000)])
	tell_me			  = models.TextField(_('Is there anything else you would like to tell me?'), blank=True)
	created_at 		  = models.DateTimeField(auto_now_add = True)
	updated_at        = models.DateTimeField(auto_now = True)

	class Meta:
		ordering = ["-created_at"]

	@property
	def pk_masked(self):
		return mask_toggle(self.pk)

	@property
	def score(self):		
		return 10-1*Householdmember.objects.filter(applicant=self).count()+2*self.a_washing_machine+5*self.a_color_tv

	def __unicode__(self):
		return "BCN:"+str(self.bank_card_number)+", PKM:"+str(self.pk_masked)+", PK:"+str(self.pk)

	@property
	def hhsize(self):
		return Householdmember.objects.filter(applicant=self).count()

	# from http://stackoverflow.com/questions/2170228/django-iterate-over-model-instance-field-names-and-values-in-template
	def get_all_fields(self):
		fields = []
		for f in self._meta.fields:

			fname = f.name        
			# resolve picklists/choices, with get_xyz_display() function
			get_choice = 'get_'+fname+'_display'
			if hasattr( self, get_choice):
				value = getattr( self, get_choice)()
			else:
				try :
					value = getattr(self, fname)
				except User.DoesNotExist:
					value = None

			# only display fields with values and skip some fields entirely
			if f.editable and f.name not in ('id', 'created_at', 'updated_at', 'user') :

				fields.append(
					{
					'label':f.verbose_name, 
					'name':f.name, 
					'value':value,
					}
				)
		return fields


class Householdmember(models.Model):

	MALE = 0
	FEMALE = 1
	GENDER_CHOICES =(
		(MALE,_('Male')),
		(FEMALE,_('Female')),
		)
	d_gender = dict(GENDER_CHOICES)
	HEAD = 1
	SPOUSE = 2
	CHILD = 3
	GRANDCHILD = 4
	NIECENEPHEW = 5
	FATHERMOTHER = 6
	SIBLING = 7
	SONDINLAW = 8
	SIBLINGINLAW = 9
	GRANDDADMOM = 10
	FATHERMOTHERINLAW = 11
	OTHER = 12
	NOTRELATED = 13
	RELTOHEAD_CHOICES = (
		(HEAD,_('Head')),
		(SPOUSE,_('Spouse/Partner')),
		(CHILD,_('Child/Adopted child')),
		(GRANDCHILD,_('Grandchild')),
		(NIECENEPHEW,_('Niece/Nephew')),
		(FATHERMOTHER,_('Father/Mother')),
		(SIBLING,_('Sister/Brother')),
		(SONDINLAW,_('Son/Daughter in law')),
		(SIBLINGINLAW,_('Brother/Sister in law')),
		(GRANDDADMOM,_('Grandfather/Grandmother')),
		(FATHERMOTHERINLAW,_('Father/Mother in law')),
		(OTHER,_('Other relative')),
		(NOTRELATED,_('Not related')),
		)
	d_reltohead = dict(RELTOHEAD_CHOICES)
	MARRIED = 1
	DIVORCED = 2
	LIVINGTOGETHER = 3
	WIDOWER = 4
	SINGLE = 5
	MARITAL_CHOICES = (
		(MARRIED,_('Married')),
		(DIVORCED,_('Divorced/Separated')),
		(LIVINGTOGETHER,_('Living together')),
		(WIDOWER,_('Widower')),
		(SINGLE,_('Single')),
		)
	d_marital = dict(MARITAL_CHOICES)
	YES = 1
	NO = 0
	YESNO_CHOICES = (
		(YES,_('Yes')),
		(NO,_('No')),
		)
	d_yesno = dict(YESNO_CHOICES)
	applicant 		  = models.ForeignKey(Applicant)
	first_name		  = models.CharField(_('First name'),max_length=50,blank=False)
	middle_name		  = models.CharField(_('Middle name'),max_length=50,blank=True) 
	last_name		  = models.CharField(_('Last name'),max_length=50,blank=False)
	national_id		  = models.CharField(_('National ID'),max_length=50,blank=False, unique=True)
	male 			  = models.IntegerField(_('Gender'), choices = GENDER_CHOICES, blank=False)
	date_of_birth     = models.DateField()
	rel_to_head       = models.IntegerField(_('Relationship to HH Head'), choices = RELTOHEAD_CHOICES, blank=False)
	disability 		  = models.IntegerField(_('Has a disability'), choices = YESNO_CHOICES, blank=False)
	created_at 		  = models.DateTimeField(auto_now_add = True)
	updated_at        = models.DateTimeField(auto_now = True)

	class Meta:
		ordering = ["rel_to_head"]

	# from http://stackoverflow.com/questions/2170228/django-iterate-over-model-instance-field-names-and-values-in-template
	def get_all_fields(self):
		fields = []
		for f in self._meta.fields:

			fname = f.name        
			# resolve picklists/choices, with get_xyz_display() function
			get_choice = 'get_'+fname+'_display'
			if hasattr( self, get_choice):
				value = getattr( self, get_choice)()
			else:
				try :
					value = getattr(self, fname)
				except User.DoesNotExist:
					value = None

			# only display fields with values and skip some fields entirely
			if f.editable and f.name not in ('id', 'created_at', 'updated_at', 'applicant'):

				fields.append(
					{
					'label':f.verbose_name, 
					'name':f.name, 
					'value':value,
					}
				)
		return fields
