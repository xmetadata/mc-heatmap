# -*- coding: UTF-8 -*-
from app import app
from common.utils import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models.users import UsersModel
from models.options import OptionsModel
from models.province_dict import ProvinceModel
from models.city_dict import CityModel
from models.district_dict import DistrictModel
from models.housing_type_dict import HousingTypeModel
from models.project_property import PropertyModel
from models.total_area_dict import TotalAreaModel
from models.unit_price_dict import UnitPriceMode
from models.total_price_dict import TotalPriceModel
#from models.project_detail_data import ProjectDetailModel
from models.project_infomation_data import ProjectInfomationModel

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
