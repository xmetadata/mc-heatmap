# -*- coding: UTF-8 -*-
from datetime import datetime

from marshmallow import Schema, fields, post_load
from werkzeug.security import check_password_hash, generate_password_hash

from common.utils import CRUD, db, get_uuid


class UsersModel(db.Model, CRUD):
    __tablename__ = "users"

    id = db.Column(db.String(32), default=get_uuid, primary_key=True)
    username = db.Column(db.String(128))
    hash_password = db.Column(db.String(128))
    roles = db.Column(db.String(32), default='user')
    status = db.Column(db.Integer, default=1)
    createtime = db.Column(db.DateTime, default=datetime.now)
    updatetime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def password(self):
        raise AttributeError('password cannot be read')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def confirm_password(self, password):
        return check_password_hash(self.hash_password, password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter(cls.username==username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.id==id).first()


class UsersSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String()
    password = fields.String(load_only=True)
    roles = fields.String()
    status = fields.Integer(dump_only=True)
    createtime = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    updatetime = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
