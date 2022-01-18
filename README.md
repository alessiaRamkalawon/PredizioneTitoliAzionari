# Sistema di predizione di titoli azionari
**Membri del gruppo**: Ramkalawon Alessia 706212, Lovreglio Giuseppe 708245
<br> **Link Repository:** https://github.com/alessiaRamkalawon/PredizioneTitoliAzionari
<br>

Il progetto consiste in una piccola web-application in grado di raccogliere dati rigurdanti titoli azionari da un base di conoscenza ed effettuare delle predizioni.
Nello specifico, la predizione è effettuata sul prezzo (Closing Price).
<br>

**Funzionamento**
<br>
L'utente accede all'interfaccio web e ha la possibilità di inserire un titolo azionario.
Nel caso in cui l'utente non inserisca alcun titolo, il sistema lavorerà di default con **AAPL** (Apple).
Dopo aver premuto invio, l'utente ha accesso alla visualizzazione di 4 sezioni: <br>
**1)** Un riassunto, in forma tabellare, dei dati presi in considerazione nel periodo prestabilito (di default è 2010-2019) <br>
**2)** Un grafico che mostra la variazione del prezzo nel periodo di tempo <br>
**3)** Un grafico che mostra la variazione del prezzo nel periodo di tempo includendo anche la media mobile <br>
**4)** Un grafico che mostra il confronto tra il prezzo reale e il prezzo predetto <br> 

**Scelte di progettazione**   
Per lo sviluppo dell'applicazione è stato scelto il linguaggio Python<br>
Come sorgente di conoscenza da cui estrapolare i dati relativi ai titoli azionari, è stato scelto yahho finance.
Come periodo è stato preso in considerazione di default il 2010-2019.

Prima di creare il modello, sono state eseguite alcune operazioni preliminari. 
I dati sono stati filtrati per eliminare informazioni inutili e dopodichè sono stati divisi in Training set (70%) e Test set(70%).
Inoltre i valori sono stati scalati in un range [0-1]. <br>
Dopodichè si è passati alla creazione del modello di apprendimento. Nello specifico è stata utilizzata una rete neurale con layer LSTM(Long Short Term Memory) composto
da 1 layer di input, 3 layer intermedi e 1 finale così composti: <br>
**1° layer:** 50 unità <br>
**2° layer:** 60 unità <br>
**3° layer:** 80 unità <br>
**4° layer:** 1200 unità <br>
**5° layer:** 1 unità (il valore predetto) <br>
Come funzione di attivazione è stata utilizzata ReLU (Rectified linear unit activation function).
Infine è stato addestrato il modello con i dati di training e test ed è stato serializzato su file.
<br>
Dopodichè è stata creata la web-application utilizzando la libreria Streamlit.
Utilizzando l'applicazione sarà possibile effettuare predizioni, anche di diversi titoli azionari, utlizzando il modello precedentemente creato.
Dopo aver effettuato la predizione, il sistema riporta i valori dal range [0-1] al range originale.
<br> <br>
**Librerie utilizzate**
<br>
* _streamlit_ per la creazione della web-app
* _matplotlib_ per la presentazione dei grafici
* _numpy_ e _pandas_ per la gestione del dataset
* _keras_ e _sklearn_ per la creazione e addestramento del modello

