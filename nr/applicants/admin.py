from django.contrib import admin 
from applicants.models import Applicant, Householdmember
import reversion

"""
class HouseholdmemberInline(admin.TabularInline):
	model = Householdmember
	extra = 1

class ApplicantAdmin(admin.ModelAdmin):
	inlines = [HouseholdmemberInline]
	# list_display = ('user__first_name','user__last_name','merchant','tracking_number')
	#list_display = ('id','user','merchant','tracking_number')
	#list_filter = ['user']
	
admin.site.register(Applicant, ApplicantAdmin)
"""

class HouseholdmemberInline(admin.TabularInline):
	model = Householdmember
	extra = 1

class ApplicantAdmin(reversion.VersionAdmin):
	inlines = [HouseholdmemberInline]
	# list_display = ('user__first_name','user__last_name','merchant','tracking_number')
	#list_display = ('id','user','merchant','tracking_number')
	#list_filter = ['user']
	
admin.site.register(Applicant, ApplicantAdmin)