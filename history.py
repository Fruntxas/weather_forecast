# pylint: disable=missing-docstring

import sys
import urllib
import datetime
import csv
import requests


from weather import search_city, BASE_URI


def daily_forecast(woeid, year, month, day):
    '''Return the daily forecasts'''
    daily_url = urllib.parse.urljoin(BASE_URI, f"/api/location/{woeid}/{year}/{month}/{day}")
    return requests.get(daily_url).json()

def monthly_forecast(woeid, year, month):
    '''Return the total daily forecasts for the month'''
    month_forecast = []
    date = datetime.date(year, month, 1)
    last_date = datetime.date(year + int(month/12), month%12+1, 1)-datetime.timedelta(days=1)
    while date <= last_date:
        print(f"Fetching forecast for {date.strftime('%Y-%m-%d')}")
        month_forecast += daily_forecast(woeid, date.year, date.month, date.day)
        date = date + datetime.timedelta(days=1)
    return month_forecast

def write_csv(woeid, year, month, city, forecasts):
    ''' Extract the monthly forecast to a csv on the data folder '''
    path_file_name = f"data/{year}_{'{:02d}'.format(month)}_{woeid}_{city.lower()}.csv"
    with open(path_file_name, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = forecasts[0].keys())
        writer.writeheader()
        writer.writerows(forecasts)


def main():
    if len(sys.argv) > 2:
        city = search_city(sys.argv[1])
        if city:
            woeid = city['woeid']
            year = int(sys.argv[2])
            month = int(sys.argv[3])
        if 1 <= month <= 12:
            forecasts = monthly_forecast(woeid, year, month)
            if not forecasts:
                print("Sorry, could not fetch any forecast")
            else:
                write_csv(woeid, year, month, city['title'], forecasts)
        else:
            print("MONTH must be a number between 1 (Jan) and 12 (Dec)")
            sys.exit(1)
    else:
        print("Usage: python history.py CITY YEAR MONTH")
        sys.exit(1)


if __name__ == '__main__':
    main()
