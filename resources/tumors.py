import falcon
from resources.base_resources import RHTResources
from database import db
import mysql.connector
from resources import tumors, pacients
import json
from datetime import datetime


class Tumours(RHTResources):
    def on_get(self, req, resp, *args, **kwargs):
        super(Tumours, self).on_get(req, resp, *args, **kwargs)

        cursor = db._mysql_session.cursor()

        cursor.execute("SELECT sap, dni, cip, sexe, id_tumor, DATE_FORMAT(data_inc_hosp, '%d/%m/%Y') as data_inc_hosp, DATE_FORMAT(data_inc_pobl, '%d/%m/%Y') as data_inc_pobl, DATE_FORMAT(data_mostra, '%d/%m/%Y') as data_mostra, metode_dx, ltum3, morf, centre, revisat FROM tumors ORDER BY sap")

        myresult = cursor.fetchall()

        result = []
        service = pacients.Service()

        for x in myresult:
            sap_s = service.parse_sap_id(x[0])
            tumor = {
                "sap": sap_s,
                "dni": x[1],
                "cip": x[2],
                "sexe": x[3],
                "id_tumor": x[4],
                "data_inc_hosp": x[5],
                "data_inc_pobl": x[6],
                "data_mostra": x[7],
                "metode_dx": x[8],
                "ltum3": x[9],
                "morf": x[10],
                "centre": x[11],
                "revisat": x[12]
            }
            result.append(tumor)


        if len(myresult) > 0:
            rankingJSON = json.dumps(result)

            resp.status = falcon.HTTP_200
            resp.body = rankingJSON
        else:
            resp.status = falcon.HTTP_200
            resp.body = ("None")

    def on_post(self, req, resp, *args, **kwargs):
        super(Tumours, self).on_get(req, resp, *args, **kwargs)
        print("In post")
        
        services = Services()
        print(req.media)

        try:
            id_tumor = req.media["id_tumor"]
            data_inc_hosp = req.media["data_inc_hosp"]
            data_inc_pobl = req.media["data_inc_pobl"]
            data_mostra = req.media["data_mostra"]
            metode_dx = req.media["metode_dx"]
            ltum3 = req.media["ltum3"]
            morf = req.media["morf"]
            revisat = "X"

            cursor = db._mysql_session.cursor()

            cursor.callproc('update_tumor',(id_tumor, data_inc_hosp, data_inc_pobl, data_mostra, metode_dx, ltum3, morf, revisat))

            data = cursor.fetchall()
            
            if(len(data) is 0):
                db._mysql_session.commit()

                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"response:": "OK"})
            else:
                resp.status = falcon.HTTP_404
                resp.body = json.dumps({"response:": "FAIL"})

        except:
            raise falcon.HTTPBadRequest(description="Error updating patient")

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"response:": "OK"})

class Services:
    def convert_to_date(data_ps):
        if data_ps != '':
            return datetime.strptime(data_ps, '%y-%m-%d')
        else:
            return ""