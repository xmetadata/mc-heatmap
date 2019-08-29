# -*- coding: UTF-8 -*-
from app import app
from common.utils import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models.users import UsersModel
from models.options import OptionsModel
from models.projects import ProjectsModel

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
