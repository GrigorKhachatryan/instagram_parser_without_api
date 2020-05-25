import os
import sys
sys.path.append('..')
import re
import requests
import json
import pickle
import time
import numpy as np
import pandas as pd
from pprint import pprint
from tensorflow.keras.preprocessing.sequence import pad_sequences
from parsering.instagram_all import InstaParser
from settings import API_KEY
from analysis.sentiment_analysis.lstm_model import Model
from scipy.spatial.distance import euclidean
# 1) Получить id
# 2) Парсинг постов
# 3) Обработка инфы с постов
# 4) Построения вектора средних оценок и соотнесение с кластером
# 5) возня в кластере
#
#
#
print(os.getcwd())
print(os.listdir(os.getcwd()))
class Information():

    def __init__(self, nickname='khachatryan_jr'):
        self.url = f'https://www.instagram.com/{nickname}/?__a=1'
        self.love_list = {'result':{}}
        self.model_lstm = Model().lstm()
        self.model_lstm.load_weights(os.getcwd() + '/web/best_model_lstm.h5')

        with open(os.getcwd() + '/analysis/sentiment_analysis/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        self.emoji_pattern = re.compile("["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        u"\U00002702-\U000027B0"
                                        u"\U000024C2-\U0001F251"
                                        u"\U0001f926-\U0001f937"
                                        u'\U00010000-\U0010ffff'
                                        u"\u200d"
                                        u"\u2640-\u2642"
                                        u"\u2600-\u2B55"
                                        u"\u23cf"
                                        u"\u23e9"
                                        u"\u231a"
                                        u"\u3030"
                                        u"\ufe0f"
                                        "]+", flags=re.UNICODE)

    def login_to_id(self):
        response = requests.get(self.url).json()
        return int(response['graphql']['user']['id'])

    def short_code(self):
        obj = InstaParser(user_id=self.login_to_id())
        short_list = obj.instagram_parser()
        return short_list

    def translate_text(self, text, dest_language="en"):
        translate_url = f'https://translate.yandex.net/api/v1.5/tr.json/translate?key={API_KEY}'
        param = {'text': text, 'lang': dest_language, 'format': 'plain'}
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(translate_url, params=param, headers=header).json()
        return response['text'][0]

    def posts_info(self):
        posts = self.short_code()[:300]
        for post in posts:
            response = requests.get(f'https://www.instagram.com/p/{post}/?__a=1', headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'Content-Type': 'application/json'})
            if response.status_code != 200:
                continue
            try:
                try:
                    print(1)
                    print(response.json())
                except:
                    v=1
                    print(11)
                json_res = response.text
                dataform = str(json_res).strip("'<>() ").replace('\'', '\"')
                json_res = json.loads(dataform)
                print(json_res)

            except BaseException as err:
                print(22222222,err)
            except:
                print(1)
                continue
            try:
                location = json_res['graphql']['shortcode_media']['location']
                post_text = str(json_res['graphql']['shortcode_media']["edge_media_to_caption"]["edges"][0]["node"]["text"])

                if location is None:
                    continue
                if location['address_json'] is None:
                    continue
                if json.loads(location['address_json'])["country_code"] == '':
                    continue

                post_text = self.emoji_pattern.sub('', post_text)[:200]
                if len(post_text) < 5:
                    continue
                post_text = self.translate_text(post_text)

                if json.loads(location['address_json'])["country_code"] not in self.love_list['result']:
                    self.love_list['result'][json.loads(location['address_json'])["country_code"]] = {'point':0,'count':0}
                self.love_list['result'][json.loads(location['address_json'])["country_code"]]['point'] += self.post_point(post_text)+1
                self.love_list['result'][json.loads(location['address_json'])["country_code"]]['count'] += 1
            except IndexError as err:
                print(err)
            except:
                continue
        return self.love_list

    def post_point(self, text):

        sequence = self.tokenizer.texts_to_sequences([text])
        data = pad_sequences(sequence, maxlen=50)
        result = self.model_lstm.predict(data)
        return int(np.argmax(result))

    def distance_centroid(self, centroid, df):
        min_dist, index, number = 10000, -1, 0

        for key, value in centroid.iterrows():
            dist = euclidean(df, value)
            if dist < min_dist:
                min_dist = dist
                index = number
            number += 1
        return index

    def clastering(self):

        country_points = self.posts_info()

        country_list = pd.read_csv(os.getcwd() + '/analysis/clastering/roo.scv')
        centroid = pd.read_csv(
            os.getcwd() + '/analysis/clastering/centroid.csv',
            header=None)


        country_list = list(country_list.columns)[1:]
        zero_data = np.zeros(shape=(1, len(country_list)))
        df = pd.DataFrame(zero_data, columns=country_list)
        for country, point in country_points['result'].items():
            df[country][0] = point['point'] / point['count']

        index = self.distance_centroid(centroid,df[:1])
        return index

    def similar_users(self):
        index = self.clastering()
        print(index)
        pprint(self.love_list)
        users_clusters = pd.read_csv(os.getcwd() + '/analysis/clastering/app.csv', header=None, index_col=0)
        one_cluster = []
        for key,value in users_clusters.iterrows():
            if np.all(value == index):
                one_cluster.append(int(key))
        result = {}
        country_list = pd.read_csv(os.getcwd() + '/analysis/clastering/roo.scv', index_col=0)
        for key,value in country_list.iterrows():
            if key in one_cluster :
                value_dict = json.loads(value.to_json())
                for country,point in value_dict.items():
                    if np.all(point>0):
                        if country not in result:
                            result[country] = point
                        else:
                            result[country] += point

        result_country = []
        result = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
        for item in result:
            if item[0] not in self.love_list['result'].keys():
                result_country.append(item[0])
            if len(result_country) == 5:
                break

        return result_country



