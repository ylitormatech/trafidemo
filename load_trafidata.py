import datetime
import numpy as np
import pandas as pd
import pymongo
import warnings



client = pymongo.MongoClient()
db = client.lz_trafi


print("{}: Haetaan kuntien nimet tietokannasta".format(datetime.datetime.now()))
citylistcollection = db.kunnat
kunnat = list(citylistcollection.find())
print("{}: Kuntien nimet haettu".format(datetime.datetime.now()))

print("{}: Hae henkilöautot paikallisesta MongoDB palvelimesta".format(datetime.datetime.now()))
rawcollection = db.autot
df = pd.DataFrame(list(rawcollection.find({},{'kunta':1,
                                              'vuosi':1,
                                              'matkamittarilukema':1,
                                              'suurinNettoteho': 1,
                                              'vari': 1,
                                              'Co2': 1
                                              })))
print("{}: Henkilöautot haettu".format(datetime.datetime.now()))

print("{}: Ryhmittele tiedot kunnan ja rekisteröintivuoden mukaan".format(datetime.datetime.now()))
for gkey in [['kunta'], ['kunta', 'vuosi']]:
    for key, group in df.groupby(gkey):
        km = group['matkamittarilukema'].values
        co2 = group['Co2'].values
        teho = group['suurinNettoteho'].values


        km = km[~np.isnan(km)] # poista nan arvot
        co2 = co2[~np.isnan(co2)] # poista nan arvot
        teho = teho[~np.isnan(teho)] # poista nan arvot

        k = next((item for item in kunnat if item['kunta'] == (int(key[0]) if len(gkey)> 1 else key)), None)
        if k != None:
            dataitem = {'kunta': k['kuntanimi'],
                        'vuosi': key[1] if 'vuosi' in gkey else '',
                        'lkm': len(group),
                        'data': {
                            'km': {
                                'p25': np.nanpercentile(km, 25) if len(km) > 20 else '',
                                'p50': np.nanpercentile(km, 50) if len(km) > 20 else '',
                                'p75': np.nanpercentile(km, 75) if len(km) > 20 else ''
                            },
                            'co2': {
                                'p25': np.nanpercentile(co2, 25) if len(co2) > 20 else '',
                                'p50': np.nanpercentile(co2, 50) if len(co2) > 20 else '',
                                'p75': np.nanpercentile(co2, 75) if len(co2) > 20 else ''
                            },
                            'teho': {
                                'p25': np.nanpercentile(teho, 25) if len(teho) > 20 else '',
                                'p50': np.nanpercentile(teho, 50) if len(teho) > 20 else '',
                                'p75': np.nanpercentile(teho, 75) if len(teho) > 20 else ''
                            }
                        }
                        }
            db.autotkunnittain.insert_one(dataitem)
print("{}: Tiedot tallennettu tietokantaan".format(datetime.datetime.now()))