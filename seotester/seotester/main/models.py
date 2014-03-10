import datetime
from django.db import models
from picklefield.fields import PickledObjectField
from model_utils import Choices
import hashlib

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
    started = models.DateTimeField(blank=True, null=True)
    ended = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default="started")
    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    root_url_255 = models.CharField(max_length=255, db_index=True)
    def save(self, *args, **kwargs):
        self.root_url_255 = self.root_url[:255]
        super(Crawl, self).save(*args, **kwargs)

    def add_message(self, message_text, type=Message.MESSAGE_TYPES.info):
        Message(crawl=self, message=message_text, type=type).save()

    def add_exception(self, message_text):
        self.add_message(message_text=message_text, type=Message.MESSAGE_TYPES.exception)

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
    status_code = models.CharField(max_length=10)
    elapsed = models.FloatField()
    contents = models.TextField(blank=True, null=True)
    history = PickledObjectField(default={})

    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    objects = CrawledLinkManager()

    contents_hash = models.CharField(max_length=255, blank=True, null=True)
    url_255 = models.CharField(max_length=255, db_index=True)
    def save(self, *args, **kwargs):
        self.url_255 = self.url[:255]
        if self.contents:
            self.contents = self.contents.encode('ascii', 'xmlcharrefreplace')
            self.contents_hash = hashlib.sha224(self.contents).hexdigest()
        super(CrawledLink, self).save(*args, **kwargs)

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
