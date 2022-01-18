import numpy as np
import pandas as pd
import pandas_datareader as data
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential

dataInizio = '2010-01-01'
dataFine = '2019-12-31'

#leggo i dati da yahoo finance
df = data.DataReader('APPL','yahoo',dataInizio,dataFine)
df = df.reset_index()

#rimuovo le colonne che non servono
df = df.drop(['Date','Adj Close'], axis = 1)

mediaMobile100 = df.Close.rolling(100).mean()

mediaModile200 = df.Close.rolling(200).mean()

#Decido di lavorare con la colonna 'Close' perchè sono interessato al Closing Price di una certa data
#Creo i df di train (70%) e test (30%)
dataTraining = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
dataTesting = pd.DataFrame(df['Close'][0:int(len(df)*0.30)])

#scalo i valori nel range 0-1 (mi serve per passarli all' LSTM)
scaler = MinMaxScaler(feature_range=(0,1))

dataTrainingArray = scaler.fit_transform(dataTraining) #restituisce un array

x_train = []
y_train = []

#Divido i dati in train e test
for i in range(100, dataTrainingArray.shape[0]):
    x_train.append(dataTrainingArray[i-100:i])
    y_train.append(dataTrainingArray[i,0])

x_train, y_train = np.array(x_train), np.array(y_train)

#Creo il modello sequenziale
model = Sequential()
#Aggiungo i 4 layers
#1
model.add(LSTM(units=50, activation='relu', return_sequences= True, input_shape=(x_train.shape[1],1)))
model.add(Dropout(0.2))

#2
model.add(LSTM(units=60, activation='relu', return_sequences= True))
model.add(Dropout(0.3))

#3
model.add(LSTM(units=80, activation='relu', return_sequences= True))
model.add(Dropout(0.4))

#4
model.add(LSTM(units=120, activation='relu'))
model.add(Dropout(0.5))

#l'ultimo layer è formato da 1 sola unità perchè prediciamo 1 solo valore (Closing price)
model.add(Dense(units = 1))

print(model.summary())

#utilizzo l'adam optimizer e l'errore quadratico medio
model.compile(optimizer='adam', loss= 'mean_squared_error')
#addestro il modello
model.fit(x_train, y_train, epochs=50)

#salvo il modello
model.save('modello.h5')

giorniPrecedenti = dataTraining.tail(100)
dfFinale = giorniPrecedenti.append(dataTesting, ignore_index=True)

inputData = scaler.fit_transform(dfFinale)

x_test = []
y_test = []

for i in range(100,inputData.shape[0]):
    x_test.append(inputData[i-100: i])
    y_test.append(inputData[i,0])

x_test , y_test = np.array(x_test), np.array(y_test)

#Faccio le predizioni
y_predicted = model.predict(x_test)

scaleFactor = 1/scaler.scale_
y_predicted = y_predicted * scaleFactor
y_test = y_test * scaleFactor