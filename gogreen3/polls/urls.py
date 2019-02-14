from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from polls.views import *

urlpatterns = [

    url(r'^sensein/$', SenseInList.as_view()),
    url(r'^senseinall/$', SenseInListOld.as_view()),
    url(r'^sensein/(?P<pk>[0-9]+)/$', SenseInDetail.as_view()),
    url(r'^lastsensein/$', lastSenseIn),

    url(r'^senseout/$', SenseOutList.as_view()),
    url(r'^senseout/(?P<pk>[0-9]+)/$', SenseOutDetail.as_view()),
    url(r'^lastsenseout/$', lastSenseOut),
    
	url(r'^setup/$', SenseOutList.as_view()),
    url(r'^acao/$', Acao.as_view()),
    url(r'^status/$', Status.as_view()),
    url(r'^freshData/$', freshData),
    url(r'^dadosPizza/$', dadosPizza),
    url(r'^log/$', Logs.as_view())
	

]
urlpatterns = format_suffix_patterns(urlpatterns)
