from astro import db





class Chart(db.EmbeddedDocument):
    sun = db.FloatField()
    moon = db.FloatField()
    mercury = db.FloatField()
    venus = db.FloatField()
    mars = db.FloatField()
    jupiter = db.FloatField()
    saturn = db.FloatField()
    uranus = db.FloatField()
    neptune = db.FloatField()
    pluto = db.FloatField()


class Event(db.Document):
    name = db.StringField()
    local = db.StringField()
    date = db.DateTimeField()
    coord = db.PointField()
    birth = db.EmbeddedDocumentField(Chart)
    
    def __unicode__(self):
        return u"<{name} {date} {coord}>".format(**self.__dict__['_data'])
        
    def __lt__(self, other):
        return self.name.__lt__(other.name)
    
