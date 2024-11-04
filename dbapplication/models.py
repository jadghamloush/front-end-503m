from app import db
from flask_login import UserMixin

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
    for_gender = db.Column(db.String, nullable=False)  # "Men", "Women", or "Kids"
    
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
    
    def __repr__(self):
        return f'<ProtectiveGearSubCategory: {self.type}, Price: {self.price}, Size: {self.size}, Quantity: {self.quantity}, For: {self.for_gender}>'
