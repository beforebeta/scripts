from multiprocessing import Pool
import sys, traceback
import requests
from xml.dom import minidom

sitemap_url = "http://pushpenny.com/sitemap.xml"

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def parse_sitemap(xml_contents):
    xmldoc = minidom.parseString(xml_contents)
    locs = xmldoc.getElementsByTagName('loc')
    urls = []
    for loc in locs:
        urls.append(loc.firstChild.nodeValue)
    return urls

def test_sitemap():
    urls = parse_sitemap(requests.get(sitemap_url).content)
    test_urls = []
    for url in urls:
        test_urls.extend(parse_sitemap(requests.get(url).content))
    return test_urls

def print_stack_trace():
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60

def test_link_for_301(link):
    try:
        r = requests.get(link)
        if r.status_code != 200:
            print r.status_code, link
        if r.history and 301 not in [h.status_code for h in r.history]:
            print [h.status_code for h in r.history], link
    except:
        print link
        print_stack_trace()

if __name__ == "__main__":
    test_urls = test_sitemap()
    p = Pool(50)
    p.map(test_link_for_301, test_urls)
