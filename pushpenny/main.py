import requests
from xml.dom import minidom

sitemap_url = "http://s3.amazonaws.com/pushpenny/sitemap.xml"

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
    f = open("urls_to_test.lines","w")
    for u in test_urls:
        f.write(u)
        f.write("\n")
    f.close()

test_sitemap()