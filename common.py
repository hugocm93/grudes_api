from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info

info = Info(title="Grudes API", version="1.0")
app = OpenAPI(__name__, info = info)
CORS(app)
