from flask import render_template, url_for, redirect, request, session, flash
from flask.helpers import make_response
from . import *
from .forms import *
from .models import *
from .utils import *
import time

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/scrap")
def scrap():
    return render_template("scrap.html")

@app.route('/scrap/login', methods=['GET','POST'])
def login():
    if not isUserLoggedIn():
        form = LoginForm()
        
        error_message = ""
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            result = verifyAndLogin(email, password)
            if result["result"] == True:
                if isAdmin():
                    flash(result["message"], "success")
                return make_response(redirect(url_for('admin')))
                flash(result["message"], "success")
                return make_response(redirect(url_for('scrap')))
            if result["result"] == False:
                flash(result["message"], "danger")
                return make_response(redirect(url_for('login')))

        return render_template("login.html", form=form)
    else:
        return render_template("scrap.html")

@app.route('/scrap/registration', methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Getting Form Data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
 
        # Inserting Data into DB
        result = registerUser(email, password, first_name, last_name)
        if result["result"] == True:
            flash(result["message"], "success")
            return make_response(redirect(url_for('scrap')))
        if result["result"] == False:
            flash(result["message"], "danger")
            return make_response(redirect(url_for('registration')))
        
    return render_template("registration.html", form=form)

@app.route('/scrap/logout')
def logout():
    result = logoutUser()
    if result["result"] == True:
        flash(result["message"], "success")
        return make_response(redirect(url_for('scrap')))
    if result["result"] == False:
        flash(result["message"], "danger")
        return make_response(redirect(url_for('scrap')))

@app.route('/scrap/addproduct', methods=['POST','GET'])
def addproduct():
    if isAdmin():
        form = AddProductForm()
        if request.method == "POST":
            product_name = form.name.data
            category = getCategory(form.category.data)
            price = form.price.data
            description = form.description.data
            f = form.image.data
            filename = str(int(time.time())) + '.' + f.filename.split('.')[1]
            f.save(os.path.join(app.config["UPLOAD_PHOTOS_DEST"], filename))
            print("Category : ",category)

            result = addProduct(product_name , category.category_id , price , description , filename)
            if result["result"] == True:
                flash(result["message"], "success")
                return make_response(redirect(url_for('addproduct')))
            if result["result"] == False:
                flash(result["message"], "danger")
                return make_response(redirect(url_for('addproduct')))
                
        return render_template("addproduct.html", title="Add Products page", form=form)


@app.route('/admin')
def admin():
    return "ON ADMIN PAGE"

@app.route('/product')
def product():
    data = {}
    category = getAllCategory()
    for cat in category:
        category_id = cat.category_id
        products = getProductByCategory(category_id)
        data[cat.category_name] = products

    return render_template("product.html", data=data)
        
@app.route('/add_to_cart', methods=["GET"])
def add_to_cart():
    if isUserLoggedIn():
        product_id = request.args.get('product_id')
        result = addToCart(product_id)
        print(result)
        return make_response(redirect(url_for('product')))
    else:
        product_id = request.args.get('product_id')
        addToCartTemp(product_id)
        return make_response(redirect(url_for('product')))


@app.route("/cart")
def cart():
    if isUserLoggedIn():
        cart = getCart()
        product_list = []
        for c in cart:
            product_list.append(Product.query.filter(Product.product_id == c.product_id).first())
        return render_template("/cart.html", product_list=product_list)
    

@app.route("/scrap/detail", methods=["GET","POST"])
def detail():
        form = DetailForm()
        if request.method == "POST" and form.validate_on_submit():
            phone = form.phone.data
            address = form.address.data
            print(phone, address)
            session["Request"] = {}
            session["Request"]["phone"] = phone
            session["Request"]["address"] = address

            

            return make_response(redirect(url_for('checkout')))

        return render_template("detail.html", form=form)


@app.route("/scrap/checkout", methods=["GET", "POST"])
def checkout():
    cart = getCart()
    product_list = []
    total_price = 0
    for c in cart:
        product = Product.query.filter(Product.product_id == c.product_id).first() 
        product_list.append(product)
        total_price += product.price


    return render_template("checkout.html", product_list=product_list, total_price=total_price)

@app.route("/scrap/placerequest", methods=["GET","POST"])
def placerequest():
    if request.method == "POST":
        cart = getCart()
        product_list = []
        total_price = 0
        for c in cart:
            product = Product.query.filter(Product.product_id == c.product_id).first() 
            product_list.append(product)
            total_price += product.price

        requests = Request(user_id=session["user_id"], total_price=total_price)
        db.session.add(requests)
        db.session.flush()
        db.session.commit()
        for product in product_list:
            request_prod = RequestProduct(request_id=requests.request_id, product_id=product.product_id)
            db.session.add(request_prod)
            db.session.flush()
            db.session.commit()

        print("DONE")

        clearCart()
        session["cart_count"] = 0
        flash("Request Placed for selling !!!", "success")
        return make_response(redirect(url_for('scrap')))


@app.route('/scrap/contact', methods=['GET','POST'])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        contact = Contact(name=name, email=email, phone=phone, message=message)
        db.session.add(contact)
        db.session.flush()
        db.session.commit()

        flash("Message Submitted !!!", "success")
        return make_response(redirect(url_for('scrap')))
        
    return render_template("contact.html")

@app.route("/scrap/about")
def about():
    return render_template("about.html")
    
