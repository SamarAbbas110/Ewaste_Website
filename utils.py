from FlaskApp.models import *
from flask import session
import random


def getUser(email):
    user = User.query.filter(User.email == email).first()
    return user

def verifyAndLogin(email, password):
    user = getUser(email)
    if user == None:
        return {"result": False, "message": "USER NOT FOUND / CREATE ACCOUNT TO LOGIN"}
    if user.password == password:
        setLoginSession(user)
        return {"result": True, "message": "Successfully Logged In !!!"}
    return {"result": False, "message": "Email / Password Incorrect"}

def setLoginSession(user):
    user_id = user.user_id
    user_fullname = user.first_name + " " + user.last_name
    user_email = user.email
    session['is_user_logged_in'] = True
    session['user_id'] = str(user_id)
    session['user_fullname'] = user_fullname
    session['user_email'] = user_email
    session['cart_count'] =  0 
    session['buy_product_id'] = []

def isAdmin():
    if isUserLoggedIn():
        user = getUser(session['user_email'])
        if user.user_type == "admin":
            return True
    return False

def isUserLoggedIn():
    try:
        if session['is_user_logged_in'] == True :
            return True
        return False
    except:
        return False

def setTempUser():
    session['is_user_logged_in'] = False
    session['user_fullname'] = None
    session['user_email'] = None
    session['temp_user'] = 'True'
    session['temp_cart'] = []
    session['cart_count'] = 0
    session['user_id'] = random.randint(100000,900000)

def logoutUser():
    if isUserLoggedIn():
        session.clear()
        setTempUser()
        return {"result":True, "message": "Successfully logout!!"}
    else:
        return {"result":False, "message": "User Not lOgged in !!"}

def registerUser(email, password, firstname, lastname):
    try:
        user = User(email=email, password=password, first_name=firstname, last_name=lastname)
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        setLoginSession(user)
        return {"result":True, "message": "User Created Successfully"}
    except:
         return {"result":False, "message": "User Already Found"}

def addProduct(product_name , category_id , price , description , image):
    try:
        product = Product(product_name=product_name , category_id=category_id , price=price , desc=description , image=image)
        db.session.add(product)
        db.session.flush()
        db.session.commit()
        return {"result":True, "message": "Product Added !!"}
    except:
         return {"result":False, "message": "Product Addition Failed !!"}

def addCategory(category_name):
    try:
        category = Category(category_name=category_name)
        db.session.add(category)
        db.session.flush()
        db.session.commit()
        return {"result":True, "message": "Category Added !!"}
    except:
         return {"result":False, "message": "Category Addition Failed !!"}

def getCategory(category_name):
    category = Category.query.filter(Category.category_name == category_name).first()
    if category == None:
        result = addCategory(category_name)
        if result["result"] == True:
            category = Category.query.filter(Category.category_name == category_name).first()
    return category

def getProductByCategory(category_id):
    return Product.query.filter(Product.category_id == category_id).all()

def getAllCategory():
    return Category.query.all()

def addToCart(product_id):
    # try:
    cart = Cart(product_id=product_id, user_id=session['user_id'])
    db.session.add(cart)
    db.session.flush()
    db.session.commit()
    session["cart_count"] = Cart.query.filter(Cart.user_id == session['user_id']).count()
    # except:
    #     pass


def addToCartTemp(product_id):
    try:
        if product_id not in session["temp_cart"]:
            session["temp_cart"].extend([product_id])
    except:
        session["temp_cart"] = [product_id]

def getCart():
    if isUserLoggedIn():
        cart = Cart.query.filter(Cart.user_id == session['user_id']).all()
        return cart
    
def clearCart():
    Cart.query.filter(Cart.user_id == session['user_id']).delete()
    db.session.commit()