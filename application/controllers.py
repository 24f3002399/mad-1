from flask import Flask, render_template, redirect,url_for, request
from flask import current_app as app
from .models import *
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

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
                    return redirect(f"/Home_user/{this_user.id}")
            else:
                return render_template("incorrect_pass.html")
        else:
           return render_template("not_exist.html")
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
            return render_template("already_exist.html")
        else:
            user = Users(name= name, email = email , password = password , address = address , pincode = pin_code,)
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
    return render_template("register.html")

@app.route("/admin_search")
def search():
    this_user = Users.query.filter_by(type = "admin").first()
    return render_template("admin_search.html" , this_user = this_user)

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
        return render_template("pfile_edit.html" , this_user = this_user)
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
    spot = Parking_spot.query.filter_by(lot_id = id , status = "available").all()
    lnt = len(Parking_spot.query.filter_by(lot_id = id , status = "occupied").all())
    if request.method == "POST":

        for i in spot:
            db.session.delete(i)
        db.session.commit()

        this_lot.id = request.form.get("id")
        this_lot.prime_location_name = request.form.get("loc")
        this_lot.Address = request.form.get("add")
        this_lot.Pin_code = request.form.get("pin")
        this_lot.Price = request.form.get("price")
        this_lot.maximum_number_of_spots = request.form.get("maxs")
        db.session.commit()
        
        for i in range(int(this_lot.maximum_number_of_spots) - lnt):
            spot = Parking_spot(lot_id = id)
            db.session.add(spot)
        db.session.commit()
        return redirect("/admin")
    
    return render_template("edit_prk.html", this_lot =this_lot )

@app.route("/Home_user/<int:id>")
def Ushome(id):
    this_user = Users.query.filter_by(id = id).first()
    reserve = Reserve_parking_spot.query.filter_by(user_id = id).all()
    return render_template("user_home.html" , this_user = this_user, reserve = reserve)

@app.route("/U_summary/<int:id>")
def Us_summary(id):
    this_user = Users.query.filter_by(id = id).first()
    spot = len(Reserve_parking_spot.query.filter_by(user_id = id).all())
    if (spot >= 1) :
        a_s = len(Reserve_parking_spot.query.filter_by(status = "released" , user_id = id).all())
        o_s = len(Reserve_parking_spot.query.filter_by(status = "occupied" , user_id = id).all())

        labels = ["Parked Out" , "Occupied"]
        sizes = [a_s , o_s]
        colors = ["yellow" , "green"]
        plt.pie(sizes , labels = labels , colors = colors ,autopct = "%1.1f%%")
        plt.title("Parking Details")
        plt.savefig(f"static/{id}_us_pie.png")
        plt.clf()

        labels = ["Parked Out" , "Occupied"]
        sizes = [a_s , o_s]
        plt.bar(labels , sizes)
        plt.xlabel("Parking Details")
        plt.ylabel("No of Spot")
        plt.title("Parking Details")
        plt.savefig(f"static/{id}_us_bar.png")
        plt.clf()

        return render_template("user_summary.html" , this_user = this_user , a_s = a_s , o_s = o_s)
    else:
        return redirect(f"/Home_user/{id}")

@app.route("/us_prof_edit/<int:id>" , methods = ["GET", "POST"])
def us_prof_edit(id):
    this_user = Users.query.filter_by(id = id).first()
    if request.method == "POST":
        this_user.email = request.form.get("email")
        this_user.password = request.form.get("pwd")
        this_user.name = request.form.get("name")
        this_user.address = request.form.get("add")
        this_user.pincode = request.form.get("pin")
        db.session.commit()
        return render_template("pfile_edit.html", this_user = this_user)
    return render_template("us_prof_edit.html" , this_user = this_user)

@app.route("/release/<int:user_id>/<int:spot_id>/<int:lot_id>" , methods = ["GET", "POST"])
def release(user_id , spot_id , lot_id):
    this_user = Users.query.filter_by(id = user_id).first()
    spot = Parking_spot.query.filter_by(id = spot_id).first()
    lot = Parking_lot.query.filter_by(id = lot_id).first()
    l_time = datetime.datetime.now()
    l_stamp = l_time - spot.parking_time
    hour = (l_stamp.total_seconds())/3600
    price = (hour*lot.Price)
    if request.method == "POST":
        
        res = Reserve_parking_spot.query.filter_by(spot_id = spot.id , status = "occupied").first()
        res.status = "released"
        res.leaving_time = l_time
        res.parking_cost = price
        db.session.commit()

        spot.status = "available"
        spot.occupied_user = None
        spot.vehicle_no = None
        spot.parking_time = None
        lot.occupied_spot -= 1 
        db.session.commit()
        return redirect(f"/Home_user/{user_id}")
    return render_template("release_prk.html" , this_user = this_user, spot = spot , l_time = l_time ,price = price)

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
        if lot.occupied_spot == None:
            db.session.delete(lot)
            db.session.commit()
            return redirect("/admin")
        elif lot.occupied_spot == 0:
            db.session.delete(lot)
            db.session.commit()
            return redirect("/admin")
        else:
            return render_template("not_delete.html")
    return render_template("delete_prk.html" , this_lot = this_lot)

