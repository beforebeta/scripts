import json
from django.http import Http404, HttpResponse
from django.shortcuts import render
import requests
from seotester import print_stack_trace
from seotester.main.models import Crawl, CrawledLink

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from seotester.web.serializers import UserSerializer, GroupSerializer, CrawlSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CrawlList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        crawls = Crawl.objects.all()
        for c in crawls:
            c.stats_json = json.loads(c.stats_json)
        serializer = CrawlSerializer(crawls, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CrawlSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrawlDetail(APIView):
    """
    Retrieve, update or delete a Crawl instance.
    """
    def get_object(self, pk):
        try:
            return Crawl.objects.get(pk=pk)
        except Crawl.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Crawl = self.get_object(pk)
        serializer = CrawlSerializer(Crawl)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Crawl = self.get_object(pk)
        serializer = CrawlSerializer(Crawl, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Crawl = self.get_object(pk)
        Crawl.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def check_links(request, crawl_id, status_code):
    links = []
    for link in Crawl.objects.get(id=crawl_id).crawledlink_set.filter(status_code=status_code):
        links.append(
            {
                "url": link.url,
                "link_id": link.id,
                "status_code": requests.get(link.url, timeout=10).status_code
            }
        )
    return HttpResponse(json.dumps(links), content_type="application/json")

def index(request):
    context = {}
    context["latest_crawl"] = Crawl.objects.filter(status="ended").order_by("-date_added")[0]
    return render(request, 'crawl_detail.html', context)

def link_detail(request, link_id):
    context = {}
    link = CrawledLink.objects.get(id=link_id)
    context["link"] = link
    context["backlinks_info"] = []
    backlinks = link.backlinks()
    backlink_backlinkurls = list(set([b.backlink_url_255 for b in backlinks]))
    backlink_crawledlink_info = CrawledLink.objects.filter(crawl_id=link.crawl_id, url_255__in=backlink_backlinkurls)
    backlink_crawledlink_info = dict([(c.url, c) for c in backlink_crawledlink_info])
    for b in backlinks:
        info = {
            "backlink_id": b.id,
            "backlink_url": b.backlink_url
        }
        try:
            info["backlink_url_status_code"] = backlink_crawledlink_info[b.backlink_url].status_code
            info["backlink_url_crawled_link_id"] = backlink_crawledlink_info[b.backlink_url].id
        except:
            print_stack_trace()
            info["backlink_url_status_code"] = -1
            info["backlink_url_crawled_link_id"] = -1
        context["backlinks_info"].append(info)
    return render(request, 'link_detail.html', context)