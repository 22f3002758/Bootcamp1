from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


class Admin(db.Model):
    __tablename__='admin'

    id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    admin_name=db.Column(db.String)
    email=db.Column(db.String,unique=True)
    password=db.Column(db.String,unique=True)
    


    
class ServiceProvider(db.Model):
    __tablename__='serviceprovider'

    id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    name=db.Column(db.String,unique=True)
    address=db.Column(db.String)
    email=db.Column(db.String,unique=True)
    password=db.Column(db.String)
    exp=db.Column(db.Integer)
    phone=db.Column(db.String)
    city=db.Column(db.String)
    
    status=db.Column(db.String)
    servicename=db.Column(db.String,db.ForeignKey("services.name"))
    receive_request=db.relationship("Request",backref="servprovider",cascade="all, delete-orphan")
    



class Customer(db.Model):
    __tablename__="customer" 

    id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    name=db.Column(db.String,unique=True)
    address=db.Column(db.String)
    city=db.Column(db.String) 
    email=db.Column(db.String,unique=True)
    password=db.Column(db.String)
    phone=db.Column(db.String) 
    status=db.Column(db.String)
    Sent_Request=db.relationship("Request",backref="cust")
   

class Services(db.Model):
    __tablename__="services"

    id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    name=db.Column(db.String,unique=True)
    baseprice=db.Column(db.Integer)
    description=db.Column(db.String)
    Sproviders=db.relationship("ServiceProvider",backref="service", cascade="all, delete-orphan")



class Request(db.Model):
    __tablename__="request"

    r_id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    sp_id=db.Column(db.Integer, db.ForeignKey("serviceprovider.id"),nullable=False)
    c_id=db.Column(db.Integer, db.ForeignKey("customer.id"),nullable=False)
    
    r_date=db.Column(db.String)
    r_time=db.Column(db.String)
    r_address=db.Column(db.String)
    r_city=db.Column(db.String)
    r_status=db.Column(db.String)
    r_rating=db.Column(db.Integer)



# class Request(db.Model):
#     __tablename__="request"

#     r_id=db.Column(db.Integer, primary_key=True, autoincrement= True)
#     sp_id=db.Column(db.Integer, db.ForeignKey("serviceprovider.id"),nullable=False)
#     c_id=db.Column(db.Integer, db.ForeignKey("customer.id"),nullable=False)
    
#     r_date=db.Column(db.String)
#     r_time=db.Column(db.String)
#     r_address=db.Column(db.String)
#     r_city=db.Column(db.String)
#     r_status=db.Column(db.String)
    