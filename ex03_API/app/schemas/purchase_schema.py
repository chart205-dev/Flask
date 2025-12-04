from marshmallow import Schema, fields, validate, ValidationError, validates
from app.models.item_model import Item  

class PurchaseSchema(Schema):
    id = fields.Int(dump_only=True)
    
    item_name = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': 'item_name is required.'
            }
    ) 
    
    item_id = fields.Int(required=False)

    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            'validator_failed': 'Please set it to 1 or more.'
        }
    )

    purchased_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)
