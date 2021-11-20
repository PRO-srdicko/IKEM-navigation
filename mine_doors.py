from os import read, write
import requests
import rstr
from bs4 import BeautifulSoup
import json

url = 'http://ikem.di-base.com/cz/show?qrkod='

door_names = ['A 1001', 'A 1001-01', 'A 1001-02', 'A 1002', 'A 1002a', 'A 1002a-01', 'A 1002a-02', 'A 1002b', 'A 1002c', 'A 1002d', 'A 1003', 'A 1004', 'A 1005', 'A 1005a', 'A 1005b', 'A 1005c', 'A 1006', 'A 1007', 'A 1008', 'A 1009', 'A 1009a', 'A 1009b', 'A 1010', 'A 1011', 'A 1012', 'A 1012a', 'A 1012b', 'A 1012c', 'A 1013', 'A 1014', 'A 1014-01', 'A 1014-02', 'A 1015', 'A 1016', 'A 1017', 'A 1018', 'A 1019', 'A 1020', 'A 1021', 'A 1022', 'A 1023', 'A 1023a', 'A 1024', 'A 1026', 'A 1026a', 'A 1026b', 'A 1026c', 'A 1026c-01', 'A 1026c-02', 'A 1027', 'A 1028', 'A 1029', 'A 1030', 'A 2001', 'A 2001-01', 'A 2001-02', 'A 2001-03', 'A 20013-01', 'A 20013-02', 'A 2001a', 'A 2001a-01', 'A 2001a-02', 'A 2001a-03', 'A 2001b', 'A 2001c', 'A 2001d', 'A 2001d-01', 'A 2001d-02', 'A 2001d-03', 'A 2002', 'A 2002a', 'A 2003', 'A 2003a', 'A 2003b', 'A 2003c', 'A 2004', 'A 2004a', 'A 2005', 'A 2006', 'A 2007', 'A 2007a', 'A 2007b', 'A 2007c', 'A 2008', 'A 2008a', 'A 2008b', 'A 2008c', 'A 2010', 'A 2010a',
              'A 2011', 'A 2011a', 'A 2012', 'A 2012a', 'A 2013', 'A 2013-01', 'A 2013-02', 'A 2014', 'A 2014a', 'A 2015', 'A 2015a', 'A 2016', 'A 2016a', 'A 2017', 'A 2018', 'A 2018a', 'A 2018b', 'A 2018c', 'A 2019', 'A 2020', 'A 2020a', 'A 2020b', 'A 2020c', 'A 2021', 'A 2022', 'A 2023', 'A 2024', 'A 2025', 'A 2026', 'A 3001', 'A 3001a', 'A 3002', 'A 3003', 'A 3003a', 'A 3003b', 'A 3003c', 'A 3003d', 'A 3004', 'A 3005', 'A 3005a', 'A 3005b', 'A 3005c', 'A 3005d', 'A 3006', 'A 3007', 'A 3008', 'A 3009', 'A 3009a', 'A 3010', 'A 3010a', 'A 3010b', 'A 3010c', 'A 3011', 'A 3011a', 'A 3011b', 'A 3012', 'A 3012a', 'A 3012a-01', 'A 3012a-02', 'A 3012b', 'A 3013', 'A 3013a', 'A 3013b', 'A 3013c', 'A 3013d', 'A 3013e', 'A 3013f', 'A 3013i', 'A 3013j', 'A 3014', 'A 3014a', 'A 3014b', 'A 3014c', 'A 3015', 'A 3016', 'A 3017', 'A 3018', 'A 3019', 'C 2001', 'C 2002a', 'C 2004', 'C 2004a', 'C 2004b', 'C 3001', 'C 3002', 'C 3002a', 'C 3003a', 'C 3007b', 'D 2002', 'D 2002a', 'D 2002b', 'D 2003', 'D 2003a', 'D 2003b', 'D 2004', 'D 2004a', 'D 2005']

door_codes = [name.replace(' ', '_') for name in door_names]

database = {}


for code in sorted(door_codes):
    print(code)
    database[code] = {}
    response = requests.get(url+code)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    for row in soup.find_all(class_='reportsboxlabel'):
        strings = list(row.strings)
        if len(strings) < 1:
            continue
        parameter = strings[0].split(':')[0]
        if len(strings) == 1:
            database[code][parameter] = None
        else:
            if parameter == 'Nazev':
                database[code][parameter] = str(strings[1]).split(' - ')[2]
            else:
                database[code][parameter] = strings[1]
    print(database[code])

with open('door_database.json', 'w', encoding='utf-8') as f:
    json.dump(database, f, indent=6, ensure_ascii=False)
