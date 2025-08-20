from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Expense, Income, Signup
from datetime import datetime
from sqlalchemy import func
from app import db


dashboard_bp = Blueprint("dashboard", __name__)


# Dashboard logic
@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    user = current_user
    user_id = user.id

    total_income = (
        db.session.query(func.sum(Income.amount)).filter_by(user_id=user_id).scalar()
        or 0
    )

    total_expense = (
        db.session.query(func.sum(Expense.amount)).filter_by(user_id=user_id).scalar()
        or 0
    )

    balance = total_income - total_expense

    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        user=user,
    )


# Add income logic
@dashboard_bp.route("/add_income", methods=["GET", "POST"])
@login_required
def add_income():
    user = current_user
    user_id = user.id

    if request.method == "POST":
        amount = request.form.get("amount")
        date_str = request.form.get("date")
        note = request.form.get("note")

        if not amount or not note:
            flash("All fields are required.", "danger")
            return redirect(url_for("dashboard.add_income"))

        # If user provides date, parse it, else use current time
        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Invalid date format.", "danger")
                return redirect(url_for("dashboard.add_income"))
        else:
            date = datetime.strptime(
                datetime.now().strftime("%Y-%m-%dT%H:%M"), "%Y-%m-%dT%H:%M"
            )

        add_income = Income(user_id=user_id, amount=int(amount), date=date, note=note)

        db.session.add(add_income)
        db.session.commit()
        flash("Income added successfully!", "success")
        return redirect(url_for("dashboard.income_history"))
    current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M")

    return render_template("add_income.html", current_datetime=current_datetime)


# Update income logic
@dashboard_bp.route("/update_income/<int:income_id>", methods=["GET", "POST"])
@login_required
def update_income(income_id):
    income = Income.query.get_or_404(income_id)

    if income.user_id != current_user.id:
        flash("You are not authorized to update this income.", "danger")
        return redirect(url_for("dashboard.income_history"))

    if request.method == "POST":
        amount = request.form.get("amount")
        note = request.form.get("note")
        date_str = request.form.get("date")

        if not amount or not note or not date_str:
            flash("All fields are required.", "danger")
            return redirect(url_for("dashboard.update_income", income_id=income_id))

        try:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("dashboard.update_income", income_id=income_id))

        # Update
        income.amount = int(amount)
        income.note = note
        income.date = date

        # Final commit
        db.session.commit()
        flash("Income updated successfully!", "success")
        return redirect(url_for("dashboard.income_history"))

    return render_template("update_income.html", income=income)


# Delete income logic
@dashboard_bp.route("/delete_income/<int:income_id>", methods=["POST"])
@login_required
def delete_income(income_id):
    income = Income.query.get_or_404(income_id)

    if income.user_id != current_user.id:
        flash("You are not authorized to delete this income.", "danger")
        return redirect(url_for("dashboard.income_history"))

    db.session.delete(income)
    db.session.commit()
    flash("Income deleted successfully!", "success")
    return redirect(url_for("dashboard.income_history"))


# Income History logic
@dashboard_bp.route("/income_history")
@login_required
def income_history():
    incomes = (
        Income.query.filter_by(user_id=current_user.id)
        .order_by(Income.date.desc())
        .all()
    )

    return render_template("income_history.html", incomes=incomes)


# Add expense logic
@dashboard_bp.route("/add_expense", methods=["GET", "POST"])
@login_required
def add_expense():
    user = current_user
    user_id = user.id

    if request.method == "POST":
        item = request.form.get("item")
        category = request.form.get("category")
        amount = request.form.get("amount")
        date_str = request.form.get("date")

        if not item or not category or not amount:
            flash("All fields are required.", "danger")
            return redirect(url_for("dashboard.add_expense"))

        # If user provides date, parse it, else use current time
        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Invalid date format.", "danger")
                return redirect(url_for("dashboard.add_expense"))
        else:
            date = datetime.strptime(
                datetime.now().strftime("%Y-%m-%dT%H:%M"), "%Y-%m-%dT%H:%M"
            )

        add_expense = Expense(
            user_id=user_id, item=item, category=category, amount=int(amount), date=date
        )

        db.session.add(add_expense)
        db.session.commit()
        flash("Expense added successfully!", "success")
        return redirect(url_for("dashboard.expense_history"))
    current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M")

    return render_template("add_expense.html", current_datetime=current_datetime)


# Update expense logic
@dashboard_bp.route("/update_expense/<int:expense_id>", methods=["GET", "POST"])
@login_required
def update_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if expense.user_id != current_user.id:
        flash("You are not authorized to update this expense.", "danger")
        return redirect(url_for("dashboard.expense_history"))

    if request.method == "POST":
        item = request.form.get("item")
        category = request.form.get("category")
        amount = request.form.get("amount")
        date_str = request.form.get("date")

        if not item or not category or not amount or not date_str:
            flash("All fields are required.", "danger")
            return redirect(url_for("dashboard.update_expense", expense_id=expense_id))
        try:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("dashboard.update_expense", expense_id=expense_id))

        # Update
        expense.item = item
        expense.category = category
        expense.amount = amount
        expense.date = date

        # Final commit
        db.session.commit()
        flash("Expense updated successfully!", "success")
        return redirect(url_for("dashboard.expense_history"))

    return render_template("update_expense.html", expense=expense)


# Delete expense logic
@dashboard_bp.route("/delete_expense/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash("You are not authorized to delete this expense.", "danger")
        return redirect(url_for("dashboard.expense_history"))

    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for("dashboard.expense_history"))


# Expense History logic
@dashboard_bp.route("/expense_history")
@login_required
def expense_history():
    expenses = (
        Expense.query.filter_by(user_id=current_user.id)
        .order_by(Expense.date.desc())
        .all()
    )

    return render_template("expense_history.html", expenses=expenses)
