import re
import psycopg2.extras
import pickle
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from settings import PASSWORD
from lstm_model import Model
import time
import asyncio
import aiohttp


en_stops = set(stopwords.words('english'))
reg = re.compile('[^a-zA-Z ]')
lemmatizer = WordNetLemmatizer()

connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
print('начал работать')
cursor.execute("select posts,code from publication where posts is not null and language is null")
data = cursor.fetchall()
print('загрузил данные -- ', len(data))

# # Максимальное количество слов
# num_words = 5000
# # Максимальная длина новости
# max_news_len = 200
# # Количество классов новостей
# nb_classes = 5
#
# # Создание нейронной сети
# model_lstm = Model().lstm()
# model_lstm.load_weights('best_model_lstm.h5')
# starts = time.time()
# with open('tokenizer.pickle', 'rb') as handle:
#     tokenizer = pickle.load(handle)
# loop = asyncio.get_event_loop()
# engl = []
# rus = []


async def posts_inst(datas):
    for i in datas:

        try:
            a = detect(i['posts'])
        except LangDetectException:
            a = ''
        if a == 'en':
            engl.append(('en', i['code']))
        elif a == 'ru':
            rus.append(('ru', i['code']))

        # sequence = tokenizer.texts_to_sequences([text])
        # data = pad_sequences(sequence, maxlen=max_news_len)
        # result = model_lstm.predict(data)
        # print(a,np.argmax(result))


async def main():

    chunk = len(k) // 30
    start, stop = 0, chunk

    futures = []
    while stop <= len(k):
        futures.append(loop.create_task(posts_inst(k[start:stop])))
        start += chunk
        stop += chunk

    await asyncio.gather(*futures)


for j in range(0,len(data),500):
    engl= []
    rus = []
    print(j, j+500)
    k = data[j:j+500]
    loop = asyncio.get_event_loop()
    starts = time.time()
    try:
        loop.run_until_complete(main())
    except BaseException as err:
        print(err)
    print(time.time() - starts)

    cursor.executemany('update publication set language=%s where code=%s', engl)
    connection.commit()

    cursor.executemany('update  publication set language=%s where code=%s', rus)
    connection.commit()

    print(f'Английских {len(engl)} постов.')
    print(f'Русских {len(rus)} постов.')



