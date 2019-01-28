#_*_coding:utf-8_*_
# Author   : Leo
# Time     : 23/01/2019
from google.cloud import storage,bigquery
import csv
import requests_toolbelt.adapters.appengine
global client,bucket
requests_toolbelt.adapters.appengine.monkeypatch()

client = storage.Client()
bucket = client.get_bucket('{Your bucket id}')




def get_geo(indecator):
    query_job = bigquery.Client().query("""select country_name,t2.two_alpha_code, year,value
    from `bigquery-public-data.world_bank_health_population.health_nutrition_population` as t1 join
    `bigquery-public-data.world_bank_health_population.country_summary` as t2 on (t1.country_code=t2.country_code)
    where indicator_name="{0}" and upper(country_name)!='WORLD'""".format(indecator))  # API request
    string="\r\n".join(["\"{0}\",\"{1}\",{2},{3} ".format(row.country_name.replace(u"\u2018", "").replace(u"\u2019", "'").strip(),
                                                             row.two_alpha_code ,
                                                             row.year,
                                                             row.value)
                        for row in query_job.result()])

    filename=indecator.strip().replace(" ","_")+".csv"

    modify_bucket(filename, string)




def modify_bucket(filename,text):
    global client, bucket
    try:
        blob = bucket.get_blob(filename)
        blob.upload_from_string(text)
    except:
        blob = bucket.blob(filename)
        blob.upload_from_string(text)



def read_bucket_new(indecator):
    filename = indecator.strip().replace(" ", "_") + ".csv"
    blob = bucket.get_blob(filename)
    try:
        return blob.download_as_string().split("\r\n")
    except:
        get_geo(indecator)
        blob = bucket.get_blob(filename)
        return blob.download_as_string().split("\r\n")


# import csv
def get_statistic_new(indecator):
    data = read_bucket_new(indecator)
    data=csv.reader(data)
    data=[row for row in data]
    print data
    unique_year=sorted(list(set([row[2] for row in data])))
    unique_country=sorted(list(set([row[0] for row in data])))
    country_number = len(sorted(list(set([row[0] for row in data]))))
    max_value=max([float(row[3]) for row in data])
    min_value = min([float(row[3]) for row in data])
    max_year=max([int(row[2]) for row in data])
    min_year=min([int(row[2]) for row in data])
    max_value_item=data[[float(row[3]) for row in data].index(max_value)]
    min_value_item=data[[float(row[3]) for row in data].index(min_value)]
    range_year = "Data avaliable from " + str(min_year) + " to " + str(max_year)
    return country_number,max_year,min_year,max_value,min_value,min_value,max_value_item,min_value_item,unique_year,unique_country,range_year


def get_particular_year_new(indecator,year):
    data = read_bucket_new(indecator)
    data = csv.reader(data)
    data = [row for row in data]
    data=[[row[1],float(row[3])] for row in data if row[2]==str(year)]
    data.insert(0, ["Country", "Value"])
    return data

def get_particular_country_new(indecator,country):
    data = read_bucket_new(indecator)
    data = csv.reader(data)
    data = [row for row in data]
    return ([[row[2],float(row[3])] for row in data if row[0]==country],[row[1] for row in data if row[0]==country][0])


def get_all_country_new(indecator):
    data = read_bucket_new(indecator)
    data = csv.reader(data)
    data = [row for row in data]
    list=[]
    for year in get_statistic_new(indecator)[-3]:
        values=[float(row[3]) for row in data if row[2]==year]
        list.append([year,sum(values)/len(values)])

    return list

