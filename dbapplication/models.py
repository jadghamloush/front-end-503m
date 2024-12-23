from app import db
from flask_login import UserMixin
from datetime import datetime, timedelta

# models.py

class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    invoice_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)  # **New Field**
    status = db.Column(db.String, nullable=False) 

    user = db.relationship('User', backref='invoices')

    def __repr__(self):
        return f"<Invoice #{self.invoice_id} - User: {self.user.username}, Product ID: {self.product_id}, Quantity: {self.quantity}, Date: {self.date}, Total Price: {self.total_price}, Status: {self.status}>"

class Promotion(db.Model):
    _tablename_ = 'promotions'
    
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    old_price = db.Column(db.Float, nullable=False)
    discounted_price = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, default=True)
    
    def _repr_(self):
        return (f"<Promotion {self.id} - {self.product_type} ID: {self.product_id} "
                f"Old Price: {self.old_price} -> New Price: {self.discounted_price}>")
    
    def is_active(self):
        """Check if the promotion is currently active."""
        now = datetime.utcnow()
        if self.active and (self.end_date is None or self.end_date > now):
            return True
        return False
    
    def get_product(self):
        """Retrieve the associated product object."""
        model = globals().get(self.product_type)
        if model:
            return model.query.get(self.product_id)
        return None




# models.py

from app import db
from flask_login import UserMixin
from datetime import datetime, timedelta

# Existing models...

class ReturnRequest(db.Model):
    __tablename__ = 'return_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.invoice_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String, nullable=False)
    reason = db.Column(db.String, nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String, nullable=False, default='Pending')  # Possible statuses: Pending, Approved, Denied, Completed
    refund_amount = db.Column(db.Float, nullable=True)
    replacement_product_id = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)  # **New Field**

    
    
    user = db.relationship('User', backref='return_requests')
    invoice = db.relationship('Invoice', backref='return_requests')
    
    def __repr__(self):
        return f"<ReturnRequest #{self.id} - User ID: {self.user_id}, Invoice ID: {self.invoice_id}, Status: {self.status}>"


    def get_product(self):
        """
        Retrieve the product object associated with this return request based on product_type and product_id.
        """
        model_mapping = {
            'FootwearSubCategory': FootwearSubCategory,
            'ActivewearSubCategory': ActivewearSubCategory,
            'BottomsSubCategory': BottomsSubCategory,
            'OuterwearSubCategory': OuterwearSubCategory,
            'RecoverySubCategory': RecoverySubCategory,
            'AccessoriesSubCategory': AccessoriesSubCategory,
            'SwimwearSubCategory': SwimwearSubCategory,
            'CompressionSubCategory': CompressionSubCategory,
            'SpecialtySportswearSubCategory': SpecialtySportswearSubCategory,
            'ProtectiveGearSubCategory': ProtectiveGearSubCategory
        }
        model = model_mapping.get(self.product_type)
        if model:
            return model.query.get(self.product_id)
        return None




class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_generated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    most_popular_product_id = db.Column(db.Integer, nullable=False)
    most_popular_product_type = db.Column(db.String, nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)  # Total quantity sold of most popular product
    inventory_turnover = db.Column(db.Float, nullable=False)  # Ratio of sales to average inventory
    future_demand = db.Column(db.String, nullable=True)  # Prediction text
    
    def _repr_(self):
        return f"<Report #{self.id} - Date: {self.date_generated}, Most Popular Product ID: {self.most_popular_product_id}>"
        

# models.py

class Cart(db.Model):
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    product_type = db.Column(db.String, nullable=False)  # e.g., 'FootwearSubCategory', 'ActivewearSubCategory', etc.
    product_id = db.Column(db.Integer, nullable=False)   # ID corresponding to the product in its subcategory
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)  # Added price field
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    
    def __repr__(self):
        return f"<CartItem UserID: {self.user_id}, ProductType: {self.product_type}, ProductID: {self.product_id}, Quantity: {self.quantity}, Price: {self.price}>"
    
    def get_product(self):
        try:
            model = globals().get(self.product_type)
            if model:
                return model.query.get(self.product_id)
            return None
        except:
            return None


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String)
    description = db.Column(db.String)
    
    def __repr__(self):
        return f'<User: {self.username},Role: {self.role}>'
    def get_id(self):
        return self.uid

from app import db

# Main Categories
class Footwear(db.Model):
    __tablename__ = 'footwear'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    subcategories = db.relationship('FootwearSubCategory', backref='footwear', lazy=True)
    
    def __repr__(self):
        return f'<Footwear: {self.type}, Quantity: {self.quantity}>'


class ActivewearTops(db.Model):
    __tablename__ = 'activewear_tops'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    subcategories = db.relationship('ActivewearSubCategory', backref='activewear', lazy=True)
    
    def __repr__(self):
        return f'<ActivewearTop: {self.type}, Quantity: {self.quantity}>'


