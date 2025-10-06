from django.contrib import admin

# Register your models here.

from . models import Record,TicketType

admin.site.register(Record)
admin.site.register(TicketType)