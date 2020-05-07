import psycopg2.extras
from settings import PASSWORD
import csv
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import re
import ssl
import random

lemmatizer = WordNetLemmatizer()

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('stopwords')
nltk.download('wordnet')

en_stops = set(stopwords.words('english'))
reg = re.compile('[^a-zA-Z ]')

connection = psycopg2.connect(user="postgres",
                              password=PASSWORD,
                              host="localhost",
                              port="5434",
                              database="postgres")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
# train = []
# test = []
# cursor.execute('select text,star from dataset_en where star=5')
# dataset_db = cursor.fetchall()
# train.extend(dataset_db[10000:25000])
# test.extend(dataset_db[:40000])
# cursor.execute('select text,star from dataset_en where star=4')
# dataset_db = cursor.fetchall()
# train.extend(dataset_db[:15000])
# test.extend(dataset_db[30000:40000])
# cursor.execute('select text,star from dataset_en where star=3')
# dataset_db = cursor.fetchall()
# train.extend(dataset_db[:30000])
# test.extend(dataset_db[30000:])
# cursor.execute('select text,star from dataset_en where star=2')
# dataset_db = cursor.fetchall()
# train.extend(dataset_db[:10000])
# test.extend(dataset_db[10000:])
# cursor.execute('select text,star from dataset_en where star=1')
# dataset_db = cursor.fetchall()
# train.extend(dataset_db[:9000])
# test.extend(dataset_db[9000:])

#
# random.shuffle(train)
# random.shuffle(test)
cursor.execute('select text,star from dataset_en  ')
dataset_db = cursor.fetchall()

random.shuffle(dataset_db)

train = dataset_db[20000:]
test = dataset_db[:20000]

# for i in dataset_db[:30000]:
#     if i not in train:
#         print(True)
#         test.append(i)
#     if len(test) > 3000:
#         break
# for i in train:
#     if i[1] == 5:
#         i[1] = 4
# for i in test:
#     if i[1] == 5:
#         i[1] = 4


def render_text(data):
    for i in data:
        i[0] = reg.sub('', i[0])
        i[0] = i[0].lower()
        data_text = i[0].split(' ')
        text = []
        for word in data_text:
            if word not in en_stops and len(word) > 1:

                text.append(lemmatizer.lemmatize(word,'v'))

        text = str(' '.join(text))
        i[0] = text


render_text(test)
render_text(train)

with open('train_en.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(train)

with open('test_en.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(test)

