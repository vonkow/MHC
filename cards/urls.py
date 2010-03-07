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
	(r'^show_card/(?P<setId>\d+)/$', 'showSetView'),
	(r'^show_card/(?P<setId>\d+)/(?P<cardId>\d+)/$', 'showCardView'),
)
