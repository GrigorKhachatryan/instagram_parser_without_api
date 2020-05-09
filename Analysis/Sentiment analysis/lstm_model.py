from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Dropout, LSTM, SpatialDropout1D


class Model():
    def __init__(self):
        # Максимальное количество слов
        self.num_words = 5000
        # Максимальная длина новости
        self.max_news_len = 200
        # Количество классов новостей
        self.nb_classes = 5

    def lstm(self):
        model_lstm = Sequential()
        model_lstm.add(Embedding(self.num_words, 100, input_length=self.max_news_len))
        model_lstm.add(SpatialDropout1D(0.1))
        model_lstm.add(LSTM(64, dropout=0.2, recurrent_dropout=0.1))
        model_lstm.add(Dense(5, activation='softmax'))

        model_lstm.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        return model_lstm
