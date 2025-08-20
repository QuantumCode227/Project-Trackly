from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.country_timezone import country_timezone_map
from cloudinary.uploader import cloudinary, upload, destroy
from app.utils.cloudinary_utils import extract_public_id
from flask_login import current_user, login_required
from app.models import Signup
from app import db
import os

settings_bp = Blueprint("settings", __name__)


# Settings page
@settings_bp.route("/settings")
@login_required
def settings():
    user = current_user
    return render_template("settings.html", user=user, country_timezone_map=country_timezone_map)


# Update name/email/country
@settings_bp.route("/settings/update-profile", methods=["POST"])
@login_required
def update_profile():
    user = current_user

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        country = request.form.get("country")

        if email and email != user.email:
            if Signup.query.filter_by(email=email).first():
                flash("Email is already taken!", "danger")
                return redirect(url_for("settings.settings"))
            user.email = email

        if name:
            user.name = name
        if country:
            user.country = country

        # Final commit
        db.session.commit()
        flash("Profile updated successfully!", "success")
    return redirect(url_for("settings.settings"))


# Upload profile picture
@settings_bp.route("/settings/upload-profile-picture", methods=["POST"])
@login_required
def upload_profile_picture():
    user = current_user

    profile_picture = request.files.get("profile_picture")
    if profile_picture:
        max_file_size = 2 * 1024 * 1024
        profile_picture.seek(0, os.SEEK_END)
        file_size = profile_picture.tell()
        profile_picture.seek(0)
        if file_size > max_file_size:
            flash("File is lager then 2 MB", 'danger')
            return redirect(url_for('settings.settings'))
        try:
            result = cloudinary.uploader.upload(
                profile_picture,
                folder="trackly_profile_pics",
                transformation=[
                    {
                        "width": 200,
                        "height": 200,
                        "crop": "thumb",
                        "radius": "max",
                    }
                ],
            )
            new_pfp_url = result.get("secure_url")

            if new_pfp_url:
                if user.profile_picture_url:
                    try:
                        previous_pfp_name = extract_public_id(user.profile_picture_url)
                        destroy(previous_pfp_name)
                    except Exception as e:
                        flash("Some error occured. Please try again.", "danger")
                user.profile_picture_url = new_pfp_url

        except Exception as e:
            flash("Image upload failed. Please try again.", "danger")
            return redirect(url_for("settings.settings"))
        # Final commit
        db.session.commit()
        flash("Profile picture uploaded successfully", "success")
    else:
        flash('No file selected', 'danger')
    return redirect(url_for("settings.settings"))


# Remove profile picture
@settings_bp.route("/settings/remove-profile-picture", methods=["POST"])
@login_required
def remove_profile_picture():
    user = current_user
    if user.profile_picture_url:
        try:
            previous_pfp_name = extract_public_id(user.profile_picture_url)
            destroy(previous_pfp_name)
            user.profile_picture_url = None
        except Exception as e:
            flash("Some error occured. Please try again.", "danger")
            return redirect(url_for("settings.settings"))
    
        # Final commit
        db.session.commit()
        flash("Profile picture uploaded successfully", "success")
    return redirect(url_for("settings.settings"))


# Password update logic
@settings_bp.route("/settings/update-password", methods=["POST"])
@login_required
def update_password():
    user = current_user

    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if current_password:
        if check_password_hash(user.password, current_password):
            if new_password == confirm_password:
                user.password = generate_password_hash(new_password)
            else:
                flash("Password not match!", "warning")
                return redirect(url_for("auth.settings"))
        else:
            flash("Invalid password!", "danger")
            return redirect(url_for("settings.settings"))

        # Final commit
        db.session.commit()
        flash("Password updated successfully", "success")
    return redirect(url_for("settings.settings"))
