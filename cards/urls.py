from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('mhc.cards.views',
	(r'^$', 'showLogin'),
	(r'^register/$', 'newUser'),
	(r'^login/$', 'login'),
	(r'^logout/$', 'logout'),
	(r'^main/$', 'showSet'),
	(r'^send_results/$', 'processSet'),
	(r'^select_set/(?P<setNum>\d+)/$', 'selectSet'),
)
