# _*_coding:utf-8_*_
# Author   : Leo
# Time     : 25/01/2019

import requests
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()


def get_country(code):
    r = requests.get('https://restcountries.eu/rest/v2/alpha/{0}'.format(code))
    # language
    r = r.json()
    try:
        langeuage = [x["name"] for x in r["languages"]]
        name = r["name"]
        # flag

        flag = r["flag"]

        # population
        population = r["population"]

        # region
        region = r["region"]

        capital = r["capital"]

        area = r["area"]
    except:
        pass

    return name, langeuage, region, capital, population, flag, area
