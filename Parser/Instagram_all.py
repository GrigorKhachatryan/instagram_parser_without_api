# -*- coding: utf-8 -*-
import time
import json
import hashlib
import requests
from pprint import pprint
from selenium import webdriver


class InstaParser():
    def __init__(self, user_id=0):
        self.url = 'https://www.instagram.com/'
        self.counter = 0
        self.information = []
        self.user_id = user_id

    # Функция, которая убирает html  теги
    def parser_html(self):
        html_source = self.driver.page_source.replace(
            r'<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">',
            '').replace(r'</pre></body></html>', '')
        return json.loads(html_source)

    # Создается url для парсинга shortcode фоток
    def generate_url(self, page):
        hash = 'graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables='
        user_data = '{' + f'"id":"{self.user_id}","first":50,"after":"{page}"' + '}'
        url_page = self.url + hash + user_data
        return url_page

    # Непосредственный сбор кодов фоток
    def all_user_data(self, url_page):
        try:
            response = requests.get(url_page, headers=self.const_gis()).text
            json_user = json.loads(response)
            try:
                json_user = json_user['data']['user']['edge_owner_to_timeline_media']
                if json_user['count'] > 1300:
                    return None
            except TypeError:
                return None
            for edge in json_user['edges']:
                text = edge['node']['edge_media_to_caption']['edges']
                if len(text) == 0:
                    text = ''
                else:
                    text = text[0]['node']['text']
                photo_information = edge['node']['shortcode']
                if text is not None and len(text) > 5:
                    self.information.append(photo_information)
        except:
            print('Я сплю')
            time.sleep(150)
            return self.all_user_data(url_page=url_page)
        next_page = json_user['page_info']['end_cursor']
        if next_page is not None:
            self.instagram_parser(next_page)
        return next_page

    def const_gis(self):
        query_variable = '{"user_id":"' + str(self.counter + self.user_id) + '","include_reel":true}'
        t = 'jvSxaufdAkZQOEfmADK5vg==' + ':' + query_variable
        x_instagram_gis = hashlib.md5(t.encode("utf-8")).hexdigest()
        header = {'X-Instagram-GIS': x_instagram_gis,
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
                  'X-Requested-With': 'XMLHttpRequest'}
        self.counter += 100
        # print(self.counter)
        return header

    def id_to_login(self):
        query_variable = '{"user_id":"' + str(self.user_id) + '","include_reel":true}'
        header = self.const_gis()
        r = requests.get(
            'https://www.instagram.com/graphql/query/?query_hash=' + 'ad99dd9d3646cc3c0dda65debcd266a7' + '&variables=' + query_variable,
            headers=header).text
        try:
            username = json.loads(r)['data']['user']['reel']['user']['username']
        except:
            return False

        t = requests.get(self.url + username + '?__a=1', headers=header).text
        return username

    def pars_code(self, code):
        response = requests.get(self.url + 'p/' + code + '/?__a=1', headers=self.const_gis()).text
        result = json.loads(response)
        return result


    # Осталось написать тело, которое будет постоянно все вызывать
    ## тут нужно перебрать много id и вызвать функцию один раз, чтобы узнать количество фотографий
    def instagram_parser(self, end_cursor=''):

        url_page_user = self.generate_url(end_cursor)
        end_cursor = self.all_user_data(url_page_user)


        return self.information

    def pause_pars(self):
        time.sleep(5)


