#coding: utf-8
import svgwrite
import xml.dom.minidom
import math
from math import cos,sin,pi
from collections import namedtuple
import swisseph as swe
import codecs
from datetime import datetime
from bs4 import BeautifulSoup
#from IPython import embed

N_PLANETS = 10
CENTER = 300, 300



class Planet(object):
    PLANET_NAMES = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter','Saturn', 'Uranus', 'Neptune' ,'Pluto']
    PLANET_GLYPHS = u'☉☽☿♀♂♃♄♅♆♇'
    
    
    def __init__(self, index, angle):
        self.index = index
        self.name = self.PLANET_NAMES[index]
        self.glyph = self.PLANET_GLYPHS[index]
        self.angle = angle
        self.sign = Sign(int(self.angle/30))
        self.aspects = []
    
    def dss(self, degrees):
        d,m,s = dms(degrees)
        sign = self.sign.glyph
        return "%d %s %d'"%(d,sign,m)
        
    def get_desc(self):
        desc = self.glyph+" "+self.dss(self.angle%30)+'\n\n'+'\n'.join([a.get_desc() for a in self.aspects if a.is_visible()])
        return desc
    
    def _get_tooltip(self, dwg):
        svg = dwg.svg(id=self.name+'-tooltip', visibility='hidden' )
        desc = self.get_desc()
        for i,t in enumerate(desc.split('\n')):
            txt = dwg.text(t, (0,15*(i+1)))
            svg.add(txt)
        return svg
    
    def draw(self, dwg, center, radius):
        height = 20
        width = 20
        r = height/2
        
        #svg = dwg.svg(id=self.name, onmousemove="ShowTooltip(evt, this)", onmouseout="HideTooltip(evt, this)")
        svg = dwg.svg(id=self.name)
        g = dwg.g()
        angle = self.angle
        posCircle = polarToCartesian(center, radius, angle)
        
        circle = dwg.circle(center=posCircle, r=r) 
        circle.fill('white', opacity=0.5).stroke('black', width=1)
        
        g.add(circle)
        
        
        posImg = polarToCartesian((center[0]-r,center[1]-r),radius,self.angle)
        img = dwg.image('static/img/planets/%02d-%s.svg'%(self.index+1,self.name.lower()), height=height, width=width, insert=posImg)
        
        
        g.add(img)
        
        circle = dwg.circle(center=posCircle, r=r, id=self.name+'_drawing') 
        circle.fill('white', opacity=0.01).stroke('black', width=1)
        circle.set_desc(_get_tooltip2(self.get_desc()))
        #setTitle(circle, _get_tooltip2(self.get_desc()))
        g.add(circle)
        
        
        
        #desc = self.get_desc()
        #txt = dwg.text(desc, id=self.name+'-tooltip', visibility='hidden')
        #g.add(_get_tooltip(dwg, self.name, self.get_desc()))
        #g.set_desc(desc,desc)
        svg.add(g)
        return svg
        

class Aspect(object):
    GLYPHS = u'☌⚺⚹□△⚻☍'
    def __init__(self, planet1, planet2):
        self.p1 = planet1
        self.p2 = planet2
        self.name = planet1.name+"_"+planet2.name
        self.angle = self._diff(planet1.angle, planet2.angle)
        self.type, self.diff = self._calc_type()
        self.glyph = self.GLYPHS[self.type]
    
    def get_desc(self):
        d,m,s = dms(self.diff)        
        return u"%s %s %s %d° %d'"%(self.p1.glyph, self.glyph, self.p2.glyph, d,m)
    

    
    def draw(self, dwg, center, radius):
        planet1, planet2 = self.p1, self.p2
        a1 = planet1.angle
        a2 = planet2.angle
        p1 = polarToCartesian(center, radius, a1)
        p2 = polarToCartesian(center, radius, a2)
        #svg = dwg.svg(id = self.name, onmousemove="ShowTooltip(evt, this)", onmouseout="HideTooltip(evt, this)")
        svg = dwg.svg(id = self.name)
        line = dwg.line(p1,p2)
        line2 = dwg.line(p1,p2,id = self.name+'_drawing')
        
        diff = lambda x,y: min((2 * 180.0) - abs(x - y), abs(x - y))
        angle = diff(a1, a2)
        a,b = divmod(angle,30)
        c,d = map(abs,divmod(angle,-30))
        diff_angle, aspect_type = min((b,a), (d,c))
        aspect_type = int(aspect_type)
        
        
        color = 'none'
        linewidth = 1
        alpha = 1
        
        aspect_name = ['conjunct', '30', 'sextile', 'square', 'trine', '150', 'opposite'][aspect_type]
        
        if aspect_type in [3,6]:
            color='red'
        if aspect_type in [2,4]:
            color='blue'
        
        orb = self.orb()
        
        if diff_angle>orb:
            color = 'none'
        if diff_angle<orb/2:
            linewidth = int(4-diff_angle)
        else:
            
            alpha = (orb-diff_angle)/orb
            if alpha<0:
                color = 'none'
                
        desc = self.get_desc()
        line2.set_desc(_get_tooltip2(desc))
        line2.stroke(color, 10, 0.01)
        
        line.stroke(color, linewidth, alpha)
        #txt = dwg.text(desc, id=self.name+'-tooltip', visibility='hidden')
        
        svg.add(line)
        svg.add(line2)
        
        
        #svg.add(_get_tooltip(dwg, self.name, self.get_desc()))
        return svg
    
    def is_visible(self):
        return self.type in [0,2,3,4,6] and self.in_orb()
        
    def orb(self):
        orbs = [15,12,7,7,8,9,9,5,5,5]
        orb = (orbs[self.p1.index] + orbs[self.p2.index])/2.0
        return orb
    
    def in_orb(self):
        return self.diff < self.orb()
        
    def _diff(self, x, y):
        return min((2 * 180.0) - abs(x - y), abs(x - y))
    
    def _calc_type(self):
        angle = self.angle
        a,b = divmod(angle,30)
        c,d = map(abs,divmod(angle,-30))
        diff_angle, aspect_type = min((b,a), (d,c))
        aspect_type = int(aspect_type)
        return aspect_type, diff_angle


