# -*- coding: UTF-8 -*-
from uuid import uuid1
import json

from flask_sqlalchemy import SQLAlchemy

# instantiate database
db = SQLAlchemy()


class CRUD():
    def add(self, resource):
        db.session.add(resource)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        db.session.commit()

def StandardResponse(code = 200, errcode = 0, errmsg = '', data = None):
    instance = {'errcode': errcode, 'errmsg': errmsg, 'data': ''}
    if errcode == 0 and data:
        instance['data'] = data
    return json.dumps(instance), code


def pretty_response(code, data=None):
    message = {
        200: "OK",
        20001: "Create Success",
        20002: "Update Success",
        20003: "Delete Success",
        400: "Bad Request",
        40001: "Invalid Request Parameters",
        40002: "Duplicate Creation",
        40003: "Marshmallow Validate Fail",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Resource Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
        50001: "SQLAlchemy Error",
        50002: "External Server Error",
        50003: "Initialize Configuration Error",
    }
    http_code = int(code / 100) if code > 9999 else code
    if data is None:
        return {'message': message[code], 'status_code': code}, http_code
    else:
        return {'data': data}, http_code


def get_uuid():
    return uuid1().hex

