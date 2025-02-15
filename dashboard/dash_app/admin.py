from django.contrib import admin
from .models import Data_table
# Register your models here.
class Data_tableAdmin(admin.ModelAdmin):
    list_display=['intensity','topic' , 'relevance','likelihood','country','start_year','region']
    list_filter =('end_year','topic','country','sector','region','pestle','source','country' )
    ordering =('intensity',)
    search_fields=('country',)
    list_per_page=50
admin.site.register(Data_table,Data_tableAdmin)