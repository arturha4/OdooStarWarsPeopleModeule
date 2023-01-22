import base64
import logging

import requests
from requests import Response
import json

logging.getLogger(__name__)


class Requester:
    def __init__(self, url: str):
        self.url: str = url
        self.response: Response = None
        self.related_object_url: dict = {}

    def save_response(self, data: Response):
        self.response = data

    def create_response(self):
        try:
            request = requests.get(self.url)
            if request.status_code == 200:
                self.save_response(request)
        except Exception as e:
            logging.info(f'Ошибка получения данных с удаленного url: {self.url}, трассировка {e}')

    def get_json_response(self):
        if self.response:
            try:
                return json.loads(self.response.text)
            except Exception as e:
                logging.info(f'Ошибка перевода данных в json, трассировка: {e} ')
                raise ValueError('Данные невозможно перевести в json')
        else:
            print('Поле response пустое')


class StarWarsRequester(Requester):
    def __init__(self, url):
        super().__init__(url)
        self.previous = None
        self.next = None
        self.obj = []
        self.create_response()

    def save_response(self, data: Response):
        self.response = data
        self.update_previous_and_next()
        self.update_obj()
        self.update_url()

    def filter_json_obj(self):
        return [{'name': item['name'], 'planet_url': item['homeworld'],
                 'image_pk': StarWarsRequester.get_pk_from_url(item['url']),
                 'planet_url_pk': StarWarsRequester.get_pk_from_url(item['homeworld'])} for item in
                self.get_json_response()['results']]

    @staticmethod
    def get_pk_from_url(url_with_pk: str):
        return int(url_with_pk.split('/')[-2])

    def update_previous_and_next(self):
        data = self.get_json_response()
        self.previous, self.next = data['previous'], data['next']

    def update_obj(self):
        for item in self.filter_json_obj():
            self.obj.append(item)

    def update_url(self):
        self.url = self.next

    def get_all_objects(self):
        while self.next:
            self.create_response()
        return self.obj


class StarWarsPlanetRequester(StarWarsRequester):

    @staticmethod
    def filter_unknown_fields(obj_items: dict):
        for key, value in obj_items.items():
            if value == "unknown":
                obj_items[key] = False
        return obj_items

    @staticmethod
    def get_objects_with_url_pk(data):
        return {item['planet_url_pk']: item for item in data}

    def filter_json_obj(self):
        return [StarWarsPlanetRequester.filter_unknown_fields(
            {'name': item['name'],
             'diameter': item['diameter'],
             'rotation_period': item['rotation_period'],
             'orbital_period': item['orbital_period'],
             'population': item['population'],
             'planet_url_pk': StarWarsRequester.get_pk_from_url(item['url'])}) for item in
            self.get_json_response()['results']]


class ImageRequester:
    def __init__(self, url: str, image_id: int, pk_prefix='.jpg'):
        self.url: str = url
        self.image_id: int = image_id
        self.pk_prefix: str = pk_prefix
        self.encoded_image = False
        self.create_image()

    def get_url_response(self):
        try:
            r = requests.get(self.url + str(self.image_id) + self.pk_prefix)
            if r.status_code == 200:
                return r.content
            else:
                raise ConnectionError('Некорректный url или ресурс недоступен')
        except Exception as e:
            logging.info(f'Ошибка получения изображения с удаленного url: {self.url}, трассировка {e}')

    def create_image(self, codec: str = 'ascii'):
        try:
            self.encoded_image = base64.b64encode(self.get_url_response()).decode(codec)
        except Exception as e:
            logging.info(
                f'Ошибка получения изображения, адрес: {self.url + str(self.image_id) + self.pk_prefix}. Трассирровка: {e}')
