from multiprocessing import Pool
import sys, traceback
import requests

def print_stack_trace():
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60

#p = Pool(5)
#def f(x):
#    return x*x
#
#p.map(f, [1,2,3])

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
    f = open("links.txt","r")
    lines = [line.strip() for line in f.readlines()]
    p = Pool(50)
    p.map(test_link_for_301, lines)