class Bottoms(db.Model):
    __tablename__ = 'bottoms'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    subcategories = db.relationship('BottomsSubCategory', backref='bottoms', lazy=True)
    
    def __repr__(self):
        return f'<Bottom: {self.type}, Quantity: {self.quantity}>'


class Outerwear(db.Model):
    __tablename__ = 'outerwear'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    subcategories = db.relationship('OuterwearSubCategory', backref='outerwear', lazy=True)
    
    def __repr__(self):
        return f'<Outerwear: {self.type}, Quantity: {self.quantity}>'


class RecoveryAndWellness(db.Model):
    __tablename__ = 'recovery_and_wellness'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    subcategories = db.relationship('RecoverySubCategory', backref='recovery', lazy=True)
    
    def __repr__(self):
        return f'<RecoveryAndWellness: {self.type}, Quantity: {self.quantity}>'


# Subcategory Models
class FootwearSubCategory(db.Model):
    __tablename__ = 'footwear_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    footwear_id = db.Column(db.Integer, db.ForeignKey('footwear.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    for_gender = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<FootwearSubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'


class ActivewearSubCategory(db.Model):
    __tablename__ = 'activewear_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    activewear_id = db.Column(db.Integer, db.ForeignKey('activewear_tops.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    for_gender = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<ActivewearSubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'


class BottomsSubCategory(db.Model):
    __tablename__ = 'bottoms_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    bottoms_id = db.Column(db.Integer, db.ForeignKey('bottoms.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    for_gender = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<BottomsSubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'


class OuterwearSubCategory(db.Model):
    __tablename__ = 'outerwear_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    outerwear_id = db.Column(db.Integer, db.ForeignKey('outerwear.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    for_gender = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<OuterwearSubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'


class RecoverySubCategory(db.Model):
    __tablename__ = 'recovery_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    recovery_id = db.Column(db.Integer, db.ForeignKey('recovery_and_wellness.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String, nullable=True)  # Optional for recovery items
    quantity = db.Column(db.Integer, nullable=False, default=0)
    for_gender = db.Column(db.String, nullable=True)  # Optional for recovery items
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<RecoverySubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'

class Accessories(db.Model):
    __tablename__ = 'accessories'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    subcategories = db.relationship('AccessoriesSubCategory', backref='accessories', lazy=True)
    
    def __repr__(self):
        return f'<Accessory: {self.type}, Quantity: {self.quantity}>'


class Swimwear(db.Model):
    __tablename__ = 'swimwear'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    subcategories = db.relationship('SwimwearSubCategory', backref='swimwear', lazy=True)
    
    def __repr__(self):
        return f'<Swimwear: {self.type}, Quantity: {self.quantity}>'


class CompressionWear(db.Model):
    __tablename__ = 'compression_wear'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    subcategories = db.relationship('CompressionSubCategory', backref='compression_wear', lazy=True)
    
    def __repr__(self):
        return f'<CompressionWear: {self.type}, Quantity: {self.quantity}>'


class SpecialtySportswear(db.Model):
    __tablename__ = 'specialty_sportswear'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    subcategories = db.relationship('SpecialtySportswearSubCategory', backref='specialty_sportswear', lazy=True)
    
    def __repr__(self):
        return f'<SpecialtySportswear: {self.type}, Quantity: {self.quantity}>'


class ProtectiveGear(db.Model):
    __tablename__ = 'protective_gear'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    
    subcategories = db.relationship('ProtectiveGearSubCategory', backref='protective_gear', lazy=True)
    
    def __repr__(self):
        return f'<ProtectiveGear: {self.type}, Quantity: {self.quantity}>'


# Sub-Category Models
class AccessoriesSubCategory(db.Model):
    __tablename__ = 'accessories_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    accessories_id = db.Column(db.Integer, db.ForeignKey('accessories.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    for_gender = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<AccessoriesSubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'


class SwimwearSubCategory(db.Model):
    __tablename__ = 'swimwear_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    swimwear_id = db.Column(db.Integer, db.ForeignKey('swimwear.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    for_gender = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<SwimwearSubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'


class CompressionSubCategory(db.Model):
    __tablename__ = 'compression_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    compression_wear_id = db.Column(db.Integer, db.ForeignKey('compression_wear.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    for_gender = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<CompressionSubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'


class SpecialtySportswearSubCategory(db.Model):
    __tablename__ = 'specialty_sportswear_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    specialty_sportswear_id = db.Column(db.Integer, db.ForeignKey('specialty_sportswear.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    for_gender = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<SpecialtySportswearSubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'


class ProtectiveGearSubCategory(db.Model):
    __tablename__ = 'protective_gear_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    protective_gear_id = db.Column(db.Integer, db.ForeignKey('protective_gear.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    for_gender = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    
    def __repr__(self):
        return f'<ProtectiveGearSubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'
