import traceback
import uuid
from django.core.management import BaseCommand
import datetime

import requests
from seotester import print_stack_trace
from seotester.main.models import Crawl, CrawlQueue, CrawledLink, BackLink
from multiprocessing import Pool
from multiprocessing import Lock
from BeautifulSoup import BeautifulSoup
import urlparse

class Command(BaseCommand):

    def handle(self, *args, **options):
        assert len(args) == 1, "the root URL argument must be provided to start the crawl!"
        self.crawl(args[0])

    def crawl(self, root_url):
        started = datetime.datetime.now()
        crawl = Crawl(crawl_id=uuid.uuid4().hex, root_url=root_url, started=started, ended=started, status="started")
        try:
            crawl.robots_text = requests.get(urlparse.urljoin(root_url, "robots.txt")).content
        except:
            print_stack_trace()
        crawl.save()
        try:
            stats = {}
            stats["root_url"] = root_url
            CrawlQueue(crawl=crawl, url=root_url).save()
            self.begin_crawl(crawl)
            crawl.ended = datetime.datetime.now()
            crawl.status = "ended"
            crawl.save()
        except:
            print_stack_trace()
            crawl.ended = datetime.datetime.now()
            crawl.status = "exception"
            crawl.save()

    def begin_crawl(self, crawl):
        l = Lock()
        crawl_queued_links.lock = l
        #feeding the beast before the storm
        crawl_queued_links((0, crawl, True))
        while True:
            p = Pool(None, crawl_queued_links_init, [l])
            p.map(crawl_queued_links, [(i, crawl, False) for i in range(20)])
            #crawl_queue(crawl.id)
            p.close()
            p.join()
            p = None
            if CrawlQueue.objects.filter(crawl=crawl).count() <= 0:
                break #crawl ended

def crawl_queued_links(args):
    process_id, crawl, initial = args
    while True:
        crawled_link = None
        crawl_queued_links.lock.acquire()
        try:
            q = CrawlQueue.objects.filter(crawl=crawl)[0]
        except:
            crawl_queued_links.lock.release()
            break
        url = q.url
        print "%s:%s" % (str(process_id), url)
        q.delete()
        if CrawledLink.objects.link_already_crawled(crawl, url):
            crawl_queued_links.lock.release()
            continue
        else:
            crawled_link = CrawledLink(crawl=crawl, url=url, status_code=-1)
            crawled_link.save()
            crawl_queued_links.lock.release()
        try:
            crawl.add_message("Crawling %s" % url)
            r = requests.get(url=url, timeout=10)
            crawled_link.status_code = r.status_code
            crawled_link.contents = r.content
            crawled_link.elapsed = r.elapsed.total_seconds()
            crawled_link.save()
            soup = BeautifulSoup(crawled_link.contents)
            outgoing_links = []
            for a in soup.findAll("a"):
                link = urlparse.urljoin(crawl.root_url, a["href"])
                if link.startswith(crawl.root_url):
                    outgoing_links.append(link)
            outgoing_links = list(set(outgoing_links))
            for link in outgoing_links:
                CrawlQueue(crawl=crawl, url=link).save()
                try:
                    BackLink(crawl=crawl, url=link, backlink_url=url).save()
                except:
                    pass
        except:
            print_stack_trace()
            crawl.add_exception("Exception\n %s" % "".join(traceback.format_stack()))
        if initial:
            break

def crawl_queued_links_init(lock):
    crawl_queued_links.lock = lock

