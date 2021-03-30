import requests
import datetime as dt
import json
import pandas as pd

token= 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImM1MzQ3MWM0YmEyYjU4ZjUyNDJkYWY1YWYzZWM0MDJkZGJmM2I4ZTMyZWFkZmUwZThiNzM4YTUyOGE5YzFlNDk1MGYzYzk3MDhlOGU1NDg2In0.eyJhdWQiOiIyIiwianRpIjoiYzUzNDcxYzRiYTJiNThmNTI0MmRhZjVhZjNlYzQwMmRkYmYzYjhlMzJlYWRmZTBlOGI3MzhhNTI4YTljMWU0OTUwZjNjOTcwOGU4ZTU0ODYiLCJpYXQiOjE2MTY5MjU3NzAsIm5iZiI6MTYxNjkyNTc3MCwiZXhwIjoxNjQ4NDYxNzcwLCJzdWIiOiIxMzMzIiwic2NvcGVzIjpbXX0.xoBUnQZXDNZExCofZmbBGLYZwDIBVNxq8-btV78qpc-UsDN-RIpzKDhTvsjeqkPrxp3YHJSfhcY7JFGN52ZeMVtseLn6x0qd9rzb09p9wxcmiu3tcGL5vkbA-8KhzGYxnY0W2bL8S6c-1K75omRKQjGTlfqa5thRNElbACaR4duk_d8WiO8SVOMkMv5PWxvXLY19KIc3tnTb7AxBE3dupktITQ2xKiVaAfI8RqY9P0ML4BlEeoifMUUkqpP8MN5RO8JNJ8O6GUwkhruUOfP45DRpMd8Uf8KjJg-1KVPBOav2UwzqpHnlWwqYp8gqiig_UeKHOUmzoI6211D5aD0W2PfJTi5Of9o58qhF1zKGgio5joQBG0ccxJ-L6OMoDHaug2EXnTBHbp_jWdDxm-klMsKx2ueyy0xVTa-n2YUPfpgYGiC1RdkANo7QQMfV4qSZmwI_keee2RVSCd3kz-RsQy95Fl7WYSn3Q0beZ8QZ1di8G9pP9XG0-PMhKY6W5t2dSiOcktXSk_Y8hcTGZCen45m8LFpu0wLaZPQ9QMDVUIAONIUSJ6nd4VvJmkMcoJ7J-zlbvRrvg30uUXsmQVhfnIYGtSUJnLJA34tVrXRb8KTF_7qD0kKtYfdRbPqzDo6YGirzWLzmWRXghdDHosIbu1NLCAGZkExR6QM8vdT90pw'

#lat long for BKK
lat =  13.753
long = 100.5
t = dt.datetime.now()+dt.timedelta(hours=1)

url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/at"

querystring = {
    "lat":"%s"%lat,
    "lon":"%s"%long,
    "fields":"tc,rh,rain",
    "date":"%s-%02d-%02d"%(t.year,t.month,t.day),
    "hour":"%s"%(t.hour),
    "duration":"1"
   }
headers = {
   'accept': "application/json",
   'authorization': "Bearer "+token,
    }

response = requests.request("GET", url, headers=headers, params=querystring)
d=json.loads(response.text)
d =  {
        'lat': d['WeatherForecasts'][0]['location']['lat'],
        'lon': d['WeatherForecasts'][0]['location']['lon'],
        'time': d['WeatherForecasts'][0]['forecasts'][0]['time'],
        'rh': d['WeatherForecasts'][0]['forecasts'][0]['data']['rh'],
        'tc': d['WeatherForecasts'][0]['forecasts'][0]['data']['tc'],
        'rain': d['WeatherForecasts'][0]['forecasts'][0]['data']['rain']
    }
df_out = pd.read_csv('tmd_hourly.csv')
df_out = df_out.drop(columns=['Unnamed: 0'])
df_out.loc[len(df_out)]=['BKK',d['time'],d['tc'],d['rh'],d['rain']]
df_out.to_csv('test.csv')