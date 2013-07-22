from django.contrib import admin
from myproject.models import *

class ResearchersAdmin(admin.ModelAdmin):

    list_display = ('name',)

class ResearchAdmin(admin.ModelAdmin):

    list_display = ('name',)
    prepopulated_fields={'slug': ('name',),}


class GraphAdmin(admin.ModelAdmin):

    search_fields = ['name']
    list_display = ('name', 'type')
    list_filter = ('research', 'subject',)
    prepopulated_fields={'slug': ('name','type',),}

class SubjectAdmin(admin.ModelAdmin):

    list_display = ('short_name',)

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Researchers, ResearchersAdmin)
admin.site.register(Graph, GraphAdmin)
