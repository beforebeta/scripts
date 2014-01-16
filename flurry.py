from dateutil.relativedelta import relativedelta
import requests
import datetime
import time
import smtplib
import json

ACCESS_CODE = 'RF8TYCVMKVWBZ6FCZ7TM'
API_KEY = 'VQNHJC57WHGP8MXYMWKN'

def get_app_metric(metric, start_date, end_date, group_by='DAYS'):
    time.sleep(1)
    url = 'http://api.flurry.com/appMetrics/%s?apiAccessCode=%s&apiKey=%s&startDate=%s&endDate=%s&country=US&groupBy=%s' \
          % (metric, ACCESS_CODE, API_KEY, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), group_by)
    return requests.get(url).content

def get_new_users(start_date, end_date, group_by='DAYS'):#group_by WEEKS, MONTHS
    return get_app_metric('NewUsers', start_date, end_date, group_by)

def get_active_users(start_date, end_date, group_by='DAYS'):
    return get_app_metric('ActiveUsers', start_date, end_date, group_by)

def get_event_info(event_name, start_date, end_date):
    time.sleep(1)
    url = "http://api.flurry.com/eventMetrics/Event?apiAccessCode=%s&apiKey=%s&startDate=%s&endDate=%s&eventName=%s" \
        % (ACCESS_CODE, API_KEY, start_date, end_date, event_name)
    return requests.get(url).content

def send_email(msg):
    _user="beforebetabot@gmail.com"
    _password='123dfvlabs'
    fromaddr = _user
    #toaddrs  = ['janto@digitalfirstventures.com','amrish@digitalfirstventures.com','amrish.singh@gmail.com', 'thomas.whyyou@ymail.com', 'elodieblakely@gmail.com']
    toaddrs  = ['amrish@digitalfirstventures.com','amrish.singh@gmail.com']
    username = _user
    password = _password

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def get_conv_rate(deal_stats, index):
    try:
        return float(deal_stats["day"][index]["@totalCount"])/float(deal_stats["day"][index]["@totalSessions"])
    except:
        return 0.0

today = datetime.date.today()
yesterday = today + relativedelta(days=-1)
day_before = yesterday + relativedelta(days=-1)

new_users = json.loads(get_new_users(day_before, today))
msg = "Subject:PushPenny Mobile App Stats\n\nPushPenny Mobile App Stats\n"
msg += "For more info go to: https://dev.flurry.com/customDashboard.do?dashboardId=22&projectID=423865\n"
msg += "username: amrish@digitalfirstventures.com\n"
msg += "password: 123dfvlabs\n\n\n"

msg += "New Users by Day\n"
msg += "----------------\n"
msg += "%s: %s\n" % (new_users["day"][-1]["@date"],new_users["day"][-1]["@value"])
msg += "%s: %s\n" % (new_users["day"][-2]["@date"],new_users["day"][-2]["@value"])
msg += "%s: %s\n" % (new_users["day"][-3]["@date"],new_users["day"][-3]["@value"])

active_users = json.loads(get_active_users(day_before, today))
msg += "\n\nDaily Active Users\n"
msg += "------------------\n"
msg += "%s: %s\n" % (active_users["day"][-1]["@date"],active_users["day"][-1]["@value"])
msg += "%s: %s\n" % (active_users["day"][-2]["@date"],active_users["day"][-2]["@value"])
msg += "%s: %s\n" % (active_users["day"][-3]["@date"],active_users["day"][-3]["@value"])

#print msg
get_deal_stats = json.loads(get_event_info('Action_GetDeal', day_before, today))
msg += "\n\nGet Deal Events\n"
msg += "---------------\n"
msg += "%s: Total=%s, Conversion Rate=%.2f\n" % (get_deal_stats["day"][-1]["@date"], get_deal_stats["day"][-1]["@totalCount"], get_conv_rate(get_deal_stats, -1))
msg += "%s: Total=%s, Conversion Rate=%.2f\n" % (get_deal_stats["day"][-2]["@date"], get_deal_stats["day"][-2]["@totalCount"], get_conv_rate(get_deal_stats, -2))
msg += "%s: Total=%s, Conversion Rate=%.2f\n" % (get_deal_stats["day"][-3]["@date"], get_deal_stats["day"][-3]["@totalCount"], get_conv_rate(get_deal_stats, -3))

send_email(msg)