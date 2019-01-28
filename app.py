# _*_coding:utf-8_*_
# Author   : Leo
# Time     : 23/01/2019
import json
import os

import country_info, user_action
import page_set, storage
import jinja2
from flask import Flask, render_template, request

app = Flask(__name__)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

global particular_index
particular_index = None


@app.route('/')
def home():
    indicators = page_set.get_indicator()
    user_action.track_action("login", 1, request.remote_addr, request.user_agent.platform)
    return render_template("home1.html", health_indexs=indicators)


@app.route('/aboutus')
def aboutus():
    return render_template("about.html")


@app.route('/about')
def about():
    return render_template("aboutdata.html")


@app.route('/action')
def action():
    return render_template("action.html", action=user_action.get_action()[0],
                           agent=json.dumps(user_action.get_action()[1]),
                           year=json.dumps(user_action.get_action()[2]),
                           geo=json.dumps(user_action.get_action()[3]),
                           hour=json.dumps(user_action.get_action()[4]),
                           city=json.dumps(user_action.get_action()[5]),
                           hel_ind=json.dumps(user_action.get_action()[6]))


@app.route('/particular_index', methods=['POST', "GET"])
def particular():
    global particular_index
    if request.method == "POST":
        particular_index = request.form.get("health_index")
    else:
        particular_index = particular_index

    statistics = storage.get_statistic_new(particular_index)
    series = storage.get_all_country_new(particular_index)
    user_action.track_action("check_indicator", particular_index, request.remote_addr, request.user_agent.platform)
    len_series = True
    if len(series) <= 1:
        len_series = False
    return render_template("second.html",
                           particular_index=particular_index,
                           countries=statistics[9],
                           years=statistics[8],
                           year_range=statistics[10],
                           country_number=statistics[0],
                           max_year=statistics[1],
                           min_year=statistics[2],
                           max_value=statistics[3],
                           min_value=statistics[4],
                           max_value_item=statistics[6],
                           min_value_item=statistics[7],
                           series=series, len_series=len_series
                           )


@app.route('/particular_index/particular_country', methods=['POST', "GET"])
def country():
    global particular_index
    form = request.form
    country = form.get("country")
    series, code = storage.get_particular_country_new(particular_index, country)
    info = country_info.get_country(code)
    len_series = True
    if len(series) <= 1:
        len_series = False
    user_action.track_action("check_country", str(code), request.remote_addr, request.user_agent.platform)

    return render_template("country.html",
                           series=json.dumps(series),
                           country=country.upper(),
                           indecator=particular_index.upper(),
                           name=info[0],
                           language=info[1],
                           region=info[2],
                           capital=info[3],
                           population=info[4],
                           flag=info[5],
                           area=info[6],
                           len_series=len_series)


@app.route('/particular_index/particular_year', methods=['POST'])
def year():
    global particular_index
    form = request.form
    year = form.get("year")
    user_action.track_action("check_year", year, request.remote_addr, request.user_agent.platform)
    return render_template("poly_map.html",
                           geo=json.dumps(storage.get_particular_year_new(particular_index, int(year))),
                           year=year,
                           be_chosen=particular_index)


if __name__ == '__main__':
    app.run()
