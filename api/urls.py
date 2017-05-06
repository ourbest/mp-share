from django.conf.urls import url

from api import views

app_name = 'api'
urlpatterns = [
    url(r'^go/(?P<page>.+)$', views.redirect),
    url(r'^pages$', views.pages),
    url(r'^share/(?P<page>.+)$', views.share_page),
    url(r'^auth$', views.wx_auth),
    url(r'^login$', views.login),
    url(r'^add_share$', views.add_share),
]
