from flask import Flask
from flask_login import LoginManager
from backend.models import *

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mydb.sqlite3"
    db.init_app(app)
    app.config["SECRET_KEY"]="mysecretkey"
    loginmanager=LoginManager(app)
    @loginmanager.user_loader
    def load_user(email):
        obj=db.session.query(ServiceProvider).filter_by(email=email).first() or db.session.query(Customer).filter_by(email=email).first() or db.session.query(Admin).filter_by(email=email).first()
        return obj
    app.app_context().push()
    
    return app

app=create_app()
from backend.create_initialdata import *
from backend.routes import *


if __name__=="__main__":
    app.run(debug=True)
    





