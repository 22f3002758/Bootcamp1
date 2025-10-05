from flask import current_app as app
from .models import *

with app.app_context():
    db.create_all()
    if db.session.query(Services).count()==0:
        srv1=Services(name="Home Cleaning",baseprice=500,description="Home Cleaning Category")
        srv2=Services(name="Home Decor",baseprice=500, description="Home Decor Category")
        db.session.add_all([srv1,srv2])
        db.session.commit()
        
    if db.session.query(ServiceProvider).count()==0:
        sp1=ServiceProvider(email="sp1@gmail.com",password="asdf",servicename='Home Cleaning',status="Active")
        sp2=ServiceProvider(email="sp2@gmail.com",password="asdf",servicename='Home Cleaning',status="Active")
        sp3=ServiceProvider(email="sp3@gmail.com",password="asdf",servicename='Home Decor',status="Active")
        sp4=ServiceProvider(email="sp4@gmail.com",password="asdf",servicename='Home Decor',status="Flagged")
        db.session.add_all([sp1,sp2,sp3,sp4])
        db.session.commit()   
    if db.session.query(Admin).count()==0: 
        ad=Admin(email="admin@gmail.com",password="asdf")  
        db.session.add(ad)
        db.session.commit() 
    if db.session.query(Customer).count()==0: 
        cust=Customer(email="cust1@gmail.com",password="asdf",name='Rahul',status='Active')   
        db.session.add(cust)
        db.session.commit() 
        
    if db.session.query(Request).count()==0:
        req=Request(sp_id=1,c_id=1,r_status="Completed",r_date="25-08-2025")    
        db.session.add(req)
        db.session.commit()

    ##accessing variables of ServiceProvider's table (Child) from Services table (parent) 
    # srv1=db.session.query(Services).filter_by(id=1).first()
    # Sprvd=srv1.Sproviders
    # print(Sprvd[0].name)

    
    
    # accessing services table data from serviceprovider table
    # spobj=db.session.query(ServiceProvider).filter_by(id=1).first()
    # servname=spobj.service.name
    # print(servname)




