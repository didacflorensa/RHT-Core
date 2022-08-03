import falcon
from resources import tumors, pacients
import logging.config
from falcon_multipart.middleware import MultipartMiddleware
from database import db

# LOGGING

app = application = falcon.API(
    middleware=[
        MultipartMiddleware()
    ]
)

db.init()


app.add_route('/tumors', tumors.Tumours())
app.add_route('/pacients', pacients.Pacients())
app.add_route('/pacient/{sap}', pacients.Pacient())
