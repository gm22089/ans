from flask import Blueprint

unidad2=Blueprint('unidad2', __name__, template_folder="templates")

# Importar las vistas después de definir el blueprint
from . import views