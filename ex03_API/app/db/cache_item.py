from app.models.item_model import Item, db

# グローバル変数でキャッシュを保持
item_cache = {}

def load_item_cache(app):
    global item_cache
    with app.app_context():
        items = Item.query.all()
    item_cache = {item.item_name: item.id for item in items}
    print("Item cache loaded:", item_cache)

