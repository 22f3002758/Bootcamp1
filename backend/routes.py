from flask import current_app as app, render_template, request, redirect
from backend.models import *


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
            return redirect("/dashboard/sp")
        elif cust_obj and cust_obj.password==fpwd:
            return redirect("/dashboard/cust")
        elif ad_obj and ad_obj.password==fpwd:
            return redirect("/dashboard/ad")
        else:
            return "check your crendentials"
        

@app.route("/dashboard/sp")
def dash_sp():
    return "Welcome to Service Provider Dashbord"

@app.route("/dashboard/cust")
def dash_cust():
    return "Welcome to Customer Dashbord"

@app.route("/dashboard/ad")
def dash_ad():
    return "Welcome to Admin Dashbord"

