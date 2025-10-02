from flask import Flask

from backend.models import *

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mydb.sqlite3"
    db.init_app(app)
    
    
    app.app_context().push()
    
    return app

app=create_app()
from backend.create_initialdata import *
from backend.routes import *


if __name__=="__main__":
    app.run(debug=True)





