from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('mhc.cards.views',
	(r'^$', 'showLogin'),
	(r'^login/$', 'login'),
	(r'^logout/$', 'logout'),
	(r'^main/$', 'showSet'),
	(r'^send_results/$', 'processSet'),

)
