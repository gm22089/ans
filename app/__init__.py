from flask import Flask

def create_app():
    app=Flask(__name__)
    
    #registros de blueprints
    from .unidad2 import unidad2 as unidad2_blueprint
    app.register_blueprint(unidad2_blueprint, url_prefix='/unidad2')

    return app