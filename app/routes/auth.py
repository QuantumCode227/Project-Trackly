from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.country_timezone import country_timezone_map
from app.models import Signup
from app import db


from cloudinary.uploader import cloudinary, upload, destroy
from app.utils.cloudinary_utils import extract_public_id


auth_bp = Blueprint("auth", __name__)


# Signup logic
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        country = request.form.get("country")
        timezone = country_timezone_map.get(country, "UTC")

        hashed_password = generate_password_hash(password)

        user_exist = Signup.query.filter_by(email=email).first()
        if user_exist:
            flash("User already exists.", "danger")
            return redirect(url_for("auth.register"))
        new_user = Signup(
            name=name,
            email=email,
            password=hashed_password,
            country=country,
            timezone=timezone,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", country_timezone_map=country_timezone_map)


# Login logic
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        email = request.form.get("email").lower().strip()
        password = request.form.get("password")

        user = Signup.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("dashboard.dashboard"))
            else:
                flash("Invalid Password!", "danger")
        else:
            flash("User not exist", "danger")
    return render_template("login.html")


# Logout logic
@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


# Delete Account & Account data Logic
@auth_bp.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    user = current_user

    if request.method == "POST":
        password = request.form.get("password")

        if check_password_hash(user.password, password):
            if user.profile_picture_url:
                previous_pfp_name = extract_public_id(user.profile_picture_url)
                destroy(previous_pfp_name)
            db.session.delete(user)
            db.session.commit()
            logout_user()
            flash("Account deleted successfully!", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Incorrect password", "danger")
            return redirect(url_for("auth.delete_account"))
    return render_template("delete_account.html")
