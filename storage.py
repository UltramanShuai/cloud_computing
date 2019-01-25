#_*_coding:utf-8_*_
# Author   : Leo
# Time     : 23/01/2019
from google.cloud import storage,bigquery
# import pandas as pd
# import shlex
from io import BytesIO
global client,bucket

import csv

# import requests_toolbelt.adapters.appengine
#
# requests_toolbelt.adapters.appengine.monkeypatch()

client = storage.Client()
bucket = client.get_bucket('s3596156-assignment2')




def get_geo(indecator):

    # client = bigquery.Client()

    query_job = bigquery.Client().query("""select country_name,t2.two_alpha_code, year,value
    from `bigquery-public-data.world_bank_health_population.health_nutrition_population` as t1 join
    `bigquery-public-data.world_bank_health_population.country_summary` as t2 on (t1.country_code=t2.country_code)
    where indicator_name='{0}' and upper(country_name)!='WORLD'""".format(indecator))  # API request

    string="\r\n".join(["\"{0}\",\"{1}\",{2},{3} ".format(row.country_name.replace(u"\u2018", "").replace(u"\u2019", "'").strip(),
                                                             row.two_alpha_code ,
                                                             row.year,
                                                             row.value)
                        for row in query_job.result()])

    filename=indecator.strip().replace(" ","_")+".csv"

    modify_bucket(filename, string)



# def read_bucket(indecator):
#     filename = indecator.strip().replace(" ", "_") + ".csv"
#     blob = bucket.get_blob(filename)
#     try:
#         return pd.read_csv(BytesIO(blob.download_as_string()), names=["country_name","country_code","year", "value"])
#     except:
#         get_geo(indecator)
#         blob = bucket.get_blob(filename)
#         return pd.read_csv(BytesIO(blob.download_as_string()), names=["country_name","country_code","year", "value"])


def modify_bucket(filename,text):
    try:
        blob = bucket.get_blob(filename)
        blob.upload_from_string(text)
    except:
        blob = bucket.blob(filename)
        blob.upload_from_string(text)



# data=read_bucket("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)".strip().replace(" ","_")+".csv")
# print len(data)
# print data.info()
#
# print "独有值:"
# print data["year"].unique()
#
# print "描述"
# print data.describe()
#
#
# print data.iloc[data["value"].idxmax()]
# def get_statistic(indecator):
#     # filename = indecator.strip().replace(" ", "_") + ".csv"
#     data=read_bucket(indecator)
#     max_year=data["year"].max()
#     min_year=data["year"].min()
#     max_value=max(data["value"])
#     min_value = min(data["value"])
#     std_value=data["value"].std()
#     max_value_item=data.iloc[data["value"].idxmax()].values
#     min_value_item=data.iloc[data["value"].idxmin()].values
#     unique_year=data["year"].unique()
#     unique_country=sorted(data["country_name"].unique())
#     country_number =len(unique_country)
#     range_year="Data avaliable from "+str(data["year"].min())+" to "+str(data["year"].max())
#     return country_number,max_year,min_year,max_value,min_value,std_value,max_value_item,min_value_item,unique_year,unique_country,range_year
#
# def get_particular_year(indecator,year):
#     data = read_bucket(indecator)
#     data = data[data["year"] == year][["country_code", "value"]].values.tolist()
#     data.insert(0, ["Country", "Value"])
#     return data
#
#
# def get_particular_country(indecator,country):
#     data = read_bucket(indecator)
#     data = data[data["country_name"]==country][["year","value"]]
#     data["year"]=data["year"].astype(str)
#     return data.values.tolist()
#
# def get_all_country(indecator):
#     data = read_bucket(indecator)
#     data=pd.DataFrame({'mean':data.groupby("year")["value"].mean()})
#     # return zip(year,value)
#     return [[str(x[0]).rstrip("L"),x[1][0]] for x in zip(data.index,data.values)]
# print get_statistic("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)")

# print get_particular_year("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)",2005)

# print get_particular_country("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)","Tanzania ")

# print get_all_country("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)")

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

# print get_statistic_new("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)")
# print get_statistic("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)")

def get_particular_year_new(indecator,year):
    data = read_bucket_new(indecator)
    data = csv.reader(data)
    data = [row for row in data]
    data=[[row[1],float(row[3])] for row in data if row[2]==str(year)]
    data.insert(0, ["Country", "Value"])
    return data

# print get_particular_year("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)",2005)
# print get_particular_year_new("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)",2005)

def get_particular_country_new(indecator,country):
    data = read_bucket_new(indecator)
    data = csv.reader(data)
    data = [row for row in data]
    return ([[row[2],float(row[3])] for row in data if row[0]==country],[row[1] for row in data if row[0]==country][0])

# print get_particular_country("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)","Tanzania")
# print get_particular_country_new("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)","Tanzania")[1]



def get_all_country_new(indecator):
    data = read_bucket_new(indecator)
    data = csv.reader(data)
    data = [row for row in data]
    list=[]
    for year in get_statistic_new(indecator)[-3]:
        values=[float(row[3]) for row in data if row[2]==year]
        list.append([year,sum(values)/len(values)])

    return list


# print get_all_country("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)")
# print get_all_country_new("% of females ages 15-49 having comprehensive correct knowledge about HIV (2 prevent ways and reject 3 misconceptions)")
