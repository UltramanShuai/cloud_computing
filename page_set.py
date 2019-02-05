# _*_coding:utf-8_*_
# Author   : Leo
# Time     : 20/01/2019
import json, storage
from google.cloud import bigquery


# def get_indicator():
#     with open("condition.json", "r") as f:
#         data = json.load(f)
#
#     return sorted([x["indicator_name"] for x in data])


def get_indicator():
    query_job = bigquery.Client().query("""select distinct indicator_name
    from `bigquery-public-data.world_bank_health_population.health_nutrition_population`""")  # API request
    return sorted([row.indicator_name for row in query_job.result()])
