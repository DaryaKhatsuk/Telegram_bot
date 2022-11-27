import asyncio
import csv
import json
import time

import aiohttp
from bs4 import BeautifulSoup


class ParserAV:
    def __init__(self):
        """
        :self.JSON, self.CSV: переменные содержащие названия файлов в проекте форматов .json и .csv.
        :self.HOST: host сайта.
        :self.URL: url раздела, в котором производится парсинг.
        :self.HEADERS: искать в главном домене раздела "сеть"/"network" консоли браузера.
        """
        self.JSON = 'cars.json'
        self.CSV = 'cars.csv'
        self.HOST = 'https://av.by/'
        self.URL = 'https://moto.av.by/filter?category_type=1'
        self.HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        }
        self.cards = []

    async def get_content(self, session_request):
        """
        :param session_request: получает всю html информацию со страницы от функции parser.
        :soup: берет данный со страницы отправленные функцией parser
        :items: собирает со всей страницы все div классы под названием listing-item__wrap
        :AttributeError: обрабатывает отсутствие в карточках описания, т.к. это необязательный для
         заполнения пользователем параметр.
        :Exception: общее исключение для обработки внезапных ошибок.
        :return: safe_doc(cards), передает данные для сохранения в форматах json и csv
        """
        soup = BeautifulSoup(await session_request, 'html.parser')
        items = soup.find_all('div', class_='listing-item__wrap')
        for item in items:
            try:
                title_car = item.find('span', class_='link-text').text
                href_car = 'https://moto.av.by' + item.find('a', class_='listing-item__link').get('href')
                price_car_byn = item.find('div', class_='listing-item__price').text.replace('\xa0', ' ').replace(
                    '\u2009', ' ')
                price_car_usd = item.find('div', class_='listing-item__priceusd').text.replace('\xa0', ' ').replace(
                    '\u2009', ' ')
                params_car = item.findNext('div', class_='listing-item__params').text.replace('\n', ' ').replace(
                    '\u2009', ' ').replace('\xa0', ' ')
                card = {href_car: [title_car, price_car_byn, price_car_usd, params_car]}
                self.cards.append(card)
            except AttributeError:
                title_car = item.find('span', class_='link-text').text
                href_car = ['https://moto.av.by' + item.find('a', class_='listing-item__link').get('href')]
                price_car_byn = item.find('div', class_='listing-item__price').text.replace('\xa0', ' ').replace(
                    '\u2009', ' ')
                price_car_usd = item.find('div', class_='listing-item__priceusd').text.replace('\xa0', ' ').replace(
                    '\u2009', ' ')
                card = {href_car: [title_car, price_car_byn, price_car_usd, 'Pass']}
                self.cards.append(card)
                print(f'params_car: pass')
            except Exception as ex:
                print(f'Some {ex} here.')

    def safe_doc(self):
        """
        :return: запись в json и csv файлы.
        """
        with open(self.JSON, 'w', newline='', encoding='UTF-8') as file:
            wordbook = {}
            sc = 1
            for item in self.cards:
                wordbook.update(
                        item
                )
                sc += 1
            json.dump(self.cards, file, indent=4, ensure_ascii=False)
            print('The data is saved in JSON.')

    async def parser(self):
        """
        :async with aiohttp.ClientSession(): позволяет использовать одну сессию несколько раз.
        :session_request (первый): использует данные url и headers сети.
        :session_request.status == 200: проверяет что бы статус подключения на странице был 200,
         т.е. существующей, не пустой страницей.
        :counter: является счетчиком для отсчитывания страниц, в виду использования цикла while
        :session_request (второй): подставляет в открытую сессию точные данные страницы, которую нужно спарсить сейчас.
        :asyncio.create_task(get_content(session_request.text())): создает асинхронную задачу передачи данных со страницы,
         в виде текста, в функцию get_content.
        """
        async with aiohttp.ClientSession() as session:
            session_request = await session.get(url=self.URL, headers=self.HEADERS)
            counter = 1
            while session_request.status == 200:
                session_request = await session.get(url=self.URL + '&page=' + str(counter))
                print(f'Parsing page {counter}')
                asyncio.create_task(self.get_content(session_request.text()))
                counter += 1
            else:
                print(f"Session status: {session_request.status}. Data is being saved.")
                self.safe_doc()

    def par(self):
        x = time.time()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait([self.parser()]))
        y = time.time()
        print(y - x)


parser_run = ParserAV()
print(parser_run.par())