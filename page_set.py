# _*_coding:utf-8_*_
# Author   : Leo
# Time     : 20/01/2019
import json
# from google.cloud import bigquery
# import storage
# import pandas as pd

def get_indicator():
    with open("condition.json", "r") as f:
        data = json.load(f)

    return sorted([x["indicator_name"] for x in data])


# def get_geo(indecator):
#     client = bigquery.Client()
#
#     query_job = client.query("""select country_name,t2.two_alpha_code, year,value
#     from `bigquery-public-data.world_bank_health_population.health_nutrition_population` as t1 join
#     `bigquery-public-data.world_bank_health_population.country_summary` as t2 on (t1.country_code=t2.country_code)
#     where indicator_name='{0}'""".format(indecator))  # API request
#
#     string="\r\n".join(["\"{0}\" ,\"{1}\" , {2},{3} ".format(row.country_name.replace(u"\u2018", "").replace(u"\u2019", "'"),
#                                                              row.two_alpha_code ,
#                                                              row.year,
#                                                              row.value)
#                         for row in query_job.result()])
#
#     filename=indecator.strip().replace(" ","_")+".csv"
#
#     storage.modify_bucket(filename, string)




# get_geo("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)")


# filename="% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)".strip().replace(" ","_")+".csv"

#print storage.read_bucket(filename)
# data=pd.Series(storage.read_bucket(filename).split("\r\n"))
# #
# # print data[:5]
# print filename
# print storage.read_bucket(filename)