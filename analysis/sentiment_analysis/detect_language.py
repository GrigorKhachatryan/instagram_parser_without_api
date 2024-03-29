import re
import psycopg2.extras
import time
import asyncio
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from settings import PASSWORD


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
        else:
            lang.append((a, i['code']))




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
    lang = []
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

    cursor.executemany('update  publication set language=%s where code=%s', lang)
    connection.commit()

    print(f'Английских {len(engl)} постов.')
    print(f'Русских {len(rus)} постов.')
    print(f'Других языковых постов - {len(lang)}')



