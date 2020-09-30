from restaurants_app import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
import pandas
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


# SQL Alchemy setup

# Creating the engine that will allow us
engine = create_engine("mysql://root@localhost/restaurant.db", ecoding='utf-8', echo=True)
# Creating the Session which is the middle ground to talk to our engine
Session = db.sessionmaker(bind=engine)
session = Session()

# Map which table in the database will be related to each class

Base = declarative_base()
# Create a metadata instance
metadata = MetaData(engine)


class Restaurant_table(db.Model):
    """Create Restaurant Table """

    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    site = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    street = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    lat = db.Column(db.Float)
    lngtd = db.Column(db.Float)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, restaurant_id, name, site,
                 email, phone, street, city, state, lat, lngitd):
        self.restaurant_id = restaurant_id
        self.name = name
        self.site = site
        self.email = email
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.lat = lat
        self.lngt = lngitd

    def __repr__(self):
        return f'{self.restaurant_id, self.name, self.site, self.email, self.phone, self.street} +\
         {self.city, self.state, self.lat}'


# Here we can make switch with the instance of db from flask
def table_definition(table_name):
    table_definition.table_define = db.Table(
        table_name,
        metadata,
        db.Column('restaurant_id', db.Integer, primary_key=True),
        db.Column('name', db.Integer),
        db.Column('rating', db.String),
        db.Column('site', db.String),
        db.Column('email', db.String),
        db.Column('phone', db.String),
        db.Column('street', db.String),
        db.Column('city', db.String),
        db.Column('state', db.String),
        db.Column('lat', db.Float),
        db.Column('lngtd', db.Float)
    )
    metadata.create_all(engine)
    mapper(Restaurant_table, table_definition.table_define, non_primary=True)


# Here we can define a dummy_table
table_define_dummy = db.Table(
    'dummy_table', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('name', db.String),
    db.Column('rating', db.String),
    db.Column('site', db.String),
    db.Column('email', db.String),
    db.Column('phone', db.String)
)
metadata.create_all(engine)
mapper(Restaurant_table, table_define_dummy)


def create_table(file_name):
    """Function to create the table from a csv type of file"""
    csv_data = pandas.read_csv(file_name)
    csv_data = csv_data.values.tolist()
    table_name_from_file = file_name.split('/')[8][:-4]

    # Here we call the subroutine as the last
    table_definition(table_name_from_file)
    # Loop as the next manner over the rows
    for row in csv_data:
        ins = table_definition.table_define.insert().values(
            restaurant_id=row[0], name=row[1], rate=row[2],
            site=row[3], email=row[3], city=row[4], state=row[5],
            lat=row[6], lngtd=row[7],
        )
        conn = engine.connect()
        conn.execute(ins)


class SchemaRestaurant(ModelSchema):
    """This is a class for abstract the object from the database to a json objects in the app"""

    class Meta(ModelSchema.Meta):
        mode = Restaurant_table
        sql_session = session

    restaurant_id = fields.Integer
    restaurant_name = fields.String
    restaurant_email = fields.String
    restaurant_phone = fields.String
    restaurant_site = fields.String
    restaurant_street = fields.String
    restaurant_city = fields.String
    restaurant_state = fields.String
    restaurant_lttd = fields.Float
    restaurant_lngtd = fields.Float


# Creating the table from specific file
create_table("/home/erick-hdz/Intelimetrica_test/restaurantes.csv")
