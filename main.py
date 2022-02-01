import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error,mean_absolute_error,mean_absolute_percentage_error
from keras.models import load_model
import streamlit as st

dataInizio = '2010-01-01'
dataFine = '2019-12-31'

st.title('Predizione di titoli azionari')
input = st.text_input('Inserisci un titolo azionario', 'AAPL')
#leggo i dati da yahoo finance
df = data.DataReader(input,'yahoo',dataInizio,dataFine)

#Descrizione del dataframe
st.subheader('Dati nel periodo 2010 - 2019')
st.write(df.describe())

#Visualizzazione
st.subheader('Prezzo nel tempo')
fig = plt.figure(figsize=(12,6))
plt.plot(df.Close)
st.pyplot(fig)

#Visualizzazione
st.subheader('Prezzo nel tempo con 100MA e 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12,6))
plt.plot(ma100, 'r')
plt.plot(ma200, 'g')
plt.plot(df.Close, 'b')
st.pyplot(fig)

#divido i dati in train e test
dataTraining = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
dataTesting = pd.DataFrame(df['Close'][0:int(len(df)*0.30)])

scaler = MinMaxScaler(feature_range=(0,1))
dataTrainingArray = scaler.fit_transform(dataTraining) #restituisce un array

#Carico il modello
model = load_model('modello.h5')

giorniPrecedenti = dataTraining.tail(100)
dfFinale = giorniPrecedenti.append(dataTesting, ignore_index=True)

inputData = scaler.fit_transform(dfFinale)

x_test = []
y_test = []
for i in range(100,inputData.shape[0]):
    x_test.append(inputData[i-100: i])
    y_test.append(inputData[i,0])

x_test , y_test = np.array(x_test), np.array(y_test)
#Ora faccio le predizioni
y_predicted = model.predict(x_test)

print('fattore di scala: ' + str(scaler.scale_[0]))
scaleFactor = 1/scaler.scale_[0]
y_predicted = y_predicted * scaleFactor
y_test = y_test * scaleFactor

print('errore assoluto medio: ' + str(mean_absolute_error(y_test,y_predicted)))
print('erroe assoluto medio percentuale: ' + str((mean_absolute_error(y_test,y_predicted)/y_test.mean())*100))

#Grafico finale
st.subheader('Predizioni vs Originari')
fig2 = plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label ='Prezzo originario')
plt.plot(y_predicted, 'r', label ='Prezzo predetto')
plt.xlabel('Tempo')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)
