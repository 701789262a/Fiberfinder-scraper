# Fiberfinder-scraper

Script per fare scraping su [fiberfinder](https://fiberfinder.it/) dei comuni italiani e differenziarli per cluster.

## Requirements

Lo script richiede l'installazione di json e requests per il corretto funzionamento.


```bash
pip install json requests
```
## Esecuzione
L'esecuzione del programma richiede il passaggio di file .csv formattati in windows-1252 così strutturati:
```
REGIONE;COMUNE
REGIONE;COMUNE
    .
    .
    .
REGIONE;COMUNE
```

Il file .csv andrà passato come argv all'apertura dello script.
```bash
python3 comuni_of_fiberfinder.py comuni.csv
```
Lo script mostrerà per ogni comune lo stato (non rilegato - cluster AB - cluster CD - timeout/broken), il numero di comuni controllati e il numero totale da controllare.
```
Riga 1/4809 | Regione LIGURIA - Comune ARENZANO
^^^- Comune non rilegato
Riga 2/4809 | Regione LIGURIA - Comune AVEGNO
^^^- Comune non rilegato
Riga 3/4809 | Regione LIGURIA - Comune BARGAGLI
^^^- Comune non rilegato
```


I risultati verranno salvati, man mano che lo script controlla i comuni, sui file:
* cluster.csv per i comuni nei quali il sito risponde correttamente con un tipo di cluster (AB/CD).
* nonrilegati.csv per i comuni nei quali il sito risponde correttamente ma la specifica del cluster non è inserita nel JSON di risposta.
* broken.csv per i comuni nei quali il sito non risponde correttamente o la richiesta va in timeout.

I file .csv risultanti avranno la stessa struttura del file .csv di input.
