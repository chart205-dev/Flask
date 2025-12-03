from app import create_app
from app.db.cache_item import load_item_cache

if __name__ == "__main__":
	app = create_app('development')
	load_item_cache(app)
	app.run(debug=True)