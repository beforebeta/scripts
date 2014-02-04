import sys, traceback
import requests
import threading

NUM_THREADS = 30

def print_stack_trace():
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60

f = open("urls_to_test.lines", "r")
results = open("results.csv","w")

links = [line.strip() for line in f.readlines()]

print len(links), "links"

results.write("URL,Final Status Code,Intermediate Status Code\n")

class Downloader(threading.Thread):
    def __init__(self, number):
        self.number = number
        threading.Thread.__init__(self)

    def run(self):
        try:
            while len(links):
                url = links.pop()
                try:
                    print self.number, url
                    r = requests.get(url)
                    results.write("%s,%s,%s\n" % (url, r.status_code, "-".join([str(h.status_code) for h in r.history])))
                except:
                    print_stack_trace()
        except:
            pass

threads = []
for i in range(NUM_THREADS):
    thread = Downloader(i)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

results.flush()
results.close()
print "done"