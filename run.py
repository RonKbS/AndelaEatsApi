from app.utils import db
from config import get_env
from app import create_app
from flask_script import Manager
from app.utils.auth import Auth
from flask_migrate import Migrate, MigrateCommand

app = create_app(get_env('APP_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)

# Migrations
manager.add_command('db', MigrateCommand)

@app.before_request
def check_token():
	return Auth.check_token()

@app.before_request
def check_location_header():
	return Auth.check_location_header()

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
