from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


fav_Planets = db.Table('fav_Planets',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planets_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True)
)


fav_People = db.Table('fav_People',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    fav_Planets = db.relationship('Planets', secondary=fav_Planets, lazy='subquery', backref=db.backref('user', lazy=True))
    fav_People = db.relationship('People', secondary=fav_People, lazy='subquery', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    height = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return '<People %r>' %self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,           
        }


class Planets(db.Model):
    __tablename__ = "planets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.String(100), nullable=False)
    terrain = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain, 
        }



# class FavPeople(db.Model):
#     __tablename__ = "favPeople"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
#     user = db.relationship(User)
#     people = db.relationship(People)

#     def __repr__(self):
#         return '<FavPeople %r>' % self.name

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,
#             "people_id": self.people_id,
#         }



# class FavPlanet(db.Model):
#     __tablename__ = "favPlanet"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
#     user = db.relationship(User)
#     planet = db.relationship(Planets)

#     def __repr__(self):
#         return '<FavPlanet %r>' % self.name

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,
#             "planet_id": self.planet_id,
#         }