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
    url(r'^', include('myApi.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]