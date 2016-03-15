import datetime
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
from pandas import DataFrame
import pymongo
import requests, zipfile
import io

client = pymongo.MongoClient()
db = client.lz_trafi
rawcollection = db.carsrawdata
citycollection = db.carsbycity
citycollectionfinal = db.carsbycityfinal

citylistcollection = db.citylist
dfcitylist = pd.read_excel('D:/Downloads/trafi/AvoinData20160101/17629-avoin_data_ajoneuvojen_luokitukset.xls',
                   'kunta',
                   skiprows=3,
                   parse_cols=[0, 1])
citylistcollection.insert_many(dfcitylist.to_dict('records'))

print("{}: Start loading trafi data from onedrive storage".format(datetime.datetime.now()))
r = requests.get('http://wwwtrafifi.97.fi/opendata/AvoinData20160101.zip')
z = zipfile.ZipFile(io.BytesIO(r.content),'r')
df = pd.read_csv(z.open(z.namelist()[0]),
                 index_col=False,
                 iterator=True,
                 chunksize=1000,
                 sep=';',
                 engine='c',
                 usecols=['ajoneuvoluokka',
                          'kunta',
                          'alue',
                          'kayttoonottopvm',
                          'matkamittarilukema',
                          'Co2',
                          'sahkohybridi',
                          # 'merkkiSelvakielinen',
                          # 'ensirekisterointipvm',
                          # 'vari',
                          # 'omamassa',
                          # 'kayttovoima',
                          # 'iskutilavuus',
                          # 'suurinNettoteho',

                          # 'mallimerkinta',
                          # 'vaihteisto',
                          # 'kaupallinenNimi'
                          ],
                 dtype={
                        'matkamittarilukema': np.str,
                          'kayttoonottopvm': np.str
                        }
                 )
print("{}: Trafi data loaded".format(datetime.datetime.now()))
print("{}: Start filtering data and include only cars (M1)".format(datetime.datetime.now()))
df = pd.concat([chunk[chunk['ajoneuvoluokka'] == 'M1'] for chunk in df])
print("{}: Filterin completed".format(datetime.datetime.now()))
print("{}: Store raw data into local mongodb".format(datetime.datetime.now()))
rawcollection.insert_many(df.to_dict('records'))
print("{}: Group data by kunta and include only alue and matkamittarilukema".format(datetime.datetime.now()))
df = pd.DataFrame(list(rawcollection.find({},{'kunta':1, 'alue':1, 'matkamittarilukema':1})))
grouped = df.groupby(['kunta'])['kunta'].groups
print("{}: Calculate min, max, average and quantiles by kunta. Store result to local mongodb. Store into local Mongodb".format(datetime.datetime.now()))
for k in grouped.keys():
    try:
        kunta = citylistcollection.find({'KOODINTUNNUS': k})[0]['PITKASELITE_fi']

    except IndexError:
        kunta = "Ei löydy kunnan nimeä"
    citycollection.insert({'kunta': kunta, 'km': sorted(grouped[k]) })
    dd = DataFrame(np.array(grouped[k]), columns=['km'])
    quan = dd.quantile([0.25,0.5,0.75])['km'].values.tolist()
    citycollectionfinal.insert({
        'kunta': kunta,
        'km': quan,
        'max': int(np.max(grouped[k])),
        'min': int(min(grouped[k])),
        'avg': int(np.average(grouped[k])),
        'count': len(grouped[k])})
print("{}: Dataload completed".format(datetime.datetime.now()))
# print("Copy data into mLab database")

#####################
# POSTGRESQL
#####################
# engine = create_engine('postgresql://devuser:password@localhost/lz_trafi')
# df.to_sql('rawdata2', engine)