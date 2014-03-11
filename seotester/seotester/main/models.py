import datetime
from BeautifulSoup import BeautifulSoup
from django.db import models
from picklefield.fields import PickledObjectField
from model_utils import Choices
import hashlib
import json
from django.utils import encoding
from seotester import print_stack_trace


class Message(models.Model):
    MESSAGE_TYPES = Choices(
        ("exception", "exception"),
        ("info", "info"),
    )
    crawl = models.ForeignKey("Crawl")
    message = models.TextField()
    type = models.CharField(max_length=50, choices=MESSAGE_TYPES, default=MESSAGE_TYPES.info)
    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

# Create your models here.
class Crawl(models.Model):
    crawl_id = models.CharField(max_length=32)
    root_url = models.TextField()
    robots_text = models.TextField(default="")
    stats = PickledObjectField(default={})
    stats_json = models.TextField(default="")
    started = models.DateTimeField(blank=True, null=True)
    ended = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default="started")
    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    root_url_255 = models.CharField(max_length=255, db_index=True)
    def save(self, *args, **kwargs):
        self.root_url_255 = self.root_url[:255]
        self.stats_json = json.dumps(self.stats)
        super(Crawl, self).save(*args, **kwargs)

    def add_message(self, message_text, type=Message.MESSAGE_TYPES.info):
        Message(crawl=self, message=message_text, type=type).save()

    def add_exception(self, message_text):
        self.add_message(message_text=message_text, type=Message.MESSAGE_TYPES.exception)

    def get_404_links(self):
        return self.crawledlink_set.filter(status_code=404)

    def generate_stats(self):
        self.stats = {}
        self.stats["total_links"] = self.crawledlink_set.all().count()
        self.stats["total_200_links"] = self.crawledlink_set.filter(status_code=200).count()
        self.stats["total_404_links"] = self.crawledlink_set.filter(status_code=404).count()
        self.stats["total_500_links"] = self.crawledlink_set.filter(status_code=500).count()

        self.stats["response_times"] = []
        #create histogram of response times
        for i in range(13):
            min = i
            max = 0
            max_str = ""
            if i == 13:
                max = 9999
                max_str = "12+"
            else:
                max = i+1
                max_str = str(i+1)
            self.stats["response_times"].append({
                "interval": "%s-%s" % (str(i), max_str),
                "frequency": self.crawledlink_set.filter(elapsed__gte=i, elapsed__lt=max).count()
            })

        self.save()

    class Meta:
        ordering = ['-date_added']

class CrawlQueue(models.Model):
    crawl = models.ForeignKey(Crawl)
    url = models.TextField()

    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

class CrawledLinkManager(models.Manager):

    def link_already_crawled(self, crawl, url):
        url_255 = url[:255]
        if self.filter(crawl=crawl, url_255=url_255).exists():
            return True
        else:
            return False

class CrawledLink(models.Model):
    crawl = models.ForeignKey(Crawl)
    url = models.TextField()
    status_code = models.IntegerField()
    elapsed = models.FloatField(default=0)
    contents = models.TextField(blank=True, null=True)
    history = PickledObjectField(default={})

    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    objects = CrawledLinkManager()

    contents_hash = models.CharField(max_length=255, blank=True, null=True)
    url_255 = models.CharField(max_length=255, db_index=True)
    num_all_outbound_links = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.url_255 = self.url[:255]
        if self.contents:
            self.contents = encoding.smart_str(self.contents, encoding='ascii', errors='ignore')
            self.contents_hash = hashlib.sha224(self.contents).hexdigest()
            self.num_all_outbound_links = len(BeautifulSoup(self.contents).findAll("a"))
        else:
            self.num_all_outbound_links = 0
        super(CrawledLink, self).save(*args, **kwargs)

    def content_length(self):
        return len(self.contents) if self.contents else 0

    def backlinks(self):
        return BackLink.objects.filter(crawl_id=self.crawl_id, url_255=self.url_255)

class BackLink(models.Model):
    crawl = models.ForeignKey(Crawl)
    url = models.TextField()
    backlink_url = models.TextField()

    url_255 = models.CharField(max_length=255, db_index=True)
    backlink_url_255 = models.CharField(max_length=255, db_index=True)

    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    class Meta:
        unique_together = ("crawl", "url_255", "backlink_url_255")

    def save(self, *args, **kwargs):
        self.url_255 = self.url[:255]
        self.backlink_url_255 = self.backlink_url[:255]
        super(BackLink, self).save(*args, **kwargs)

    #def backlink_url_status_code(self):
    #    try:
    #        return CrawledLink.objects.get(crawl_id=self.crawl_id, url_255=self.backlink_url_255).status_code
    #    except:
    #        print_stack_trace()
    #        return -1

    def backlink_url_crawled_link_id(self):
        try:
            return self.crawl.crawledlink_set.get(url_255=self.backlink_url_255).id
        except:
            print_stack_trace()
            return -1
