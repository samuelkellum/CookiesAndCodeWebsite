from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Event, Meeting


class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ('email', 'is_staff', 'is_active',)
	list_filter = ('email', 'is_staff', 'is_active',)

	 # these are the fields that will display when you MODIFY a user from admin page
		# dict KEYS are the SECTIONS of the page
		# dict VALUES are the FIELDS UNDER that SECTION
	fieldsets = (
		(None, {'fields': ('email', 'password', 'first_name', 'last_name', 'date_joined', 'year_in_school')}),
		('Permissions', {'fields': ('is_staff', 'is_active')}),
		('Membership', {'fields': ('is_eboard', 'position', 'membership_points', 'membership_tier')})
	)

	# these are the fields that will display when you CREATE a user from admin page
		# dict KEYS are the SECTIONS of the page
		# dict VALUES are the FIELDS UNDER that SECTION
	add_fieldsets = ( 
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 
			'is_staff', 'is_active', 'date_joined', 'year_in_school', 'is_eboard', 'position', 
			'membership_points', 'membership_tier')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event)
admin.site.register(Meeting)