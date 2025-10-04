from flask import current_app as app, render_template, request, redirect
from backend.models import *
from flask_login import login_user,login_required,current_user


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
        

@app.route("/dashboard/sp")
@login_required
def dash_sp():
    if isinstance(current_user,ServiceProvider):
        return f"Welcome to Service Provider Dashbord{current_user.email}"
    else:
        return "error"

@app.route("/dashboard/cust")
@login_required
def dash_cust():
    if isinstance(current_user,Customer):
        return f"Welcome to Customer Dashbord{current_user.email}"
    else:
        return "error"

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

    






