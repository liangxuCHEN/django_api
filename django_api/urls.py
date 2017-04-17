from django.conf.urls import url, include
from rest_framework import routers
from myApi import views

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)

"""
Wire up our API using automatic URL routing.
Additionally, we include login URLs for the browsable API.
The r'^api-auth/' part of pattern can actually be whatever URL you want to use.
The only restriction is that the included urls must use the 'rest_framework' namespace.
"""
urlpatterns = [
    url(r'^func_download$', views.func_download, name='func_download'),
    url(r'^$', views.home_page, name='home_page'),
    url(r'miao/', views.miao_page, name='miao'),
    url(r'miao/', views.logistics_page, name='logistics'),
    url(r'^api', include('myApi.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]