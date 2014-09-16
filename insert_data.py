#coding: utf-8
from pygeocoder import Geocoder
import datetime
from astro.models import *

import swisseph as swe
import datetime



def make_data():
    escargots = """
    Felipe Holanda (m), 22 Dec. 1986 at 6:34 , Limoeiro do Norte (Ceará)
    Rodrigo Souzas (m), 27 Dec. 1986 at 9:35 , Jacareí (São Paulo)
    Robson Oliveira (m), 4 Feb. 1990 at 13:10 , Iguatu (Ceará)
    Rafaele Paiva (f), 24 Jun. 1990 at 15:53 , São Bernardo do Campo (São Paulo)
    Rodrigo Cardoso (m), 13 Jul. 1991 at 21:35 , Curitiba (Paraná)
    João Lisboa (m), 12 Sep. 1991 at 10:30 , Rio Branco (Acre)
    Claudio Trigo (m), 26 Feb. 1993 at 9:46 , São Paulo
    Catharina Inagaki (f), 24 Mar. 1995 at 2:00 , Ribeirão Preto (São Paulo)
    Isis Frank (f), 16 Oct. 1990 at 21:05 , São José dos Campos (São Paulo)
    Aline Marinelli (f), 24 May. 1989 at 17:55 , São Paulo
    Jose Alan (m), 17 Mar. 1995 at 14:15 , São José dos Campos (São Paulo)
    Sabrina Zoletti (f), 22 Feb. 1994 at 4:10 , Guarapuava (Paraná)
    Luara Maria Zago (f), 2 Feb. 1994 at 12:00 , Jaú (São Paulo)
    Amanda Prokop (m), 25 Oct. 1992 at 0:12 , Calgary, AB (CAN)
    Fernando Ferreira (m), 10 Jan. 1987 at 3:36 , Campinas (São Paulo)
    Zorica Atanasovska (f), 12 Aug. 1986 at 10:50 , Gevgelija, MKD
    """
    p = {}
    for line in escargots.strip().split('\n'):
        l = line.split(',')
        name = l[0].strip()
        gender = name.split('(')[1].split(')')[0].strip()
        name = name.split('(')[0].strip()
        date = l[1].strip()
        date = datetime.datetime.strptime(date, "%d %b. %Y at %H:%M")
        #print date

        location = ' '.join(l[2:]).strip()
        results = Geocoder.geocode(location)
        location = unicode(results[0])
        coords = results[0].coordinates
        
        d = {}
        d['name'] = name
        d['location'] = location
        d['coords'] = coords
        d['timestamp'] = date
        p[name] = d
    print p
    return p
    

