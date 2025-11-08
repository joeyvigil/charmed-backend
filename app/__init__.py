from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.users import users_bp
from .blueprints.matches import matches_bp
from .blueprints.messages import messages_bp


from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic Shop API - Joseph Vigil"
    }
)

def create_app(config_name):

    app = Flask(__name__) #Creating base app
    app.config.from_object(f'config.{config_name}')
    CORS(app) #added CORS

    #initialize extensions (plugging them in)
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    #Register blueprints 
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(matches_bp, url_prefix='/matches')
    app.register_blueprint(messages_bp, url_prefix='/messages')
    
    #Registering our swagger blueprint
    # app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) 


    return app