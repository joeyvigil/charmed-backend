from app.models import db
from app import create_app

app = create_app('ProductionConfig') # 1. change to 'ProductionConfig' as needed

with app.app_context():
    db.drop_all() # 2. uncomment to reset database
    db.create_all() 

# app.run() # 3. remove when deploying to production server