class Sign(object):
    SIGN_NAMES = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    SIGN_GLYPHS = u'♈♉♊♋♌♍♎♏♐♑♒♓'
    
    def __init__(self, index):
        self.index = index
        self.name = self.SIGN_NAMES[index]
        self.glyph = self.SIGN_GLYPHS[index]
    
    def get_desc(self, planets):
        desc = "%s %s"%(self.glyph,self.name)
        if any([p.sign.index==self.index for p in planets]):
            desc+="\n"
        for p in planets:
            if p.sign.index==self.index:
                d,m,s = dms(p.angle%30)
                desc += u"\n%s %d° %d'"%(p.glyph,d,m)
        return desc
    
    def _get_tooltip(self, dwg, planets):
        svg = dwg.svg(id=self.name+'-tooltip', visibility='hidden' )
        desc = self.get_desc(planets)
        svg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(50,50,50)'))
        for i,t in enumerate(desc.split('\n')):
            txt = dwg.text(t, (0,15*(i+1)))
            svg.add(txt)
        return svg
        
                
    
    def draw(self, dwg, center, r1, r2, r3, planets):
        height=30
        width=30
        colors=['red','green','yellow','blue']
        
        svg = dwg.svg()
        #g = dwg.g(id=self.name, onmousemove="ShowTooltip(evt, this)", onmouseout="HideTooltip(evt, this)")
        g = dwg.g(id=self.name)
        pos = polarToCartesian((center[0],center[1]-height/2),r1-width/2,0)
        img = dwg.image('static/img/signs/%02d-%s.svg'%(self.index+1,self.name.lower()), height=height, width=width, insert=pos)
        img.rotate(-self.index*30-15,center)
        rotate_around_center(img, -90)
        a1 = arc(dwg, r2, r1, 30*self.index, 30*(self.index+1))
        a2 = arc(dwg, r3, r2, 30*self.index, 30*(self.index+1))
        a1.fill(colors[self.index%len(colors)], opacity=0.5).stroke('black', width=2)
        a2.fill(colors[self.index%len(colors)], opacity=0.25).stroke('black', width=1)
        a2.opacity=0.2
        
        g.add(a1)
        
        a3 = arc(dwg, r2, r1, 30*self.index, 30*(self.index+1), id=self.name+'_drawing')
        a3.fill(colors[self.index%len(colors)], opacity=0.01).stroke('black', width=1)
        a3.set_desc(_get_tooltip2(self.get_desc(planets)))
        
        
        svg.add(a2)
        g.add(img)
        g.add(a3)
        svg.add(g)
        #svg.add(_get_tooltip(dwg, self.name, self.get_desc(planets)))
        return svg


