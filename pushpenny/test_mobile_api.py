import requests
import smtplib
from collections import OrderedDict, Counter

top_50_us_cities_dict = OrderedDict([
    ("New York, NY", "40.75170,-73.99420"),
    ("Los Angeles, CA", "34.02000,-118.15300"),
    ("Chicago, IL", "41.87440,-87.63940"),
    ("Houston, TX", "29.75720,-95.36030"),
    ("Philadelphia, PA", "39.94940,-75.15580"),
    ("Phoenix, AZ", "33.45330,-112.07400"),
    ("San Antonio, TX", "29.42690,-98.48500"),
    ("San Diego, CA", "32.71470,-117.15600"),
    ("Dallas, TX", "32.78580,-96.79360"),
    ("San Jose, CA", "37.33780,-121.89000"),
    ("Austin, TX", "30.26920,-97.74360"),
    ("Jacksonville, FL", "30.32890,-81.66170"),
    ("Indianapolis, IN", "39.76860,-86.16280"),
    ("San Francisco, CA", "37.77750,-122.41100"),
    ("Columbus, OH", "39.96300,-83.00470"),
    ("Fort Worth, TX", "32.74860,-97.32890"),
    ("Charlotte, NC", "35.22890,-80.84580"),
    ("Detroit, MI", "42.33000,-83.04920"),
    ("El Paso, TX", "31.76000,-106.48600"),
    ("Memphis, TN", "35.14610,-90.05360"),
    ("Boston, MA", "42.35670,-71.05690"),
    ("Seattle, WA", "47.60890,-122.33700"),
    ("Denver, CO", "39.74940,-104.98900"),
    ("Washington, DC", "38.89750,-77.00920"),
    ("Nashville, TN", "36.15920,-86.78190"),
    ("Baltimore, MD", "39.29050,-76.61250"),
    ("Louisville, KY", "38.24640,-85.76360"),
    ("Portland, OR", "45.51830,-122.67600"),
    ("Oklahoma City, OK", "35.47390,-97.51780"),
    ("Milwaukee, WI", "43.03860,-87.90420"),
    ("Las Vegas, NV", "36.17220,-115.14400"),
    ("Albuquerque, NM", "35.08360,-106.65100"),
    ("Tucson, AZ", "32.22080,-110.96900"),
    ("Fresno, CA", "36.73670,-119.77000"),
    ("Sacramento, CA", "38.5556,-121.4689"),
    ("Long Beach, CA", "33.77060,-118.18800"),
    ("Kansas City, MO", "39.08220,-94.58890"),
    ("Mesa, AZ", "33.41500,-111.82800"),
    ("Virginia Beach, VA", "36.84670,-75.97500"),
    ("Atlanta, GA", "33.75280,-84.39360"),
    ("Colorado Springs, CO", "38.83530,-104.82100"),
    ("Raleigh, NC", "35.77720,-78.63920"),
    ("Omaha, NE", "41.26170,-95.93720"),
    ("Miami, FL", "25.77690,-80.19220"),
    ("Oakland, CA", "37.80080,-122.26500"),
    ("Tulsa, OK", "36.15330,-95.99280"),
    ("Minneapolis, MN", "44.98250,-93.26190"),
    ("Cleveland, OH", "41.49750,-81.69720"),
    ("Wichita, KS", "37.69170,-97.33780"),
    ("Arlington, TX", "32.73670,-97.11330"),
])

PUSHPENNY_API_URL = "http://api.pushpenny.com/v2/"
MIN_DEAL_QUANTITY = 100
MAX_CONSEC_DUPS = 2 # Must be >1
MAX_TOTAL_DUPS = 4

##################################################################################################
# Tests for '/deals' end point
##################################################################################################

request_parameters = {
        'per_page': 100,
        'radius': 100,
    }

def test_mobile_api_in_service(msg):
    api_response = fetch_api_response(request_parameters)
    if api_response.status_code == 200:
        msg += "> Responding :)\n\n"
    else:
        msg += "> NOT responding! :(\n\n"
    return msg

