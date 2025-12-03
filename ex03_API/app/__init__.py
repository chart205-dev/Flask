from flask import Flask
from app.config import config
from app.db.create_database import init_db
from app.routes.item_routes import item_bp
from app.routes.purchase_routes import purchase_bp



def create_app(config_name='development'):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	init_db(app)
	app.register_blueprint(item_bp)
	app.register_blueprint(purchase_bp)

	return app
