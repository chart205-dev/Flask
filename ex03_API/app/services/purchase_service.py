from app.db.create_database import db
from app.models.purchase_model import Purchase
from sqlalchemy.exc import SQLAlchemyError
from app.db.cache_item import get_item_cache

class PurchaseService:
    @staticmethod
    def map_item_name_to_id(item_name):
        try:
            item_cache = get_item_cache()
            if item_name in item_cache:
                return item_cache[item_name]
            else:
                raise Exception('Item not found in cache')
        except Exception as e:
            raise Exception(f'Item mapping error: {str(e)}')

    @staticmethod
    def create_purchase(item_id, quantity=None):
        try:
            new_purchase = Purchase(item_id=item_id, quantity=quantity)
            db.session.add(new_purchase)
            db.session.commit()
            return new_purchase
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f'Purchase creation error: {str(e)}')

    @staticmethod
    def get_all_purchases():
        try:
            purchases = Purchase.query.order_by(Purchase.purchased_at.desc()).all()
            return purchases
        except SQLAlchemyError as e:
            raise Exception(f"Purchase retrieval error: {str(e)}")

    @staticmethod
    def get_purchase_by_id(purchase_id):
        try:
            purchase = Purchase.query.get(purchase_id)
            return purchase
        except SQLAlchemyError as e:
            raise Exception(f"Purchase retrieval error: {str(e)}")

    @staticmethod
    def update_purchase(purchase_id, item_name=None, quantity=None):
        try:
            purchase = Purchase.query.get(purchase_id)
            if purchase is None:
                return None
            if item_name is not None:
                purchase.item_name = item_name
                item_cache = get_item_cache()
                if item_name in item_cache:
                    purchase.item_id = item_cache[item_name]
                else:
                    raise Exception('Item not found in cache')
            if quantity is not None:
                purchase.quantity = quantity
            db.session.commit()
            return purchase
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Purchase update error: {str(e)}")

    @staticmethod
    def delete_purchase(purchase_id):
        try:
            purchase = Purchase.query.get(purchase_id)
            if purchase is None:
                return False
            db.session.delete(purchase)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Purchase deletion error: {str(e)}")