class Chart(object):
    N_PLANETS = 10
    def __init__(self, now=None):
        self.now = now
        if not now:
            self.now = datetime.utcnow()
        self.planets = self._calc_planets()
        self.aspects = self._calc_aspects()
        
    
    def draw(self, name):
        dwg = svgwrite.Drawing(filename=name, size=(600,600), debug=True)
        dwg.add(dwg.script(content="""    function ShowTooltip(evt, obj) {
        var tooltip = document.getElementById(obj.id+"-tooltip");
        tooltip.setAttribute("x", evt.clientX + 11);
        tooltip.setAttribute("y", evt.clientY + 27);
        tooltip.setAttribute("visibility", "visible");
    }

    function HideTooltip(evt, obj) {
        var tooltip = document.getElementById(obj.id+"-tooltip");
        tooltip.setAttribute("visibility", "hidden");
    }"""))
        dwg.add(self._draw_aspects(dwg))
        dwg.add(self._draw_signs(dwg))
        dwg.add(self._draw_planets(dwg))
        if name:
            dwg.save()
            self._prettify(name)
        
        return dwg
    
    
    
    def _calc_planets(self):
        d = self.now
        t = list(d.timetuple())
        t[3] += t[4]/60.0
        t = t[:4]
        j = swe.julday(*t)
        planets = []
        for i in range(self.N_PLANETS):
            angle = swe.calc_ut(j,i)[0]
            planets.append(Planet(i, angle))
        

        return planets
    
    def _calc_aspects(self):
        planets = self.planets
        aspects = []
        for i, p1 in enumerate(planets):
            for j, p2 in enumerate(planets):
                if j>i:
                    a = Aspect(p1, p2)
                    aspects.append(a)
                    p1.aspects.append(a)
                    p2.aspects.append(a)
        return aspects
                    
    def _draw_signs(self, dwg):
        center=CENTER
        r1 = 290
        r2 = 240
        r3 = 200
        
        zodiac = dwg.svg(id='zodiac')
        signs = [Sign(i) for i in range(12)]
        for sign in signs:
            zodiac.add(sign.draw(dwg, center, r1, r2, r3, self.planets))
        return zodiac
    
    def _draw_planets(self, dwg):
        R=220
        center=CENTER
        
        planets = self.planets
        svg_planets = dwg.svg(id='planets')
        planets.reverse()
        for planet in self.planets:
            svg_planets.add(planet.draw(dwg, center, R))
        return svg_planets
    
    def _draw_aspects(self, dwg):
        center=CENTER
        planets = self.planets
        R=200
        
        svg = dwg.svg(id='aspects')
        for i, p1 in enumerate(planets):
            for j, p2 in enumerate(planets):
                if j>i:
                    line = Aspect(planets[i], planets[j]).draw(dwg, center, R)
                    svg.add(line)
        return svg
    
    def _prettify(self, name):
        x = xml.dom.minidom.parse(name)
        pretty_xml_as_string = x.toprettyxml()
            
        with codecs.open(name,'w','utf-8') as f:
            f.write(pretty_xml_as_string)


def polarToCartesian(center, radius, angleInDegrees):
    centerX, centerY = center
    angleInRadians = (180-angleInDegrees) * math.pi / 180.0
    x = centerX + (radius * math.cos(angleInRadians))
    y = centerY + (radius * math.sin(angleInRadians))
    return x, y
        

def arc(dwg, inner_radius, outer_radius, startAngle, endAngle, **kwargs):
    center = CENTER
    
    outer_start_x, outer_start_y = polarToCartesian(center, outer_radius, startAngle);
    outer_end_x, outer_end_y = polarToCartesian(center, outer_radius, endAngle);

    inner_start_x, inner_start_y = polarToCartesian(center, inner_radius, startAngle)
    inner_end_x, inner_end_y = polarToCartesian(center, inner_radius, endAngle)
    
    arcSweep = "0" if endAngle - startAngle <= 180 else "1"
    path_txt = ""
    path_txt += "M {inner_start_x} {inner_start_y} "
    path_txt += "L {outer_start_x}, {outer_start_y} " # Line to 
    path_txt += "A {outer_radius} {outer_radius} 0 {arcSweep} 0 {outer_end_x} {outer_end_y} " # Arc
    path_txt += "L {inner_end_x} {inner_end_y} "
    path_txt += "A {inner_radius} {inner_radius} 0 {arcSweep} 1 {inner_start_x} {inner_start_y} "
    
    path = dwg.path(path_txt.format(**locals()), **kwargs)
    
    
    return path
    
def rotate_around_center(img, angle):
    x = float(img.attribs['x']) + float(img.attribs['width'])/2
    y = float(img.attribs['y']) + float(img.attribs['height'])/2
    img.rotate(angle,(x,y))
    
"""
Degrees to degrees, minutes, seconds
"""
def dms(degrees):
    
    d, f = divmod(degrees,1)
    f *= 60
    m, f = divmod(f,1)
    f *= 60
    s, f = divmod(f,1)
    return map(int,[d,m,s])


def _get_tooltip(dwg, name, text):
    svg = dwg.svg(id=name+'-tooltip', visibility='hidden' )
    #svg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(50,50,50)'))
    
    for i,t in enumerate(text.split('\n')):
        txt = dwg.text(t, (0,15*(i+1)))
        svg.add(txt)
    return svg
    
def _get_tooltip2(text):
    return text
    text = text.replace('\n','<br>')

    return text


def prettify(name):
    with codecs.open(name,'r','utf8') as f:
        soup = BeautifulSoup(f.read())
    
    for title in soup.findAll('title'):
        title.string = title.string.replace('\n','<br/>\n')
    with codecs.open(name,'w','utf8') as f:
        f.write(soup.svg.prettify(formatter=None))
        
def prettify_text(text):
    soup = BeautifulSoup(text)
    
    for title in soup.findAll('title'):
        title.string = title.string.replace('\n','<br/>\n')
        
    return soup.svg.prettify(formatter=None)
        
        
def get_chart():
    name = "astro/static/img/chart.svg"
    return prettify_text(Chart().draw(name).tostring())
    

if __name__ == '__main__':
    name = "astro/static/img/chart.svg"
    get_chart()
    
    
    #name = "static/img/chart.svg"
    Chart().draw(name)
    prettify(name)
