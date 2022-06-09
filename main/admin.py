from django.contrib.admin import ModelAdmin, register
from .models import *
# Register your models here.
@register(NewUser)
class NewUser(ModelAdmin):
    list_display = ('username','phone_number', 'email', 'code')
@register(Reference)
class Reference(ModelAdmin):
    list_display = ('referance_id','ref_type', 'field1', 'field2','field3','field4','field5')
@register(DbInformation)
class DbInformation(ModelAdmin):
    list_display = ('client_id','referance_id')
@register(ClientIdMapping)
class ClientIdMapping(ModelAdmin):
    list_display = ('client_id','ethan_token')
@register(Tableau)
class Tableau(ModelAdmin):
    list_display = ('sitename','password','user_id')
@register(TableauConnection)
class TableauConnection(ModelAdmin):
    list_display = ('client_id','tableau_id')

# admin.site.register(Tableau)
# admin.site.register(TableauConnection)