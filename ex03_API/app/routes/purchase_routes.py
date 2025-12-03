from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.purchase_service import PurchaseService
from app.schemas.purchase_schema import purchase_schema, purchases_schema
from app.models.item_model import Item

# Blueprint for /purchases
purchase_bp = Blueprint('purchases', __name__, url_prefix='/purchases')


@purchase_bp.route('', methods=['POST'])
def create_purchase():
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'Request body is empty'}), 400

        validated_data = purchase_schema.load(data)
        
        item_name = validated_data.get('item_name') or validated_data.get('purchase_name')
        if not item_name:
            return jsonify({'error': 'item_name is required'}), 400

        item = Item.query.filter_by(item_name=item_name).first()
        if item is None:
            return jsonify({'error': 'Item not found'}), 400

        new_purchase = PurchaseService.create_purchase(
            item_id=item.id,
            quantity=validated_data.get('quantity')
        )
        
        result = purchase_schema.dump(new_purchase)
        
        return jsonify(result), 201
    
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@purchase_bp.route('', methods=['GET'])
def get_all_purchases():
    try:
        purchases = PurchaseService.get_all_purchases()
        result = purchases_schema.dump(purchases)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@purchase_bp.route('/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    try:
        purchase = PurchaseService.get_purchase_by_id(purchase_id)
        if purchase is None:
            return jsonify({'error': 'Purchase not found'}), 404
        
        result = purchase_schema.dump(purchase)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @purchase_bp.route('/<int:purchase_id>', methods=['PUT'])
# def update_purchase(purchase_id):
#     try:
#         data = request.get_json()
#         if data is None:
#             return jsonify({'error': 'Request body is empty'}), 400
        
#         validated_data = purchase_schema.load(data, partial=True)
        
#         updated_purchase = PurchaseService.update_purchase(
#             purchase_id=purchase_id,
#             purchase_name=validated_data.get('purchase_name'),
#             price=validated_data.get('price')
#         )
        
#         if updated_purchase is None:
#             return jsonify({'error': 'Purchase not found'}), 404
        
#         result = purchase_schema.dump(updated_purchase)
#         return jsonify(result), 200
    
#     except ValidationError as e:
#         return jsonify({'error': e.messages}), 400
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @purchase_bp.route('/<int:purchase_id>', methods=['DELETE'])
# def delete_purchase(purchase_id):
#     try:
#         success = PurchaseService.delete_purchase(purchase_id)
#         if not success:
#             return jsonify({'error': 'Purchase not found'}), 404
        
#         return jsonify({'message': 'Purchase deleted successfully'}), 200
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
