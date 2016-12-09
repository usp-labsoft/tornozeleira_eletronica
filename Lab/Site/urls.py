from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.pessoas_list),
    url(r'^pessoas/(?P<pk>[0-9]+)/$', views.pessoa_local),
]
