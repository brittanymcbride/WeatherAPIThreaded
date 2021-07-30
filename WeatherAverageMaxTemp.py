import requests
import concurrent.futures
import statistics
from json.decoder import JSONDecodeError

#Calculate average max temperature for each API call
def get_average_max_temp(weatherUrl, timeout=10):
    try:
        response = requests.get(url=weatherUrl, timeout=timeout)
        
    except requests.exceptions.HTTPError as err_h:
        return "An Http Error occurred:" + repr(err_h)
    except requests.exceptions.ConnectionError as err_c:
        return "An Error Connecting to the API occurred:" + repr(err_c)
    except requests.exceptions.Timeout as err_t:
        return "A Timeout Error occurred:" + repr(err_t)
    except requests.exceptions.RequestException as err_:
        return "An Unknown Error occurred" + repr(err_)
    else:   
        try: 
            weather_=response.json()
        except JSONDecodeError as e_:
            return "An Unknown Error occurred" + repr(e_)
        else:
        #check that there is at least 1 day of temperatures
         assert len(weather_['consolidated_weather']) >= 1
         
         maxtemps = [i['max_temp'] for i in weather_['consolidated_weather']]
         
         # Validate that only numbers from MaxTemps used
         check_temps = [x for x in maxtemps if isinstance(x, (float,int))]
         
         #Calculate Average of Max Temperatures
         average_ = statistics.mean(check_temps)
        
         
    return weather_['title'] + " Average Max Temp: " + str(round(average_, 2))

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
