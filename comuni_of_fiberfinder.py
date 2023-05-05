import json
import socket
import sys

import requests

# Template per la richiesta POST a fiberfinder.
json_data = {
    'region': '%s',
    'city': '%s',
    'address': 'Non definito',
    'number': '',
}


def main():
    # File .csv da controllare.
    csv_file_raw = open(sys.argv[1], 'r',encoding="windows-1252")
    csv_file_ok = open('cluster.csv', 'a',encoding="utf-8-sig")
    csv_file_nonrilegati = open('nonrilegati.csv', 'a',encoding="utf-8-sig")
    csv_file_broken = open('broken.csv', 'a',encoding="utf-8-sig")

    csv_lines = csv_file_raw.readlines()

    csv_file_raw.close()

    csv_lines_number = len(csv_lines)

    i=0
    # Iterazione su ogni riga del file .csv.
    for line in csv_lines:
        i+=1
        tuple_city = line.split(';')
        json_data['region'] = tuple_city[0].strip()
        json_data['city'] = tuple_city[1].strip()
        print(f"Riga {i}/{csv_lines_number} | Regione %s - Comune %s" % (json_data['region'], tuple_city[1].strip()))
        try:

            # Richiesta POST a finderfinder - impostato timeout 5s per gestire le parecchie HTTP504.
            response = requests.post('https://www.fiberfinder.it/api/require/results', json=json_data, timeout=5).text
            response = json.loads(response)['OF']['cluster']
            print("^^^- Cluster: %s" % response)

            # Scrittura del comune e corrispettivo cluster nel file.
            csv_file_ok.write("%s;%s;%s\n" % (json_data['region'], json_data['city'], response))
            csv_file_ok.flush()

        # In caso il cluster non venga menzionato, si presume comune non rilegato.
        except KeyError:
            print("^^^- Comune non rilegato")
            csv_file_nonrilegati.write("%s;%s;%s\n" % (json_data['region'], json_data['city'], '-'))
            csv_file_nonrilegati.flush()

        # In caso di timeout si presume errore lato sito e si scrive in un file apposito.
        except socket.error:
            print("^^^- Timeout :(")
            csv_file_broken.write("%s;%s;%s\n" % (json_data['region'], json_data['city'], '-'))
            csv_file_broken.flush()

    # Chiudo i file
    csv_file_nonrilegati.close()
    csv_file_ok.close()
    csv_file_broken.close()


if __name__ == "__main__":
    main()
