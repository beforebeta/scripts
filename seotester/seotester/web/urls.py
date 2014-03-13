from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from rest_framework import viewsets, routers
from django.contrib.auth.models import User, Group
from seotester.web.views import GroupViewSet, UserViewSet, CrawlList, CrawlDetail
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = patterns(
    'seotester.web.views',
    url(r'^$', 'index', name='index'),
    url(r'^check_links/(?P<crawl_id>[0-9]+)/(?P<status_code>[0-9]+)$', 'check_links', name='check_links'),
    url(r'^link/(?P<link_id>[0-9]+)$', 'link_detail', name='link_detail'),
    url(r'^crawl/(?P<crawl_id>[0-9]+)$', 'crawl_detail', name='crawl_detail'),
    url(r'^crawl/(?P<crawl_id>[0-9]+)/links$', 'crawl_links', name='crawl_links'),
    url(r'^url/stats$', 'get_stats_for_url', name='get_stats_for_url'),
)

urlpatterns += patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

cbv_urlpatterns = patterns('',
    url(r'^crawls/$', CrawlList.as_view()),
    url(r'^crawls/(?P<pk>[0-9]+)/$', CrawlDetail.as_view(), name="crawl-detail"),
)

urlpatterns += format_suffix_patterns(cbv_urlpatterns)
