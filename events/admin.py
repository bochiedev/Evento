from django.contrib import admin
from events.models import Event

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue', 'date', 'created_by']
    list_filter = ['venue', 'date']


admin.site.register(Event, EventAdmin)
