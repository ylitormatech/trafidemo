import datetime
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
from pandas import DataFrame
import pymongo
import requests, zipfile
import io

print("{}: Avaa tietokanta lz_trafi paikallisessa MongoDB palvelimessa".format(datetime.datetime.now()))
client = pymongo.MongoClient()
db = client.lz_trafi
rawcollection = db.autot



print("{}: Lataa kuntien nimet trafin ajoneuvojen luokitukset Excel tiedostosta".format(datetime.datetime.now()))
citylistcollection = db.kunnat
dfcitylist = pd.read_excel('http://www.trafi.fi/filebank/a/1433135757/74ee1d8be49178dbee2fc7df128bd5d6/17629-avoin_data_ajoneuvojen_luokitukset.xls',
                   'kunta',
                   skiprows=3,
                   parse_cols=[0, 1])
dfcitylist.columns = ['kunta', 'kuntanimi']
citylistcollection.insert_many(dfcitylist.to_dict('records'))

print("{}: Lataa varien nimet trafin ajoneuvojen luokitukset Excel tiedostosta".format(datetime.datetime.now()))
colorlistcollection = db.varit
dfcolorlist = pd.read_excel('http://www.trafi.fi/filebank/a/1433135757/74ee1d8be49178dbee2fc7df128bd5d6/17629-avoin_data_ajoneuvojen_luokitukset.xls',
                   'VARI',
                   skiprows=3,
                   parse_cols=[0, 1])
dfcolorlist.columns = ['vari', 'varinimi']
colorlistcollection.insert_many(dfcolorlist.to_dict('records'))

print("{}: Lataa käyttövoiman nimet trafin ajoneuvojen luokitukset Excel tiedostosta".format(datetime.datetime.now()))
fuellistcollection = db.polttoaineet
dffuellist = pd.read_excel('http://www.trafi.fi/filebank/a/1433135757/74ee1d8be49178dbee2fc7df128bd5d6/17629-avoin_data_ajoneuvojen_luokitukset.xls',
                   'KAYTTOVOIMA',
                   skiprows=3,
                   parse_cols=[0, 1])
dffuellist.columns = ['kayttovoima', 'kayttovoimanimi']
fuellistcollection.insert_many(dffuellist.to_dict('records'))

print("{}: Lataa yli 5 miljoonan ajoneuvon tiedot csv tiedostosta, joka sijaitsee Trafin sivuilla zip tiedoston sisällä".format(datetime.datetime.now()))
r = requests.get('http://wwwtrafifi.97.fi/opendata/AvoinData20160101.zip')
z = zipfile.ZipFile(io.BytesIO(r.content),'r')
df = pd.read_csv(z.open(z.namelist()[0]),
                 index_col=False,
                 iterator=True,
                 chunksize=1000,
                 sep=';',
                 engine='c',
                 encoding='ISO-8859-1',
                 usecols=['ajoneuvoluokka',
                          'kunta',
                          'alue',
                          'kayttoonottopvm',
                          'matkamittarilukema',
                          'Co2',
                          'sahkohybridi',
                          'merkkiSelvakielinen',
                           'vari',
                           'omamassa',
                           'kayttovoima',
                           'iskutilavuus',
                           'suurinNettoteho',
                           'kaupallinenNimi'
                          ],
                 dtype={

                          'kayttoonottopvm': np.str
                        }
                 )
print("{}: Data ladattu muistiin".format(datetime.datetime.now()))

print("{}: Valitaan datasta mukaan vain henkilöautot (M1)".format(datetime.datetime.now()))
df = pd.concat([chunk[chunk['ajoneuvoluokka'] == 'M1'] for chunk in df])
print("{}: Henkilöautojen valinta suoritettu".format(datetime.datetime.now()))
print("{}: Muuta sarakeen kayttoonottopvm arvo vuodeksi (jätä neljä ensimmäistä merkkiä)".format(datetime.datetime.now()))
df['kayttoonottopvm'] = df['kayttoonottopvm'].map(lambda x: str(x)[:4])
print("{}: Nimeä kayttoonottopvm sarakkeeksi vuosi".format(datetime.datetime.now()))
df.rename(columns={'kayttoonottopvm': 'vuosi'}, inplace=True)
print("{}: Tallennetaan henkilöautot tietokantaan".format(datetime.datetime.now()))
rawcollection.insert_many(df.to_dict('records'))
print("{}: Data ladattu tietokantaan".format(datetime.datetime.now()))
