import sys
import requests
from bs4 import BeautifulSoup


class ArgumentError(Exception):
    pass


class GetWeather:
    def __init__(self):
        self.argv = sys.argv
        self.day = int(self.argv[-1])
        self.url = 'https://www.gismeteo.ru/weather-rostov-na-donu-13026/'
        self.get_weather()

    def __setattr__(self, key, value):
        if key == 'argv' and (len(value) != 2 or not (value[-1].isdigit() and 9 >= int(value[-1]) >= 0)):
            raise ArgumentError('Invalid argument')
        self.__dict__[key] = value

    def __get_suffix(self):
        suffix = ''
        if self.day == 1:
            suffix = 'tomorrow/'
        elif self.day > 1:
            suffix = f'{self.day + 1}-day/'
        return suffix

    def get_weather(self):
        suffix = self.__get_suffix()
        print(self.url + suffix)
        response = requests.get(self.url + suffix,
                                params={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'})
        # soup = BeautifulSoup(req.text, 'lxml')


if __name__ == '__main__':
    GetWeather()
