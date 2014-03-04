import sys
import requests
import redis
import json
import time
from operator import itemgetter

redis = redis.StrictRedis(host='localhost', port=6379, db=0)

client_id = "XNEAXLMICZQF1OW0EN5ZQHK0Y5JLOGJ4UZGPVX0J4O13UMXZ"
client_secret= "ZILAWJKPX5WOOMSX4OMCAQNWXQQVORBGN1SFT2X14FFX4313"

results = []
venues_master = {}
specials_master = {}

def process_search_response(category_id, response):
    venues = []
    if "venues" in response:
        venues = response["venues"] #search response
    elif "groups" in response:
        assert len(response["groups"]) == 1, "expected that groups contains only 1 entry! %s" % json.dumps(response)
        venues = [item["venue"] for item in response["groups"][0]["items"]] #explore response
    else:
        return
    if len(venues) == 0:
        return
    for venue in venues:
        if venue["id"] not in venues_master:
            venues_master[venue["id"]] = {"object": venue, "order": len(venues_master.keys()), "categories": [category_id]}
        else:
            venues_master[venue["id"]]["categories"].append(category_id)
        for special in venue["specials"]["items"]:
            if special["id"] not in specials_master:
                specials_master[special["id"]] = {"object": special, "order": len(specials_master.keys()), "venue": venue}

def print_venues(location, category_id):
    print location, " - ", category_id
    search_url = "https://api.foursquare.com/v2/venues/search?near=%s&client_id=%s&client_secret=%s&v=20140217&categoryId=%s&radius=10000&intent=checkin&limit=50" % (location.replace(" ", "%20"), client_id, client_secret, category_id)
    explore_url = "https://api.foursquare.com/v2/venues/explore?near=%s&client_id=%s&client_secret=%s&v=20140217&categoryId=%s&radius=100000&limit=50&specials=1" % (location.replace(" ", "%20"), client_id, client_secret, category_id)

    search_results = get_response(search_url)
    process_search_response(category_id, search_results["response"])

    explore_results = get_response(explore_url)
    process_search_response(category_id, explore_results["response"])

    results.append({
        "search" :
            {
                "url": search_url,
                "results":search_results
            },
        "explore" :
            {
                "url": explore_url,
                "results": explore_results
            },
    })

def get_response(url):
    """
        returns json
    """
    first = True
    response = redis.get(url)
    if not response:
        while(True):
            response = requests.get(url).content
            if "rate_limit_exceeded" in response or "Foursquare servers are experiencing problems" in response:
                if first:
                    time.sleep(1)
                else:
                    print "sleeping 10"
                    time.sleep(60)
                first = False
            else:
                break
        redis.set(url, response)
    return json.loads(response)

