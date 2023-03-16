"""Napisz program, który sprawdzi, czy danego dnia będzie padać. Użyj do tego poniższego
API. Aplikacja ma działać następująco:

Program pyta dla jakiej daty należy sprawdzić pogodę. Data musi byc w formacie YYYY-mm-dd,
 np. 2022-11-03. W przypadku nie podania daty, aplikacja przyjmie za poszukiwaną
 datę następny dzień.
Aplikacja wykona zapytanie do API w celu poszukiwania stanu pogody.
Istnieją trzy możliwe informacje dla opadów deszczu:
Będzie padać (dla wyniku większego niż 0.0)
Nie będzie padać (dla wyniku równego 0.0)
Nie wiem (gdy wyniku z jakiegoś powodu nie ma lub wartość jest ujemna)
Będzie padać
Nie będzie padać
Nie wiem
Wyniki zapytań powinny być zapisywane do pliku. Jeżeli szukana data znajduje sie juz w
pliku, nie wykonuj zapytania do API, tylko zwróć wynik z pliku.

URL do API:
https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=
rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date=
{searched_date}

W URL należy uzupełnić parametry: latitude, longitude oraz searched_date
"""
import requests
import pprint
MIESIACE = {
    "01": [31],
    "02": [28],
    "03": [31],
    "04": [30],
    "05": [31],
    "06": [30],
    "07": [31],
    "08": [31],
    "09": [30],
    "10": [31],
    "11": [30],
    "12": [31],

}
def sprawdz_date(dstr: str) -> bool:
    dstr = dstr.strip()
    parts = dstr.split('-')
    if len(parts) != 3:
        return False
    year, month, day = parts
    year = [e for e in year if e.isdigit()]
    month = [e for e in month if e.isdigit()]
    day = [e for e in day if e.isdigit()]
    if len(year) != 4:
        return False
    if len(month) != 2:
        return False
    if len(day) != 2:
        return False
    if not (2000 <= int("".join(year)) <= 2023):
        return False
    month = "".join(month)
    if month not in MIESIACE:
        return False
    day = "".join(day)
    dni_miesiaca = MIESIACE[month][0]
    mozliwe_dni = [str(d) if d > 9 else f"0{str(d)}" for d in range(1,dni_miesiaca)]
    if day not in mozliwe_dni:
        return False
    return True


latitude = '52.237049'
longitude = '21.017532'
searched_date = input("Podaj Date: ")
URL = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}' \
      f'&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}' \
      f'&end_date={searched_date}'
zapytanie = requests.get(URL)
dane = zapytanie.json()
pprint.pprint(dane)
if not zapytanie.ok:
    print(f"Blad API {zapytanie.status_code}")
    quit()
pogoda = []
for p in zapytanie.json()['daily']['rain_sum']:
    pogoda.append(float(p))
    print(pogoda)
    if p == 0.0:
        print('Nie Padalo w Tym Dniu')
    if p > 0.0:
        print('Padalo w Tym Dniu')
    if p < 0.0:
        print('Blad')
    with open('output.txt','w') as plik:
        #while True:
           # plik.write(f"{p}")
