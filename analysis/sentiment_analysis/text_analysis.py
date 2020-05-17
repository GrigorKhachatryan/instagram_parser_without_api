from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, MaxPooling1D, Conv1D, GlobalMaxPooling1D, Dropout, LSTM, GRU, SpatialDropout1D
from tensorflow.keras import utils
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import re
en_stops = set(stopwords.words('english'))
reg = re.compile('[^a-zA-Z ]')
lemmatizer = WordNetLemmatizer()

# Максимальное количество слов
num_words = 5000
# Максимальная длина новости
max_news_len = 50
# Количество классов новостей
nb_classes = 5

# Получение тренировочных данных
train = pd.read_csv('data/train_en.csv',
                    header=None,
                    names=['text', 'star'])
reviews = train['text']
y_train = utils.to_categorical(train['star'] - 1, nb_classes)

for i in reviews:
    if type(i) is float:
        print(i)
# Создаем токенизатор
tokenizer = Tokenizer(num_words=num_words)
# Обучаем токенизатор
tokenizer.fit_on_texts(reviews)
# Используем на наших данных
sequences = tokenizer.texts_to_sequences(reviews)
x_train = pad_sequences(sequences, maxlen=max_news_len)


# Сохраняем токенизатор
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Создание нейронной сети
model_lstm = Sequential()
model_lstm.add(Embedding(num_words, 100, input_length=max_news_len))
model_lstm.add(SpatialDropout1D(0.1))
model_lstm.add(LSTM(64, dropout=0.2, recurrent_dropout=0.1))
model_lstm.add(Dense(5, activation='softmax'))

model_lstm.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
# -----

# Подключение колбеков
model_lstm_save_path = 'best_model_lstm.h5'
checkpoint_callback_lstm = ModelCheckpoint(model_lstm_save_path,
                                      monitor='val_accuracy',
                                      save_best_only=True,
                                      verbose=1)
# -----

# Обучение нашей нейросети
history_lstm = model_lstm.fit(x_train,
                              y_train,
                              epochs=20,
                              batch_size=128,
                              validation_split=0.1,
                              callbacks=[checkpoint_callback_lstm])

# ----

# Открываем тестовые данные
test = pd.read_csv('data/test_en.csv',
                    header=None,
                    names=['text', 'star'])
reviews = test['text']
y_test = utils.to_categorical(test['star'] - 1, nb_classes)

# Токенизация данных
test_sequences = tokenizer.texts_to_sequences(test['text'])
x_test = pad_sequences(test_sequences, maxlen=max_news_len)

# Выделение правильных ответов
y_test = utils.to_categorical(test['star'] - 1, nb_classes)

# Загрузка весов
model_lstm.load_weights(model_lstm_save_path)
# Прогонка с загруженными весами
model_lstm.evaluate(x_test, y_test, verbose=1)

text = 'This journey was amazing I liked everything! The hotel was so great, the villagers were really nice. I love them. I ate some food in the local restaurant. So I have never eaten so delicious food before! I will come back soon!'
text = reg.sub('', text)
text = text.lower()
data_text = text.split(' ')
list_text = []
for word in data_text:
    if word not in en_stops and len(word) > 1:

        list_text.append(lemmatizer.lemmatize(word,'v'))

text = str(' '.join(list_text))
sequence = tokenizer.texts_to_sequences([text])
data = pad_sequences(sequence, maxlen=max_news_len)
result = model_lstm.predict(data)
print(result)