from flask_script import Manager
from flask import request
from flask_migrate import Migrate, MigrateCommand
from app import create_app  #, controllers
from app.utils import db
from config import get_env

app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)

# Migrations
manager.add_command('db', MigrateCommand)

# Creates the db tables
@manager.command
def create_db():
	db.create_all()

# Drops the db tables
@manager.command
def drop_db():
	db.drop_all()

if __name__ == '__main__':
	manager.run()
