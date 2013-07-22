from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from myproject.views import research, home, list_objects, single, contact, subject, all_data, all_researcher, all_graphs_from_research
from django.contrib import admin
from myproject.settings import MEDIA_ROOT
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    url(r'^$', 'myproject.views.weather_chart_view', name='home'),
    url(r'^home/search/$', include('haystack.urls')),
    url(r'^about/', direct_to_template, {'template':'static-page.html'}), 
    url(r'^project/', direct_to_template, {'template':'project.html'}), 
    url(r'^contact/', contact), 
    url(r'^single_data/', direct_to_template, {'template':'single-graph.html'}), 
    url(r'^subject/(?P<subject>\w+)/$', subject), 
    url(r'^subject/(?P<subject>\w+)/(?P<types>\w+)/$', list_objects), 
    url(r'^subject/(?P<subject>\w+)/(?P<types>\w+)/(?P<slug>.*)/$', single), 
    url(r'^home/all/(?P<types>.*)/$', all_data), 
    url(r'^home/graphs/(?P<slug>.*)/$', all_graphs_from_research), 
    url(r'^home/(?P<researcher>.*)/$', all_researcher), 
    url(r'^home/$', home),
    url(r'^test/$', direct_to_template, {'template': 'test.html'}), 
    url(r'^admin/', include(admin.site.urls)),
)