def test_enough_local_deals_available(msg):
    fail_count = 0
    fail_log = str()
    for name, lat_lng in top_50_us_cities_dict.iteritems():
        request_parameters['location'] = lat_lng
        api_response = fetch_api_response(request_parameters)
        is_pass, num_of_deals = check_deals_quantity_above_threshold(api_response, MIN_DEAL_QUANTITY)
        if is_pass:
            continue
        else:
            fail_log += "{} ({}): {} deals\n".format(name, lat_lng, num_of_deals)
            fail_count += 1
    if fail_count:
        msg += "> Following {} out of 50 cities failed :(\n"
        msg += fail_log
        msg += '\n'
    else:
        msg += "> All passed :)\n\n"
    return msg

def test_consec_dup_deals_minimized(msg):
    # Check only the first page in each city.
    for name, lat_lng in top_50_us_cities_dict.iteritems():
        request_parameters['location'] = lat_lng
        api_response = fetch_api_response(request_parameters)
        yield check_consec_dups_within_threshold, api_response, MAX_CONSEC_DUPS, name

def test_total_dup_deals_minimized():
    # Check only the first page in each city.
    for name, lat_lng in top_50_us_cities_dict.iteritems():
        request_parameters['location'] = lat_lng
        api_response = fetch_api_response(request_parameters)
        yield check_total_dups_within_threshold, api_response, MAX_TOTAL_DUPS, name

##################################################################################################
# Helper Methods
##################################################################################################

def fetch_api_response(request_parameters):
    return requests.get(PUSHPENNY_API_URL + 'deals', params=request_parameters)

def check_deals_quantity_above_threshold(api_response, minimum_threshold, reference_string=None):
    num_of_total_available = api_response.json()['query']['total']
    return (num_of_total_available >= minimum_threshold, num_of_total_available)

def check_consec_dups_within_threshold(api_response, maximum_threshold, reference_string=None):
    short_titles = [each['deal']['short_title'] for each in api_response.json()['deals']]
    allowed_consec_dups = (maximum_threshold - 1)

    consec_dups_detected = 0
    previous_deal_title = None
    for s in short_titles:
        if not previous_deal_title:
            previous_deal_title = s
            continue
        if s == previous_deal_title:
            consec_dups_detected += 1
            previous_deal_title = s
            if consec_dups_detected > allowed_consec_dups:
                break
        else:
            consec_dups_detected = 0
            previous_deal_title = s
    assert consec_dups_detected <= allowed_consec_dups

def check_total_dups_within_threshold(api_response, maximum_threshold, reference_string=None):
    short_titles = [each['deal']['short_title'] for each in api_response.json()['deals']]
    dup_deals_above_threshold = [k + " ->" + str(v) for k, v in Counter(short_titles).items() if v > maximum_threshold]
    assert len(dup_deals_above_threshold) == 0

def describe_section(label):
    section =  "-" * 30
    section += "\n"
    section += label
    section += "\n"
    return section

def send_email(msg):
    _user="beforebetabot@gmail.com"
    _password='123dfvlabs'
    fromaddr = _user
    # toaddrs  = ['janto@digitalfirstventures.com','amrish@digitalfirstventures.com','amrish.singh@gmail.com', 'thomas.whyyou@ymail.com', 'elodieblakely@gmail.com']
    toaddrs  = ['thomas.whyyou@outlook.com']
    username = _user
    password = _password

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

# send_email(msg)
msg =  "Subject:PushPenny Mobile API Check-ins\n\nPushPenny Mobile API Status\n\n"
msg += describe_section("MOBILE API SERVICE CHECK")
msg += test_mobile_api_in_service(msg)
msg += describe_section("DEAL VOLUME CHECK")
msg += "(Check at least {} deals available in target 50 cities)\n".format(MIN_DEAL_QUANTITY)
msg += test_enough_local_deals_available(msg)
msg += describe_section("DUPLICATES CHECK - CONSECUTIVE")
msg += "(Check no more than {} deals appearing back-to-back on 1st page of target 50 cities)\n".format(MAX_CONSEC_DUPS)
msg += test_consec_dup_deals_minimized(msg)
msg += describe_section("DUPLICATES CHECK - TOTAL")
msg += "(Check no more than {} deals appearing in total in target 50 cities)\n".format(MAX_CONSEC_DUPS)
print msg
# send_email(msg)

