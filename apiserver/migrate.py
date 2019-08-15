# -*- coding: UTF-8 -*-
from app import app
from common.utils import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models.users import UsersModel
from models.province_dict import ProvinceModel
from models.city_dict import CityModel
from models.district_dict import DistrictModel

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
