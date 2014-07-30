from flask import Flask, render_template
import swisseph as swe
from datetime import datetime
from collections import namedtuple

app = Flask(__name__)
app.debug = True

def calc_planets():
    Planet = namedtuple('Planet', ['name', 'angle', 'sign'])
    planet_names = ['Sol', 'Lua', 'Mercurio', 'Venus', 'Marte', 'Jupiter','Saturno', 'Urano', 'Netuno' ,'Plutao']
    signs = ['Aries', 'Touro', 'Gemeos', 'Cancer', 'Leao', 'Virgem', 'Libra', 'Escorpiao', 'Sagitario', 'Capricornio', 'Aquario', 'Peixes']
    d=datetime.utcnow()
    t=list(d.timetuple()[:5])
    t[3]+=t[4]/60.0
    t=t[:4]
    j = swe.julday(*t)
    txt=str(d)+"\n<br>\n"
    planets = []
    for i in range(10):
        
        a = swe.calc_ut(j,i)[0]
        s = signs[int(a/30)]
        #txt += "%s %.4f %s\n<br>\n"%(planets[i], a%30,s)
        planets.append(Planet(planet_names[i], a, s))

    return planets


@app.route("/")
def hello():
    planets = calc_planets()
    return render_template('base.html', planets=planets)
    
if __name__ == "__main__":
    app.run()