#p = make_data()
p = {'Jo\xc3\xa3o Lisboa': {'timestamp': datetime.datetime(1991, 9, 12, 10, 30), 'coords': (-9.975377, -67.8248977), 'name': 'Jo\xc3\xa3o Lisboa', 'location': u'Rio Branco - State of Acre, Brazil'}, 'Aline Marinelli': {'timestamp': datetime.datetime(1989, 5, 24, 17, 55), 'coords': (-23.5505199, -46.63330939999999), 'name': 'Aline Marinelli', 'location': u'S\xe3o Paulo - S\xe3o Paulo, Brazil'}, 'Sabrina Zoletti': {'timestamp': datetime.datetime(1994, 2, 22, 4, 10), 'coords': (-25.3907214, -51.4628097), 'name': 'Sabrina Zoletti', 'location': u'Guarapuava - Parana, Brazil'}, 'Isis Frank': {'timestamp': datetime.datetime(1990, 10, 16, 21, 5), 'coords': (-23.223701, -45.9009074), 'name': 'Isis Frank', 'location': u'S\xe3o Jos\xe9 dos Campos - S\xe3o Paulo, Brazil'}, 'Luara Maria Zago': {'timestamp': datetime.datetime(1994, 2, 2, 12, 0), 'coords': (-22.30275, -48.5755491), 'name': 'Luara Maria Zago', 'location': u'Ja\xfa - S\xe3o Paulo, Brazil'}, 'Zorica Atanasovska': {'timestamp': datetime.datetime(1986, 8, 12, 10, 50), 'coords': (41.140278, 22.502778), 'name': 'Zorica Atanasovska', 'location': u'Gevgelija, Macedonia (FYROM)'}, 'Catharina Inagaki': {'timestamp': datetime.datetime(1995, 3, 24, 2, 0), 'coords': (-21.1704008, -47.8103238), 'name': 'Catharina Inagaki', 'location': u'Ribeir\xe3o Preto - S\xe3o Paulo, Brazil'}, 'Robson Oliveira': {'timestamp': datetime.datetime(1990, 2, 4, 13, 10), 'coords': (-6.3587958, -39.29805899999999), 'name': 'Robson Oliveira', 'location': u'Iguatu - Cear\xe1, Brazil'}, 'Jose Alan': {'timestamp': datetime.datetime(1995, 3, 17, 14, 15), 'coords': (-23.223701, -45.9009074), 'name': 'Jose Alan', 'location': u'S\xe3o Jos\xe9 dos Campos - S\xe3o Paulo, Brazil'}, 'Rodrigo Cardoso': {'timestamp': datetime.datetime(1991, 7, 13, 21, 35), 'coords': (-25.4200388, -49.2650973), 'name': 'Rodrigo Cardoso', 'location': u'Curitiba - State of Paran\xe1, Brazil'}, 'Rodrigo Souzas': {'timestamp': datetime.datetime(1986, 12, 27, 9, 35), 'coords': (-23.2987827, -45.96625419999999), 'name': 'Rodrigo Souzas', 'location': u'Jacare\xed - S\xe3o Paulo, Brazil'}, 'Felipe Holanda': {'timestamp': datetime.datetime(1986, 12, 22, 6, 34), 'coords': (-5.1443118, -38.0850339), 'name': 'Felipe Holanda', 'location': u'Limoeiro do Norte - Cear\xe1, Brazil'}, 'Fernando Ferreira': {'timestamp': datetime.datetime(1987, 1, 10, 3, 36), 'coords': (-22.9099384, -47.0626332), 'name': 'Fernando Ferreira', 'location': u'Campinas - State of S\xe3o Paulo, Brazil'}, 'Claudio Trigo': {'timestamp': datetime.datetime(1993, 2, 26, 9, 46), 'coords': (-23.5505199, -46.63330939999999), 'name': 'Claudio Trigo', 'location': u'S\xe3o Paulo - S\xe3o Paulo, Brazil'}, 'Rafaele Paiva': {'timestamp': datetime.datetime(1990, 6, 24, 15, 53), 'coords': (-23.6898429, -46.5648481), 'name': 'Rafaele Paiva', 'location': u'S\xe3o Bernardo do Campo - S\xe3o Paulo, Brazil'}, 'Amanda Prokop': {'timestamp': datetime.datetime(1992, 10, 25, 0, 12), 'coords': (51.0453246, -114.0581012), 'name': 'Amanda Prokop', 'location': u'Calgary, AB, Canada'}}


planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']



def calc_sign(angle_degrees):
    return signs[int(angle_degrees/30)]

def calc_chart(date):
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour + date.minute/60
    julday = swe.julday(year, month, day, hour)
    dic = {}
    for planet_index in range(10):
        n = planets[planet_index]
        d = swe.calc_ut(julday, planet_index)[0]
        s = calc_sign(d)
        dic[n.lower()] = d
    return dic
        #print "%12s %-12s %.2f"%(n,s,d)
    #print


def insert():
    Event.drop_collection()
    for i in p.values():
        name = i['name']
        local = i['location']
        date = i['timestamp']
        coord = list(reversed(i['coords']))
        chart = Chart(**calc_chart(date))
        e = Event(name, local, date, coord, chart)
        
        #print e
        e.save()
        #print name
        calc_chart(date)


insert()