@app.route("/occupied/<int:lot_id>/<int:spot_id>")
def occupied(lot_id ,spot_id):
    this_lot = Parking_lot.query.filter_by(id = lot_id).first()
    spot = Parking_spot.query.filter_by(id = spot_id).first()    
    return render_template("occupied_prk.html" , this_lot = this_lot , spot = spot ) 

@app.route("/users")
def users():
    this_user = Users.query.filter_by(type = "admin").first()
    users = Users.query.filter_by(type = "general")
    return render_template("admin_users.html" , users = users , this_user = this_user)

@app.route("/ad_search")
def ad_search():
    search_word = request.args.get("search")
    key = request.args.get("key")
    if key == "user":
        result = Users.query.filter_by(id = search_word).first()
        spot = Parking_spot.query.filter_by(occupied_user = search_word).all()
        tot_spot = len(spot)
        return render_template("ad_search.html" ,result = result , key = key ,spot = spot , tot_spot = tot_spot)

    elif key == "parking_lot":
        result = Parking_lot.query.filter_by(Address = search_word).all()
        spots = Parking_spot.query.all()
        return render_template("ad_search.html" ,key = key ,spots = spots ,result = result)
    else:
        return redirect("/admin_search")

@app.route("/us_search/<int:id>")
def us_search(id):
    this_user = Users.query.filter_by(id = id).first()
    search_word = request.args.get("search")
    key = request.args.get("key")
    if key == "location":
        result = Parking_lot.query.filter_by(prime_location_name = search_word).all()
        return render_template("us_search.html" , result = result , key = key , search_word = search_word , this_user = this_user)
    else:
        result = Parking_lot.query.filter_by(Pin_code = search_word).all()
        return render_template("us_search.html" , result = result , key = key , search_word = search_word , this_user = this_user)

@app.route("/book/<int:user_id>/<int:lot_id>" , methods = ["GET" , "POST"])
def s_book(user_id , lot_id):
    user = Users.query.filter_by(id = user_id).first()
    lot = Parking_lot.query.filter_by(id = lot_id).first()
    spot = Parking_spot.query.filter_by(lot_id = lot_id , status = "available").first()
    v_no = request.form.get("v_no")
    if request.method == "POST":  
        spot.status = "occupied"
        spot.occupied_user = user.id
        if lot.occupied_spot == None:
            lot.occupied_spot = 1
        else:
            lot.occupied_spot += 1
        db.session.commit()
        p_time = datetime.datetime.now()
        spot.vehicle_no = v_no
        spot.parking_time = p_time
        db.session.commit()
        reserve = Reserve_parking_spot(spot_id = spot.id , status = "occupied" , user_id = user.id , vehicle_no = v_no , parking_time = p_time , location = lot.prime_location_name , lot_id = lot.id)
        db.session.add(reserve)
        db.session.commit()        
        return redirect(f"/Home_user/{user.id}")
    return render_template("book_prk.html" , user = user , lot = lot , spot = spot)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/ad_summary")
def ad_summary():
    this_user = Users.query.filter_by(type = "admin").first()
    a_s = len(Parking_spot.query.filter_by(status = "available").all())
    o_s = len(Parking_spot.query.filter_by(status = "occupied").all())

    labels = ["Available" , "Occupied"]
    sizes = [a_s , o_s]
    colors = ["green" , "yellow"]
    plt.pie(sizes , labels = labels , colors = colors ,autopct = "%1.1f%%")
    plt.title("Status of Parking Spot")
    plt.savefig("static/ad_pie.png")
    plt.clf()

    labels = ["Available" , "Occupied"]
    sizes = [a_s , o_s]
    plt.bar(labels , sizes)
    plt.xlabel("Status of Parking Spot")
    plt.ylabel("No of Spot")
    plt.title("Status of Parking Spot")
    plt.savefig("static/ad_bar.png")
    plt.clf()

    return render_template("admin_summary.html" , a_s = a_s , o_s = o_s ,this_user = this_user)


