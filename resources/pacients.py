import falcon
from resources.base_resources import RHTResources
from database import db
import json

class Pacients(RHTResources):
    def on_get(self, req, resp, *args, **kwargs): # TODO Get pacient information for all the registers
        super(Pacients, self).on_get(req, resp, *args, **kwargs)

        cursor = db._mysql_session.cursor()

        cursor.execute("SELECT sap, dni, cip, sexe FROM tumors GROUP BY sap, dni, cip, sexe")

        myresult = cursor.fetchall()

        result = []
        service = Service()
        for x in myresult:
            sap_s = service.parse_sap_id(x[0])
            pacient = {
                "sap": sap_s,
                "dni": x[1],
                "cip": x[2],
                "sexe": x[3],
            }
            result.append(pacient)


        if len(myresult) > 0:
            rankingJSON = json.dumps(result)

            resp.status = falcon.HTTP_200
            resp.body = rankingJSON
        else:
            resp.status = falcon.HTTP_200
            resp.body = ("None")
    

class Pacient(RHTResources):
    def on_get(self, req, resp, *args, **kwargs): # TODO Get specific pacient information
        super(Pacient, self).on_get(req, resp, *args, **kwargs)

        print(kwargs)
        if "sap" in kwargs:
            print("in pacient")
            print(kwargs["sap"])
            try:
                
                cursor = db._mysql_session.cursor()
                cursor.execute("SELECT sap, dni, cip, sexe FROM tumors WHERE sap = " + kwargs["sap"] + " GROUP BY sap, dni, cip, sexe")

                request = cursor.fetchall()

                patient = {}
                for element in request:
                    patient = {
                        "sap": element[0],
                        "dni": element[1],
                        "cip": element[2],
                        "sexe": element[3],
                    }

                resp.status = falcon.HTTP_200
                rankingJSON = json.dumps(patient)
                resp.body = rankingJSON

            except:
                raise falcon.HTTPBadRequest(description="No existeix pacient")


        else:
            raise falcon.HTTPMissingParam("sap")

    def on_post(self, req, resp, *args, **kwargs): # TODO Modify specific pacient information
        super(Pacient, self).on_get(req, resp, *args, **kwargs)

        resp.status = falcon.HTTP_200
        resp.body = ("This is me, Falcon, in post pacient")



# Add 0 to sap id to convert it to an id of 10 elements
class Service:
    def parse_sap_id(self, sap):
        sap_s = str(sap)
        while len(sap_s) < 10:
            sap_s = "0" + sap_s
        return sap_s