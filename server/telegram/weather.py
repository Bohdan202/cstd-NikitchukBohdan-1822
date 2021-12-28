from telegram import localization

import requests
from urllib.parse import quote

import datetime
from bs4 import BeautifulSoup as BS
from dateutil.relativedelta import relativedelta

def get_weather_fordays(language, city, days_number=3):
    city = city.lower()
    
    if days_number > 10:
        days_number = 10

    link = localization.weather[language][0] + quote("погода-" + city) + '/' + quote("10-" + localization.weather[language][1])

    response = requests.get(link)
    response = BS(response.content, 'html.parser')
    response = response.select(".main")

    result = []

    def getNowDate():
        now = datetime.datetime.now()
        d = f'{now.year}-{now.month}-{now.day}'
        
        return d

    def parseSinoptikDesc(city, date = getNowDate()):
        localization.weather[language][0] + quote("погода-" + city) + '/' + quote("10-" + localization.weather[language][1])
        response = requests.get(localization.weather[language][0] + quote("погода-" + city) + '/' + date + '?ajax=GetForecast')

        return BS(response.content, 'html.parser')

    def echoDesc(city, nextDay):
        html = parseSinoptikDesc(city, nextDay)
        main = html.select_one(".wDescription .description").text

        return main.strip(' \t\n\r')

    def getNextDay(day = 1):
        now = datetime.datetime.now()
        next_day = now + relativedelta(days=+day)
        next_day = str(next_day).split(' ')[0] # y-m-d

        return next_day

    def getDescriptions(city):
        result = []

        for x in range(10):
            if x == days_number:
                break

            result.append( echoDesc(city, getNextDay(x)) )

        return result

    descriptions = getDescriptions(city)

    for index, element in enumerate(response):
        if index == days_number:
            break

        day = element.select_one('.day-link').text
        date = element.select_one('.date').text
        month = element.select_one('.month').text
        t_min = element.select_one('.temperature .min').text
        t_max = element.select_one('.temperature .max').text

        result.append(f'{day} - <b>{date} {month.title()}</b>:\n{t_min}, {t_max}\n<i>{descriptions[index]}</i>\n\n')


    result = f'<b>{city.title()}</b>\n\n' + "".join(result)
    # print(result)

    return result
    