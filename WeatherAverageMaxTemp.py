# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 20:58:09 2021

@author: Brittany McBride
"""
import requests
import concurrent.futures
import statistics

#Calculate average max temperature for each API call
def get_average_max_temp(weatherUrl, timeout=10):
    response = requests.get(url=weatherUrl, timeout=timeout)
    temps=response.json()
    maxtemps = [i['max_temp'] for i in temps['consolidated_weather']]
    average = statistics.mean(maxtemps)
    return temps['title'] + " Average Max Temp: " + str(round(average, 2))

#MetaWeather API URLs
urls = ['https://www.metaweather.com/api/location/2487610/', 
        'https://www.metaweather.com/api/location/2442047/', 
        'https://www.metaweather.com/api/location/2366355/']


with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for url in urls:
        futures.append(executor.submit(get_average_max_temp, weatherUrl=url))
    for future in concurrent.futures.as_completed(futures):
        try:
            data = future.result()
        except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
        else:
                print(data)
