from django.contrib import admin
from seotester.main.models import *

class CrawlAdmin(admin.ModelAdmin):
    search_fields = ('root_url', )
    list_display = ['root_url', 'started', 'ended', 'status', 'date_added']

class CrawlQueueAdmin(admin.ModelAdmin):
    pass

class CrawledLinkAdmin(admin.ModelAdmin):
    list_display = ['crawl', 'url', 'status_code', 'date_added']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['message', 'type', 'date_added']

class BackLinkAdmin(admin.ModelAdmin):
    search_fields = ["url"]
    list_display = ['crawl', 'url', 'backlink_url']

admin.site.register(Crawl, CrawlAdmin)
admin.site.register(CrawlQueue, CrawlQueueAdmin)
admin.site.register(CrawledLink, CrawledLinkAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(BackLink, BackLinkAdmin)