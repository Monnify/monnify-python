from marshmallow import Schema, fields, validates_schema, ValidationError, validate

from validators import is_numeric



class BVNVerificationSchema(Schema):

   bvn = fields.Str(required=True, validate=[validate.Length(min=11, max=11), is_numeric]) 
   name = fields.Str(required=True)
   mobileNo = fields.Str(required=True,validate=[validate.Length(min=11, max=11), is_numeric])
   dateOfBirth = fields.Str(required=True)


class BVNMatchSchema(Schema):
    
   bvn = fields.Str(required=True, validate=[validate.Length(min=11, max=11), is_numeric]) 
   bankCode = fields.Str(required=True, validate=[is_numeric])
   accountNumber = fields.Str(required=True,validate=[validate.Length(min=10, max=10), is_numeric])


class NINVerificationSchema(Schema):
    
   nin = fields.Str(required=True, validate=[validate.Length(min=11, max=11), is_numeric]) 