from .database import db

class Parking_lot(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    prime_location_name = db.Column(db.String())
    Price = db.Column(db.Integer)
    Address = db.Column(db.String())
    Pin_code = db.Column(db.Integer , nullable = False)
    maximum_number_of_spots = db.Column(db.Integer)
    spot = db.relationship('Parking_spot' , backref = 'bearer')

class Parking_spot(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id') ,nullable = False)
    status = db.Column(db.String(), default = 'available')

class Reserve_parking_spot(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    # user_id = db.Column(db.Integer , db.ForeignKey('users.id'), nullable= False)
    parking_timestamp = db.Column(db.Numeric() )
    leaving_timestamp = db.Column(db.Numeric())
    parking_cost = db.Column(db.Integer)

class Users(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(),nullable = False)
    email = db.Column(db.String(),nullable = False, unique = True)
    password = db.Column(db.String(),nullable = False)
    address = db.Column(db.String())
    pincode = db.Column(db.Integer)
    type = db.Column(db.String() ,nullable = False ,default = "general")