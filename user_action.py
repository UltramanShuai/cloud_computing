# _*_coding:utf-8_*_
# Author   : Leo
# Time     : 26/01/2019
import time
from collections import Counter

import requests
from google.appengine.ext import ndb
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()


class userAction1(ndb.Expando):
    user_ip = ndb.StringProperty()
    value = ndb.StringProperty()
    user_agent = ndb.StringProperty()
    action = ndb.StringProperty()


def track_action(action, value, user_ip, user_agent):
    sandy = userAction1()
    sandy.action = str(action)
    sandy.user_ip = str(user_ip)
    sandy.value = str(value)
    sandy.user_agent = str(user_agent)
    sandy.time = time.time()
    if str(action) == "login":

        sandy.city = get_city(str(user_ip))
    else:
        sandy.city = "None"
    sandy.put()


def get_action():
    country = userAction1.query(userAction1.action == "check_country")
    year = userAction1.query(userAction1.action == "check_year")
    login = userAction1.query(userAction1.action == "login")
    indicator = userAction1.query(userAction1.action == "check_indicator")

    country_info = [[x[0], x[1]] for x in Counter([x.value for x in country.fetch()]).items()]
    year_info = [[x[0], x[1]] for x in Counter([x.value for x in year.fetch()]).items()]
    agent_info = [[x[0], x[1]] for x in Counter([x.user_agent for x in login.fetch()]).items()]
    time_info = [[x[0], x[1]] for x in Counter([time.gmtime(x.time).tm_hour for x in login.fetch()]).items()]
    city = [[x[0], x[1]] for x in Counter([x.city for x in login.fetch()]).items()]
    item = sorted([[x[0], x[1]] for x in Counter([x.value for x in indicator.fetch()]).items()], key=lambda x: x[1],
                  reverse=True)
    if len(item) > 5:
        item = item[:5]

    # ip_info=[[x[0],x[1]] for x in Counter([get_city(str(x.user_ip)) for x in login.fetch()]).items()]

    time_info = sorted(time_info, key=lambda x: x[0])
    time_info = [[str(x[0]), x[1]] for x in time_info]
    year_info = sorted(year_info, key=lambda x: x[0])

    agent_info.insert(0, ["Agent", "frequency"])
    # Counter([x.user_agent for x in agent.fetch()]).items()
    return ("Welcome to users' action analysis!" + str(item),
            # return(str(country_info)+"---"+str(year_info)+"---"+str(agent_info)+"----"+str(time_info)+"---------"+str(city),
            agent_info,
            year_info,
            country_info,
            time_info,
            city,
            item)


def get_city(ip):
    return requests.get('https://www.iplocate.io/api/lookup/{0}'.format(ip)).json()["city"]
