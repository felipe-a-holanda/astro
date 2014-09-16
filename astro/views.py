#coding: utf-8
from astro import app
from flask import Flask, jsonify, render_template, request

import swisseph as swe
import subprocess
from datetime import datetime
from collections import namedtuple, defaultdict
from models import *

from make_svg_chart import get_chart



planet_names = ['Sol', 'Lua', 'Mercurio', 'Venus', 'Marte', 'Jupiter','Saturno', 'Urano', 'Netuno' ,'Plutao']
sign_names = ['Aries', 'Touro', 'Gemeos', 'Cancer', 'Leao', 'Virgem', 'Libra', 'Escorpiao', 'Sagitario', 'Capricornio', 'Aquario', 'Peixes']

planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']


@app.route('/_calc_planets')
def calc_planets():
    Planet = namedtuple('Planet', ['name', 'angle', 'sign'])
    planet_names = ['Sol', 'Lua', 'Mercurio', 'Venus', 'Marte', 'Jupiter','Saturno', 'Urano', 'Netuno' ,'Plutao']
    signs = ['Aries', 'Touro', 'Gemeos', 'Cancer', 'Leao', 'Virgem', 'Libra', 'Escorpiao', 'Sagitario', 'Capricornio', 'Aquario', 'Peixes']
    d = datetime.utcnow()
    t = list(d.timetuple()[:5])
    t[3] += t[4]/60.0
    t = t[:4]
    j = swe.julday(*t)
    result = {}
    result['date'] = d
    planets = []
    for i in range(10):
        a = swe.calc_ut(j,i)[0]
        s = signs[int(a/30)]
        
        d = {}
        d['index'] = i
        d['name'] = planet_names[i]
        d['angle'] = a
        d['sign'] = s
        planets.append(d)
    result['planets'] = planets
    return jsonify(result=result)




@app.route("/")
def index():
    #subprocess.call(['python', 'astro/make_svg_chart.py'])
    chart = get_chart()
    return render_template('chart.html', chart=chart)





@app.route("/people")
def people_by_sign():
    people = Event.objects()
    d = defaultdict(lambda: defaultdict(list))
    
    
    for person in people:
        for planet in person.birth._fields:
            sign = signs[int(getattr(person.birth,planet)/30)]
            d[planet.title()][sign].append(person)
    for i in d:
        for j in d[i]:
            d[i][j] = sorted(d[i][j])
    
        
    return render_template('people_by_signs.html', planets=planets, signs=signs, people=d)
