from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _


class FlatPageAdmin(FlatPageAdmin):
	fieldset = (
		(None, {'fields': ('url', 'title', 'content', 'sites')}),
		(_('Advanced options'),{
			'classes': ('collapse',),
			'fields': (
				'enable_comments',
				'registration_equired',
				'template_name',
			),
		}),
	)


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)