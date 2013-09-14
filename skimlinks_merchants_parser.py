###CHANGE THESE COOKIES WHENEVER YOU RUN THE SCRIPT###
cookies = dict(
    skimsession = 'a:5:{s:10:"session_id";s:32:"6d95d5450ffd00d09f5fa558cdfff798";s:10:"ip_address";s:13:"199.47.73.122";s:10:"user_agent";s:81:"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0";s:13:"last_activity";i:1378482050;s:9:"user_data";s:0:"";}d03a92a8ec0008d8dfa513de1c45cdff',
    PHPSESSID = 'sesbe5mdh2o92j3d96oejkm6d1')





import requests
from BeautifulSoup import BeautifulSoup

url="https://accounts.skimlinks.com/index.php?menu=merchant_search_results&page=%s"

test_url = url % 1

r = requests.get(test_url, cookies=cookies)
soup = BeautifulSoup(r.content)
pp_container = soup.findAll("div",{"id":"pp-container"})[0]
preferred_partners = []
for preferred_partner in pp_container.findAll("div", {"class":"pp-result is-sortable"}):
    try:
        data = {}
        content = preferred_partner.findAll("ul",{"class":"pp-merchant-countries"})[0]
        countries = []
        for li in content.findAll("li"):
            try:
                countries.append(li["class"].replace("pp-merchant-area","").strip())
            except: pass
        if len(countries) == 0:
            countries.append("us")
        data["countries"] = ";".join(countries)
        data["commission"] = "0"
        try:
            # print preferred_partner.findAll("span",{"class":"pp-commission-percentage"})
            data["commission"] = preferred_partner.findAll("span",{"class":"pp-commission-percentage"})[0].text
        except:
            pass
        try:
            data["domain"] = preferred_partner.findAll("a",{"class":"pp-domain"})[0].text
        except:
            data["domain"] = ""
        try:
            data["cpc"] = preferred_partner.findAll("li",{"class":"ecpc"})[0].findAll("span")[0].text.strip().replace("&#36;","").replace("*","")
        except:
            data["cpc"] = 0
        try:
            data["basket_size"] = preferred_partner.findAll("li",{"class":"basket_size"})[0].findAll("span")[0].text.strip().replace("&#36;","").replace("*","")
        except:
            data["basket_size"] = 0
        try:
            data["conv_rate"] = preferred_partner.findAll("li",{"class":"conv_rate last"})[0].findAll("span")[0].text.strip().replace("&#36;","").replace("*","")
        except:
            data["conv_rate"] = 0
        preferred_partners.append(data)
    except:
        pass

def _print_list_to_csv(_list):
    print ",".join(_list[0].keys())
    for item in _list:
        print ",".join(item.values())

print _print_list_to_csv(preferred_partners)
