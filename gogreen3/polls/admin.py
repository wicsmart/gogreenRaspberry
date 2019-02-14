from django.contrib import admin

# Register your models here.
from .models import SenseIn, SenseOut, Acao, Status, Monitor, Setup, Log



class AcaoAdmin (admin.ModelAdmin):

    list_display = ['acao', 'created']
    search_fields = ['acao', 'created']

class StatusAdmin (admin.ModelAdmin):

    list_display = ['status', 'manual', 'local', 'created']
    search_fields = ['status', 'created']
    
class LogAdmin (admin.ModelAdmin):

    list_display = ['status', 'acao', 'created']
    search_fields = ['status', 'acao', 'created']

class SenseInAdmin (admin.ModelAdmin):

    list_display = ['temperatura', 'umidade', "luz", 'time']
    search_fields = ['temperatura', 'umidade', 'time']


class SenseOutAdmin(admin.ModelAdmin):

        list_display = ['temperatura', 'umidade', "luz", 'time']
        search_fields = ['temperatura', 'umidade', 'T=time']
        
class MonitorAdmin(admin.ModelAdmin):

        list_display = ['log', 'created']
        search_fields = ['log', 'created']
      
class SetupAdmin(admin.ModelAdmin):
	
		list_display = ['created','temp_min','temp_max']
		search_fields = ['created','temp_min','temp_max']

admin.site.register(SenseIn, SenseInAdmin)

admin.site.register(SenseOut, SenseOutAdmin)

admin.site.register(Acao, AcaoAdmin)

admin.site.register(Status, StatusAdmin)

admin.site.register(Log, LogAdmin)

admin.site.register(Setup, SetupAdmin)


