from app.db.create_database import db
from app.models.purchase_model import Purchase
from sqlalchemy.exc import SQLAlchemyError


class PurchaseService:
    @staticmethod
    def create_purchase(purchase, quantity=None):
        try:
            new_purchase = Purchase(purchase=purchase, quantity=quantity)
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
    def update_purchase(purchase_id, purchase=None, quantity=None):
        try:
            purchase = Purchase.query.get(purchase_id)
            if purchase is None:
                return None
            if purchase is not None:
                purchase.purchase = purchase
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
