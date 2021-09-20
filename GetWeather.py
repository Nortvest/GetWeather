import sys
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup


class ArgumentError(Exception):
    pass


class GetWeather:
    def __init__(self):
        self.argv = sys.argv
        self.day = int(self.argv[-1])
        self.url = 'https://www.gismeteo.ru/weather-rostov-na-donu-5110/'
        self.get_weather()

    def __setattr__(self, key, value):
        if key == 'argv' and len(value) == 1:
            self.__dict__[key] = [0]
            return
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
        data = []
        suffix = self.__get_suffix()
        print(self.url + suffix)
        response = requests.get(self.url + suffix,
                                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'})
        soup = BeautifulSoup(response.text, 'html.parser')
        data.append(['{:02d}:{}'.format(int(i.text[:-2]), i.text[-2:])
                     for i in soup.find('div', class_='widget__row_time').find_all('div', class_='widget__item')])
        data.append([i.get('data-text')
                     for i in soup.find('div', class_='widget__row_table').find_all('span', class_='tooltip')])
        data.append([i.text
                     for i in soup.find('div', class_='widget__row_temperature').find_all('span', class_='unit unit_temperature_c')])
        data.append([i.text.strip()
                     for i in soup.find_all('div', class_='widget__row_table')[2].find_all('span', class_='unit unit_wind_m_s')])
        data.append([i.text.strip()
                     for i in
                     soup.find('div', class_='widget__row_precipitation').find_all('div', class_='w_prec__value')])
        self.set_table(data)

    @staticmethod
    def set_table(data):
        print(tabulate(data, tablefmt="fancy_grid"))


if __name__ == '__main__':
    GetWeather()
