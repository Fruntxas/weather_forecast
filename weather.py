# pylint: disable=missing-module-docstring

import sys
import requests

BASE_URI = "https://www.metaweather.com"


def search_city(query):
    '''City search while avoiding ambiguous answers'''
    url_city = BASE_URI + "/api/location/search/?query=" + query
    response = requests.get(url_city).json()
    if len(response) == 1:
        return response[0]
    if len(response) > 1:
        print(f"Your request is ambiguous. These are the {len(response)} possible cities.")
        for index, city in enumerate(response):
            print(f"{index + 1}. {city['title']}")
        index = int(input("Pick one accordiing to their number: ")) -1
        return response[index]
    if not response:
        print(f"No cities found containing {query}")
        return None
    return None

def weather_forecast(woeid):
    '''5-day (plus current) list of weather forecast for a given woeid'''
    url_forecast = BASE_URI + "/api/location/" + str(woeid)
    return requests.get(url_forecast).json()["consolidated_weather"]

def main():
    '''Ask for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)
    print(f"Here's the weather in {city['title']} for the next 5 days")
    woeid = city["woeid"]
    forecast = weather_forecast(woeid)
    for days in forecast:
        min_temp = round(days['min_temp'])
        max_temp = round(days['max_temp'])
        avg_temp = round(days['the_temp'])
        print(f"{days['applicable_date']} -- {days['weather_state_name']} \
        with an average of {avg_temp}ºC [{min_temp} - {max_temp}]")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
