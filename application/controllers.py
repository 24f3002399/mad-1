from flask import Flask, render_template, redirect,url_for, request
from flask import current_app as app

from .models import *

@app.route("/login" , methods = ["POST" , "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        this_user = Users.query.filter_by(email = email).first()
        if this_user:
            if (this_user.password == password):
                if (this_user.type == "admin"):
                    return redirect("/admin")
                else:
                    return render_template("user_home.html",this_user = this_user)
            else:
                return "Password is Wrong"
        else:
           return "User does not exist"

    return render_template("login.html")

@app.route("/register" ,methods = ["GET" ,"POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pwd")
        name = request.form.get("name")
        address = request.form.get("add")
        pin_code = request.form.get("pin")
        user_email = Users.query.filter_by(email = email).first()
        if user_email :
            return "user already exist"
        else:
            user = Users(name= name, email = email , password = password , address = address , pincode = pin_code,)
            db.session.add(user)
            db.session.commit()
        return "Registration successfully "
    return render_template("register.html")

@app.route("/login/<int:id>")
def adhome(id):
    this_user = Users.query.filter_by(id = id).first()    
    return render_template("admin_home.html" , this_user = this_user)

@app.route("/admin_user/<int:id>")
def admin_user(id):
    this_user = Users.query.filter_by(id = id).first()
    return render_template("admin_users.html", this_user = this_user)

@app.route("/search/<int:id>")
def search(id):
    this_user = Users.query.filter_by(id = id).first()
    return render_template("admin_search.html" , this_user = this_user)

@app.route("/summary/<int:id>")
def summary(id):
    this_user = Users.query.filter_by(id = id).first()
    return render_template("admin_summary.html" , this_user = this_user)

@app.route("/prof_edit/<int:id>" , methods = ["GET", "POST"])
def prof_edit(id):
    this_user = Users.query.filter_by(id = id).first()
    if request.method == "POST":
        this_user.email = request.form.get("email")
        this_user.password = request.form.get("pwd")
        this_user.name = request.form.get("name")
        this_user.address = request.form.get("add")
        this_user.pin_code = request.form.get("pin")
        db.session.commit()
        return "Profile Edit Successfully"
    return render_template("prof_edit.html" , this_user = this_user)

@app.route("/add_lot/<int:id>" ,methods = ["GET", "POST"])
def add_lot(id):
    this_user = Users.query.filter_by(id = id).first()
    if request.method == "POST":
        id = request.form.get("id")
        loc = request.form.get("loc")
        add = request.form.get("add")
        pin = request.form.get("pin")
        price = request.form.get("price")
        maxs = request.form.get("maxs")
        lot = Parking_lot(prime_location_name = loc , Price = price , Address = add , Pin_code = pin , maximum_number_of_spots = maxs)
        db.session.add(lot)
        db.session.commit()
        
        for i in range(int(maxs)):
            spot = Parking_spot(lot_id = id)
            db.session.add(spot)
        db.session.commit()
        return redirect("/admin")
    return render_template("new_prk.html" , this_user = this_user)

@app.route("/edit_lot/<int:id>", methods = ["GET" , "POST"])
def edit_lot(id):
    this_lot = Parking_lot.query.filter_by(id = id).first()
    if request.method == "POST":
        db.session.delete(this_lot)
        db.session.commit()
        id = request.form.get("id")
        loc = request.form.get("loc")
        add = request.form.get("add")
        pin = request.form.get("pin")
        price = request.form.get("price")
        maxs = request.form.get("maxs")
        lot = Parking_lot(prime_location_name = loc , Price = price , Address = add , Pin_code = pin , maximum_number_of_spots = maxs)
        db.session.add(lot)
        db.session.commit()
        
        for i in range(int(maxs)):
            spot = Parking_spot(lot_id = id)
            db.session.add(spot)
        db.session.commit()
        return redirect("/admin")
    
    return render_template("edit_prk.html", this_lot =this_lot )

@app.route("/Home_user/<int:id>")
def Ushome(id):
    this_user = Users.query.filter_by(id = id).first()    
    return render_template("user_home.html" , this_user = this_user)

@app.route("/U_summary/<int:id>")
def Us_summary(id):
    this_user = Users.query.filter_by(id = id).first()
    return render_template("user_summary.html" , this_user = this_user)

@app.route("/us_prof_edit/<int:id>" , methods = ["GET", "POST"])
def us_prof_edit(id):
    this_user = Users.query.filter_by(id = id).first()
    if request.method == "POST":
        this_user.email = request.form.get("email")
        this_user.password = request.form.get("pwd")
        this_user.name = request.form.get("name")
        this_user.address = request.form.get("add")
        this_user.pin_code = request.form.get("pin")
        db.session.commit()
        return "Profile Edit Successfully"
    return render_template("us_prof_edit.html" , this_user = this_user)

@app.route("/release/<int:id>")
def release(id):
    this_user = Users.query.filter_by(id = id).first()
    return render_template("release_prk.html" , this_user = this_user)

@app.route("/book")
def s_book():
    return render_template("book_prk.html")

@app.route("/admin")
def admin():
    this_user = Users.query.filter_by(type = "admin").first()
    spots = Parking_spot.query.all()
    lots = Parking_lot.query.all()
    maxs = {}
    plt = Parking_lot.query.all()
    for lot in plt:
        maxs[lot.id] = lot.maximum_number_of_spots

    return render_template("admin_home.html" , this_user = this_user ,maxs = maxs, lots = lots ,spots = spots)

@app.route("/view_spot/<int:lot_id>/<int:spot_id>")
def view_spot(lot_id , spot_id):
    this_user = Users.query.filter_by(type = "admin").first()
    this_lot = Parking_lot.query.filter_by(id = lot_id).first()
    spot_id = Parking_spot.query.filter_by(id = spot_id).first()
    return render_template("view_prk.html" , this_user = this_user , this_lot = this_lot , spot_id = spot_id)

@app.route("/delete_lot/<int:id>" ,methods = ["GET" , "POST"])
def delete_lot(id):
    this_lot = Parking_lot.query.filter_by(id = id).first()
    if request.method == "POST":
        lot = Parking_lot.query.get(id)
        if lot.occupied_lot == None:
            db.session.delete(lot)
            db.session.commit()
            return redirect("/admin")
        else:
            return "Not able to Delete"
    return render_template("delete_prk.html" , this_lot = this_lot)

@app.route("/occupied/<int:lot_id>/<int:spot_id>")
def occupied(lot_id ,spot_id):
    this_lot = Parking_lot.query.filter_by(id = lot_id).first()
    spot_id = Parking_spot.query.filter_by(id = spot_id).first()    
    return render_template("occupied_prk.html" , this_lot = this_lot , spot_id = spot_id ) 

