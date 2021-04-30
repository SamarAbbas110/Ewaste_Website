from FlaskApp import db 
from datetime import datetime
db.Model.metadata.reflect(db.engine)


class Category(db.Model):
    __table_args__ = {'extend_existing' : True}
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)

class User(db.Model):
    __table_args__ = {'extend_existing' : True}
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False )
    last_name = db.Column(db.String(60), nullable=False )
    email = db.Column(db.String(255), nullable=False )
    password = db.Column(db.String(60), nullable=False )
    user_type = db.Column(db.String(60), nullable=False, default="seller" )
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )

class Product(db.Model):
    __table_args__ = {'extend_existing' : True}
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False, default="default.jpg")
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id') ,nullable=False)

    def __str__(self):
        return self.product_name
    
class Cart(db.Model):
    __table_args__ = {'extend_existing' : True}
    cart_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id') ,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id') ,nullable=False)

class Contact(db.Model):
    __table_args__ = {'extend_existing' : True}
    contact_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False )
    email = db.Column(db.String(255), nullable=False )
    phone = db.Column(db.String(20), nullable=False )
    message = db.Column(db.String(255), nullable=False )

    def __str__(self):
        return self.name

class Request(db.Model):
    __table_args__ = {'extend_existing' : True}
    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id') ,nullable=False)
    total_price = db.Column(db.Integer)

class RequestProduct(db.Model):
    __table_args__ = {'extend_existing' : True}
    requestproduct_id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.request_id') ,nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id') ,nullable=False)


