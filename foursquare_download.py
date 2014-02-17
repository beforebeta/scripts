import sys

print sys.argv[0]

def print_venues(location):
    url = "https://api.foursquare.com/v2/venues/search?near=%s&oauth_token=KQBEDBATNE0EAYDDNEWRDNH5A1AACZXUZ33DQSBXGRNAUVLA&v=20140217&categoryId=4eb1c1623b7b52c0e1adc2ec&radius=10000&intent=checkin&limit=50" % location.replace(" ","%20")
    r=requests.get(url).json()

