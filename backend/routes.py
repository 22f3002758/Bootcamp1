from flask import current_app as app, render_template, request, redirect
from backend.models import *
from flask_login import login_user,login_required,current_user,logout_user
from sqlalchemy import and_,or_
from datetime import datetime,timedelta

@app.route("/",methods=["GET","POST"])
def home():

    return render_template("home.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("cust_register.html")
    elif request.method=="POST":
        print("Hello")
        fname=request.form.get("cname") #cname is a variable we have used it in html form name="cname"
        femail=request.form.get("cemail")
        fpwd=request.form.get("cpwd")
        fcity=request.form.get("ccity")
        fphone=request.form.get("cphone")
        fadd=request.form.get("caddress")
        cust_obj=db.session.query(Customer).filter_by(email=femail).first()
        print(cust_obj)
        if not cust_obj:
            custdata=Customer(name=fname,email=femail,password=fpwd,city=fcity,phone=fphone,address=fadd)
            db.session.add(custdata)
            db.session.commit()
            return redirect("/login")
        else:   
            return "User alrerady exist" 


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    if request.method=="POST":
        femail=request.form.get("email")
        fpwd=request.form.get("pwd")
        sp_obj=db.session.query(ServiceProvider).filter_by(email=femail).first()
        cust_obj=db.session.query(Customer).filter_by(email=femail).first()
        ad_obj=db.session.query(Admin).filter_by(email=femail).first()
        if sp_obj and sp_obj.password==fpwd:
            login_user(sp_obj)
            return redirect("/dashboard/sp")
        elif cust_obj and cust_obj.password==fpwd:
            login_user(cust_obj)
            return redirect("/dashboard/cust")
        elif ad_obj and ad_obj.password==fpwd:
            login_user(ad_obj)
            return redirect("/dashboard/ad")
        else:
            return "check your crendentials"
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")        

@app.route("/dashboard/sp")
@login_required
def dash_sp():
    if isinstance(current_user,ServiceProvider) and request.method=="GET":
        reqobj=current_user.receive_request
        return render_template("serviceprovider/spdash.html",requests=reqobj)
    else:
        return "Unauthorized to access this page."

def nextsevendates():
    today=datetime.now().date()
    L=[]
    for i in range(7):
        L.append(today+timedelta(days=i))
    return L    
def get_fixedslots():

    fixed_slots=[('09:00','10:00'),('10:00','11:00'),('11:00','12:00'),('12:00','13:00'),('15:00','16:00'),('16:00','17:00'),('17:00','18:00')]
    L=[]
    for fs in fixed_slots:
        L.append((datetime.strptime(fs[0],'%H:%M').time(),datetime.strptime(fs[1],'%H:%M').time()))
    return L

@app.route("/availability/sp",methods=["GET","POST"])
def availability():
    if request.method=="GET":
        L=[]
        nextsevendays=nextsevendates()
        fixedslots=get_fixedslots()
        existing_slots=db.session.query(ProvidersAvailability).filter(ProvidersAvailability.sp_id==current_user.id,ProvidersAvailability.date>=datetime.now().date()).all()
        for day in nextsevendays:
            slot_list=[]
            for start,end in fixedslots:

                if any(es.date==day and es.start_time==start and es.end_time == end and es.status=='Booked' for es in existing_slots ):
                    slot_list.append({'start_time':start,'end_time':end,'status':'Booked'})
                elif any(es.date==day and es.start_time==start and es.end_time == end and es.status=='Available' for es in existing_slots ):
                    slot_list.append({'start_time':start,'end_time':end,'status':'Selected'})    
                else:
                    slot_list.append({'start_time':start,'end_time':end,'status':'Not Selected'})

            L.append({'date':day,'slots':slot_list})
            ##L=[{'date':value,'slots':slot_list}]
            #slot_list=[{'start_time':value,'end_time':value,'status':value}]
            print(L)
          
        return render_template("serviceprovider/availability.html",all_slots=L)  
    
    elif request.method=="POST":
        selected_slots=request.form.getlist("slot")
        db.session.query(ProvidersAvailability).filter(ProvidersAvailability.sp_id==current_user.id,ProvidersAvailability.status=='Available',
                                                       ProvidersAvailability.date>=datetime.now().date()).delete(synchronize_session=False)
        db.session.commit()
        for s in selected_slots:
            avail_date,start_time,end_time=s.split("_")
            avail_date=datetime.strptime(avail_date,"%Y-%m-%d").date()
            start_time=datetime.strptime(start_time,'%H:%M').time()
            end_time=datetime.strptime(end_time,'%H:%M').time()
            pa=ProvidersAvailability(sp_id=current_user.id,date=avail_date,start_time=start_time,end_time=end_time,status='Available')
            db.session.add(pa)
            db.session.commit()
        return redirect("/dashboard/sp")    


@app.route("/dashboard/cust")
@login_required
def dash_cust():
    if isinstance(current_user,Customer) and request.method=="GET":
        reqs=current_user.Sent_Request
        servobjs=db.session.query(Services).all()
        return render_template("customer/custdash.html",requests=reqs,services=servobjs)
    else:
        return "error"
    
@app.route("/service/<servicename>")
def service(servicename):
    if request.method=="GET":
        sps=db.session.query(ServiceProvider).filter_by(servicename=servicename).all()
    return render_template("customer/service.html",sps=sps)    


@app.route("/slotbooking",methods=["GET","POST"])
def booking():
    if request.method=="GET":
        id=request.args.get("id")
        paobj=db.session.query(ProvidersAvailability).filter(
        ProvidersAvailability.sp_id==id,
        ProvidersAvailability.status=='Available',
        or_(
            ProvidersAvailability.date>datetime.now().date(), #future dates
            and_(
                ProvidersAvailability.date==datetime.now().date(), # same day
                ProvidersAvailability.start_time>=datetime.now().time() # after current tiome
            )
        )
        )
        d={}
        for pa in paobj:
            if pa.date not in d:
                d[pa.date]=[pa]
            else:
                d[pa.date].append(pa)
        return render_template("customer/availableslots.html",all_slots=d)  

    elif request.method=="POST":
        slotstring=request.form.get("slot")
        book_date,start_time,end_time,slot_id=slotstring.split("_")    
        book_date=datetime.strptime(book_date,"%Y-%m-%d").date()
        start_time=datetime.strptime(start_time,'%H:%M').time()
        end_time=datetime.strptime(end_time,'%H:%M').time()   
        paobj=db.session.query(ProvidersAvailability).filter_by(id=slot_id).first()

        spid=paobj.sp_id
        req=Request(slot_id=slot_id,r_date=book_date,start_time=start_time,end_time=end_time,sp_id=spid,c_id=current_user.id,r_status='Booked') 
        paobj.status='Booked'
        db.session.add(req)
        db.session.commit()
        return redirect("dashboard/cust")
    
@app.route('/managerequest', methods=["GET","POST"])
def cancelbooking():
    if request.method=="GET" and request.args.get("action")=='cancel':
        reqid=request.args.get('id')
        reqobj=db.session.query(Request).filter_by(r_id=reqid).first()
        reqobj.r_status="Cancelled"
        # slot_id=reqobj.slot_id
        paobj=db.session.query(ProvidersAvailability).filter_by(id=reqobj.slot_id).first()
        paobj.status='Available'
        db.session.commit()
        if isinstance(current_user,Customer):
            return redirect("dashboard/cust")
        if isinstance(current_user,ServiceProvider):
            return redirect("dashboard/sp")
        
    elif request.method=="GET" and request.args.get("action")=='complete':    
        reqid=request.args.get("id")
        reqobj=db.session.query(Request).filter_by(r_id=reqid).first()
        reqobj.r_status="Completed"
        paobj=db.session.query(ProvidersAvailability).filter_by(id=reqobj.slot_id).first()
        paobj.status='Completed'
        db.session.commit()
        return redirect("dashboard/sp")




        

@app.route("/dashboard/ad")
@login_required
def dash_ad():
    if isinstance(current_user,Admin):
        sp=db.session.query(ServiceProvider).all() #<serviceprovider1><serviceprovider2>
        cust=db.session.query(Customer).all()
        services=db.session.query(Services).all()
        return render_template("admin/admindash.html",sps=sp, customers=cust,services=services)
    else:
        return "error"
    
@app.route("/createservices",methods=["GET","POST"])   
def services():
    if request.method=="GET" and request.args.get("action")=="create":
        return render_template("admin/createservices.html")
    elif request.method=="POST" and request.args.get("action")=="create":
        fname=request.form.get("name")
        fbp=request.form.get("baseprice")
        fdesc=request.form.get("desc")
        servobj=db.session.query(Services).filter_by(name=fname).first()
        if not servobj:
            dbserv=Services(name=fname,baseprice=fbp,description=fdesc)
            db.session.add(dbserv)
            db.session.commit()
            return redirect("/dashboard/ad")
        else:
            return redirect("/createservices")  
          
    elif request.method=="GET" and request.args.get("action")=="edit":
        id=request.args.get("id")
        servobj=db.session.query(Services).filter_by(id=id).first()
        return render_template("admin/createservices.html",servobj=servobj)
    
    elif request.method=="POST" and request.args.get("action")=="edit":
        id=request.args.get("id")
        fname=request.form.get("name")
        fbp=request.form.get("baseprice")
        fdesc=request.form.get("desc")
        obj=db.session.query(Services).filter_by(id=id).first()
        if fname:
            obj.name=fname
        if fbp:
            obj.baseprice=fbp
        if fdesc:
            obj.description=fdesc  
        db.session.commit()
        return redirect("/dashboard/ad")  
       
    elif request.method=="GET" and request.args.get("action")=="delete":
        id=request.args.get("id")
        servobj=db.session.query(Services).filter_by(id=id).first()
        db.session.delete(servobj)
        db.session.commit()
        return redirect("dashboard/ad")

            
@app.route("/manageproviders",methods=["GET","POST"])
def manageproviders():
    if request.method=="GET" and request.args.get("action")=="create":
        services=db.session.query(Services).all()
        return render_template("serviceprovider/createsp.html",services=services)
    
    elif request.method=="POST" and request.args.get("action")=="create":
        femail=request.form.get("email")
        fpwd=request.form.get("pwd")
        fname=request.form.get("name")
        fphone=request.form.get("phone")
        fexp=request.form.get("exp")
        fcat=request.form.get("cat")
        spobj=db.session.query(ServiceProvider).filter_by(email=femail).first()
        if not spobj:
            obj=ServiceProvider(name=fname,email=femail,password=fpwd,phone=fphone,exp=fexp,servicename=fcat)
            db.session.add(obj)
            db.session.commit()
            return redirect("/dashboard/ad")
        
    elif request.method=="GET" and request.args.get("action")=="edit":
        
        id=request.args.get("id")
        spobj=db.session.query(ServiceProvider).filter_by(id=id).first()
        
        services=db.session.query(Services).all()
        return render_template("serviceprovider/createsp.html",services=services,spobj=spobj)    
    
    elif request.method=="POST" and request.args.get("action")=="edit":
        id=request.args.get("id")
        spobj=db.session.query(ServiceProvider).filter_by(id=id).first()
        
        fpwd=request.form.get("pwd")
        fname=request.form.get("name")
        fphone=request.form.get("phone")
        fexp=request.form.get("exp")
        fcat=request.form.get("cat")
        
        if fpwd:
            spobj.password=fpwd
        if fname:
            spobj.name=fname
        if fphone:
            spobj.phone=fphone
        if fexp:
            spobj.exp=fexp
        if fcat:
            spobj.servicename=fcat
        db.session.commit()
        return redirect("dashboard/ad")    
     
    elif request.method=="GET" and request.args.get("action")=="delete":
        id=request.args.get("id")
        spobj=db.session.query(ServiceProvider).filter_by(id=id).first()
        db.session.delete(spobj)
        db.session.commit()
        return redirect("dashboard/ad")      

@app.route("/managecust",methods=["GET","POST"])
def managecust():
    id=request.args.get("id")
    custobj=db.session.query(Customer).filter_by(id=id).first()
    if request.args.get("action")=="flag":
        custobj.status="Flagged"
        db.session.commit()
        return redirect("dashboard/ad")
    elif request.args.get("action")=="unflag":
        custobj.status="Active"
        db.session.commit()
        return redirect("dashboard/ad")
    
@app.route("/viewcusthist",methods=["GET","POST"])  
def viewhist(): 
    if request.method=="GET":
        id=request.args.get("id")
        reqobj=db.session.query(Request).filter(and_(Request.c_id==id,Request.r_status=="Completed")).all()
        return render_template("customer/viewcusthistory.html",reqs=reqobj)
    
@app.route("/search/admin",methods=["GET","POST"])
def searchadmin():
    if request.method=="GET":
        return render_template("admin/search.html")   
    elif request.method=="POST":
        qtype=request.form.get("querytype")
        qry=request.form.get("query")
        if qtype=="service" and qry:
            obj=db.session.query(Services).filter(or_(Services.name.ilike(f"%{qry}%"),Services.description.ilike(f"%{qry}%"))).all()
            return render_template("admin/search.html", services=obj,qtype=qtype)
        if qtype=="sp" and qry:
            obj=db.session.query(ServiceProvider).filter(or_(ServiceProvider.name.ilike(f"%{qry}%"),ServiceProvider.email.ilike(f"%{qry}%"))).all()
            return render_template("admin/search.html", sps=obj,qtype=qtype)
        if qtype=="cust" and qry:
            obj=db.session.query(Customer).filter(or_(Customer.name.ilike(f"%{qry}%"),Customer.email.ilike(f"%{qry}%"))).all()
            return render_template("admin/search.html", customers=obj,qtype=qtype)



     


    




