#!/usr/bin/env python

import matplotlib.pyplot as plt
import os
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, LambdaCallback
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from utils import *




directory = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(directory, "data.csv"), names = column_names)
# print(df.head())            # view top 5 data
# print(df.isnull().sum())    # check if any field is empty
    




# --------------------------------   Data Normalization   --------------------------------

df = df.iloc[:, 1:]
df_norm = (df - df.mean())/df.std()
# print(df_norm.head())

y_mean = df['price'].mean()
y_std = df['price'].std()

def convert_label_value(pred):
    return int(pred * y_std + y_mean)
    




# --------------------------------   Creating training and test sets   --------------------------------

x = df_norm.iloc[:, :6]
y = df_norm.iloc[:, -1]

# print(x.head())
# print(y.head())

x_arr = x.values
y_arr = y.values

# print(f"Feature array shape : {x_arr.shape}")
# print(f"Labels array shape : {y_arr.shape}")

x_train, x_test, y_train, y_test = train_test_split(x_arr, y_arr, test_size=0.05, random_state=0 )
    




# --------------------------------   Model Creation   --------------------------------

def get_model():
    model = Sequential([
        Dense(10, input_shape=(6,), activation='relu'),
        Dense(20, activation='relu'),
        Dense(5, activation='relu'),
        Dense(1)
    ])

    model.compile(
        loss='mse',
        optimizer='adam'
    )
    
    return model

# print(get_model().summary())
    




# --------------------------------   Model Training   --------------------------------

es_cb = EarlyStopping(monitor='val_loss', patience=5)

model = get_model()
preds_on_untrained = model.predict(x_test)

history = model.fit(
    x_train, y_train, validation_data = (x_test, y_test), epochs=100, callbacks =[es_cb]
)

plot_loss(history)

    




# --------------------------------   Predictions   --------------------------------

preds_on_trained = model.predict(x_test)
compare_predictions(preds_on_untrained, preds_on_trained, y_test)

price_untrained = [convert_label_value(y) for y in preds_on_untrained]
price_trained = [convert_label_value(y) for y in preds_on_trained]
price_test = [convert_label_value(y) for y in y_test]
compare_predictions(price_untrained, price_trained, price_test)