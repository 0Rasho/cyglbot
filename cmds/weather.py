import requests
from lib.config import config
from lib.utils import throttle

KEY = config['API']['weather']


class Weather(object):

    def weatherdata(self, city):
        url = 'http://api.openweathermap.org/data/2.5/weather?' \
              'q=%s&lang=ru&units=metric&APPID=%s' % (city, KEY)
        if city.isalpha():
            try:
                data = requests.get(url).json()
                desc = data['weather'][0]['description'].capitalize()
                temp = '%s' % round(data['main']['temp'])
                result = 'Weather in city %s: %s %s degreeC' \
                         % (city.capitalize(), desc, temp)
            except Exception:
                return
            return result
        else:
            return 'Incorrect city'

    def forecast(self, city):
        url = 'http://api.openweathermap.org/data/2.5/forecast/daily?' \
              'q=%s&mode=json&lang=ru&' \
              'units=metric&cnt=3&APPID=%s' % (city, KEY)
        if city.isalpha():
            try:
                data = requests.get(url).json()['list']
                temp = [i['temp']['day'] for i in data]
                desc = [x['weather'][0]['description'] for x in data]
                tomorrow = '%s %s' % (desc[1].capitalize(), round(temp[1]))
                aftertmrw = '%s %s' % (desc[2].capitalize(), round(temp[2]))
            except Exception:
                return
            return tomorrow, aftertmrw
        else:
            return 'Incorrect city'

    @throttle(5)
    def _cmd_weather(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Enter city!' % username)
            return
        data = args.split()
        city = data[0]
        (tomorrow, aftertomorrow) = self.forecast(city)
        tomorrow_res = 'Weather in the city of% s on tomorrow:% s degreeC' \
            % (city.capitalize(), tomorrow)
        aftertomorrow_res = 'Weather in the city of% s on the next day: ' \
            '%s degreeC' % (city.capitalize(), aftertomorrow)
        if self.weatherdata(city) and len(data) < 2:
            cirno.sendmsg('%s: %s' % (username, self.weatherdata(city)))
        elif self.forecast(city) and data[1] == 'tomorrow':
            cirno.sendmsg('%s: %s' % (username, tomorrow_res))
        elif self.forecast(city) and data[1] == 'aftertomorrow':
            cirno.sendmsg('%s: %s' % (username, aftertomorrow_res))


def setup():
    return Weather()