if __name__ == "__main__":
    #try:
    #    with open("foursquare_results.json", "r") as f:
    #        results = json.loads(f.read())
    #        for r in results:
    #            redis.set(r["search"]["url"], json.dumps(r["search"]["results"]))
    #            redis.set(r["explore"]["url"], json.dumps(r["explore"]["results"]))
    #        print "redis has been primed with cache"
    #except:
    #    results = []
    #results = []
    cities = json.loads(open("citypics.json","r").read())
    locations = []

    for city in cities[1:]:
        locations.append(city["fields"]["name"])

    #car, food
    categories = list(set(['4eb1c1623b7b52c0e1adc2ec', '4f04ae1f2fb6e1c99f3db0ba', '503288ae91d4c4b30a586d67','4bf58dd8d48988d1c8941735','4bf58dd8d48988d14e941735','4bf58dd8d48988d152941735','4bf58dd8d48988d107941735','4bf58dd8d48988d142941735','4bf58dd8d48988d169941735','52e81612bcbc57f1066b7a01','4bf58dd8d48988d1df931735','4bf58dd8d48988d179941735','4bf58dd8d48988d16a941735','52e928d0bcbc57f1066b7e97','52e81612bcbc57f1066b7a02','52e81612bcbc57f1066b79f1','4bf58dd8d48988d16b941735','4bf58dd8d48988d143941735','52e81612bcbc57f1066b7a0c','52e81612bcbc57f1066b79f4','4bf58dd8d48988d16c941735','4bf58dd8d48988d153941735','4bf58dd8d48988d128941735','4bf58dd8d48988d16d941735','4bf58dd8d48988d17a941735','52e81612bcbc57f1066b7a03','4bf58dd8d48988d144941735','5293a7d53cf9994f4e043a45','4bf58dd8d48988d145941735','4bf58dd8d48988d1e0931735','52e81612bcbc57f1066b7a00','52e81612bcbc57f1066b79f2','4bf58dd8d48988d154941735','4bf58dd8d48988d1bc941735','52f2ae52bcbc57f1066b8b81','4bf58dd8d48988d146941735','4bf58dd8d48988d1d0941735','4bf58dd8d48988d1f5931735','4bf58dd8d48988d147941735','4e0e22f5a56208c4ea9a85a0','4bf58dd8d48988d148941735','4bf58dd8d48988d108941735','4bf58dd8d48988d109941735','52e81612bcbc57f1066b7a05','4bf58dd8d48988d10a941735','4bf58dd8d48988d10b941735','4bf58dd8d48988d16e941735','4eb1bd1c3b7b55596b4a748f','4edd64a0c7ddd24ca188df1a','52e81612bcbc57f1066b7a09','4bf58dd8d48988d1cb941735','4bf58dd8d48988d10c941735','4d4ae6fc7a7b7dea34424761','4bf58dd8d48988d155941735','4bf58dd8d48988d10d941735','4c2cd86ed066bed06c3c5209','4bf58dd8d48988d10e941735','52e81612bcbc57f1066b79ff','52e81612bcbc57f1066b79fe','52e81612bcbc57f1066b79fb','4bf58dd8d48988d16f941735','52af0bd33cf9994f4e043bdd','52e81612bcbc57f1066b79fa','4bf58dd8d48988d1c9941735','4bf58dd8d48988d10f941735','4deefc054765f83613cdba6f','52e81612bcbc57f1066b7a06','4bf58dd8d48988d110941735','4bf58dd8d48988d111941735','52e81612bcbc57f1066b79fd','4bf58dd8d48988d112941735','4bf58dd8d48988d113941735','52e81612bcbc57f1066b79fc','4bf58dd8d48988d1be941735','4bf58dd8d48988d1bf941735','4bf58dd8d48988d156941735','4bf58dd8d48988d1c0941735','4bf58dd8d48988d1c1941735','4bf58dd8d48988d115941735','52e81612bcbc57f1066b79f9','4bf58dd8d48988d1c2941735','4eb1d5724b900d56c88a45fe','4bf58dd8d48988d1c3941735','4bf58dd8d48988d157941735','52e81612bcbc57f1066b79f8','52e81612bcbc57f1066b79f7','4eb1bfa43b7b52c0e1adc2e8','52e81612bcbc57f1066b7a0a','4bf58dd8d48988d1ca941735','52e81612bcbc57f1066b7a04','4def73e84765ae376e57713a','4bf58dd8d48988d1d1941735','4bf58dd8d48988d1c4941735','52960bac3cf9994f4e043ac4','5293a7563cf9994f4e043a44','4bf58dd8d48988d1bd941735','4bf58dd8d48988d1c5941735','4bf58dd8d48988d1c6941735','4bf58dd8d48988d1ce941735','4bf58dd8d48988d1c7941735','4bf58dd8d48988d1dd931735','4bf58dd8d48988d1cd941735','4bf58dd8d48988d14f941735','52e81612bcbc57f1066b79f3','4bf58dd8d48988d150941735','4bf58dd8d48988d1cc941735','4bf58dd8d48988d1d2941735','4bf58dd8d48988d158941735','4bf58dd8d48988d151941735','4bf58dd8d48988d1db931735','52e928d0bcbc57f1066b7e98','4bf58dd8d48988d1dc931735','4bf58dd8d48988d149941735','52af39fb3cf9994f4e043be9','4f04af1f2fb6e1c99f3db0bb','52e928d0bcbc57f1066b7e96','4bf58dd8d48988d1d3941735','4bf58dd8d48988d14a941735','4bf58dd8d48988d14b941735','4bf58dd8d48988d14c941735','512e7cae91d4cbb4e5efe0af','4bf58dd8d48988d11d951735','4bf58dd8d48988d11e951735','4bf58dd8d48988d1fa941735','4bf58dd8d48988d10e951735','4bf58dd8d48988d120951735','4bf58dd8d48988d1f5941735','4bf58dd8d48988d118951735','50aa9e744b90af0d42d5de0e','4bf58dd8d48988d186941735','52f2ab2ebcbc57f1066b8b45','52f2ab2ebcbc57f1066b8b46','4bf58dd8d48988d119951735', '5294c7523cf9994f4e043a62','52939ae13cf9994f4e043a3b','52939a9e3cf9994f4e043a36','52939a643cf9994f4e043a33','5294c55c3cf9994f4e043a61','52939af83cf9994f4e043a3d','52939aed3cf9994f4e043a3c','52939aae3cf9994f4e043a37','52939ab93cf9994f4e043a38','5294cbda3cf9994f4e043a63','52939ac53cf9994f4e043a39','52939ad03cf9994f4e043a3a','52939a7d3cf9994f4e043a34','52af3a5e3cf9994f4e043bea','52af3a723cf9994f4e043bec','52af3a7c3cf9994f4e043bed','52af3a673cf9994f4e043beb','52af3a903cf9994f4e043bee','52af3a9f3cf9994f4e043bef','52af3aaa3cf9994f4e043bf0','52af3ab53cf9994f4e043bf1','52af3abe3cf9994f4e043bf2','52af3ac83cf9994f4e043bf3','52af3ad23cf9994f4e043bf4','52af3add3cf9994f4e043bf5','52af3af23cf9994f4e043bf7','52af3ae63cf9994f4e043bf6','52af3afc3cf9994f4e043bf8','52af3b053cf9994f4e043bf9','52af3b213cf9994f4e043bfa','52af3b293cf9994f4e043bfb','52af3b343cf9994f4e043bfc','52af3b3b3cf9994f4e043bfd','52af3b463cf9994f4e043bfe','52af3b633cf9994f4e043c01','52af3b513cf9994f4e043bff','52af3b593cf9994f4e043c00','52af3b6e3cf9994f4e043c02','52af3b773cf9994f4e043c03','52af3b813cf9994f4e043c04','52af3b893cf9994f4e043c05','52af3b913cf9994f4e043c06','52af3b9a3cf9994f4e043c07','52af3ba23cf9994f4e043c08','52960eda3cf9994f4e043ac9','52960eda3cf9994f4e043acb','52960eda3cf9994f4e043aca','52960eda3cf9994f4e043ac7','52960eda3cf9994f4e043ac8','52960eda3cf9994f4e043acc','52960eda3cf9994f4e043ac5','52960eda3cf9994f4e043ac6','52939a8c3cf9994f4e043a35','52e928d0bcbc57f1066b7e9d','52e928d0bcbc57f1066b7e9c','4bf58dd8d48988d14d941735','5283c7b4e4b094cb91ec88d8','5283c7b4e4b094cb91ec88d9','5283c7b4e4b094cb91ec88d4','5283c7b4e4b094cb91ec88d7','5283c7b4e4b094cb91ec88db','5283c7b4e4b094cb91ec88d6','5283c7b4e4b094cb91ec88d5','5283c7b4e4b094cb91ec88da','52e928d0bcbc57f1066b7e9a','52e928d0bcbc57f1066b7e9b', '4bf58dd8d48988d102951735','4bf58dd8d48988d104951735','4bf58dd8d48988d105951735','4bf58dd8d48988d109951735','4bf58dd8d48988d106951735','4bf58dd8d48988d107951735','4bf58dd8d48988d108951735','4bf58dd8d48988d103951735']))

    for location in locations:
        for category in categories:
            print_venues(location, category)

    #for venue in sorted(venues_master.values(), key=itemgetter("order")):
    #    categories = venue["categories"]
    #    venue = venue["object"]
    #    address = ""
    #    try:
    #        address = venue["location"]["address"]
    #    except: pass
    #    city = ""
    #    try:
    #        city = venue["location"]["city"]
    #    except: pass
    #    state = ""
    #    try:
    #        state = venue["location"]["state"]
    #    except: pass
    #    postalCode = ""
    #    try:
    #        postalCode = venue["location"]["postalCode"]
    #    except: pass
    #    lat = ""
    #    lng = ""
    #    try:
    #        lat = venue["location"]["lat"]
    #        lng = venue["location"]["lng"]
    #    except: pass
    #    #print '"%s"|"%s"|"%s"|"%s"|"%s"|"%s"|"%s"|"%s"' % (venue["id"], venue["name"], address, city, state, postalCode, lat, lng)
    #    for category in categories:
    #        print '"%s"|"%s"|"%s"|"%s"' % (category, "", venue["id"], venue["name"])

    for special in sorted(specials_master.values(), key=itemgetter("order")):
        venue = special["venue"]
        special = special["object"]
        print '"%s"|"%s"|"%s"|"%s"' % (special["id"], special["message"], venue["id"], venue["name"])

    #f = open("foursquare_results.json", "w")
    #f.write(json.dumps(results))
