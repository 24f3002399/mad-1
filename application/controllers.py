from flask import Flask, render_template, redirect,url_for, request
from flask import current_app as app

from .models import *

@app.route("/login" , methods = ["POST" , "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        this_user = Users.query.filter_by(email = email).first()
        name = this_user.name
        if this_user:
            if (this_user.password == password):
                if (this_user.type == "admin"):
                    return render_template("admin_home.html" ,name = name)
                else:
                    return render_template("user_home.html",name = name)
            else:
                return "Password is Wrong"
        else:
           return "user does not exist"

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