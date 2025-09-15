from flask import Flask, render_template, request, jsonify, redirect, url_for, session  # Import necessary libraries
from werkzeug.security import check_password_hash  # Import necessary libraries
import database  # Import necessary libraries
import os  # Import necessary libraries

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("RMS_SECRET_KEY", "dev-secret-123")  # change in production

# Ensure DB and default admin exist
database.init_db()

# Home / index
@app.route("/")
def index():  # Function: index
    return render_template("index.html")

# Booking page (user-facing)
@app.route("/book")
def book():  # Function: book
    return render_template("book.html")

# Payment page
@app.route("/pay")
def pay():  # Function: pay
    return render_template("pay.html")

# Rate page
@app.route("/rate")
def rate():  # Function: rate
    return render_template("rate.html")

# Admin login
@app.route("/admin", methods=["GET","POST"])
def admin_login():  # Function: admin_login
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        admin = database.get_admin_by_username(username)
        if admin and check_password_hash(admin["password"], password):
            session["admin"] = True
            session["admin_username"] = username
            return redirect(url_for("admin_data"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

# Admin logout
@app.route("/logout")
def logout():  # Function: logout
    session.pop("admin", None)
    session.pop("admin_username", None)
    return redirect(url_for("index"))

# Admin bookings page
@app.route("/admin/bookings")
def admin_data():  # Function: admin_data
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    return render_template("data.html")

# API: save a booking (called from book.js)
@app.route("/api/bookings", methods=["POST"])
def api_add_booking():  # Function: api_add_booking
    data = request.json or {}
    booking = {
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "car_model": data.get("car_model"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "price": data.get("price"),
        "notes": data.get("notes"),
        "payment_method": data.get("payment_method", "Pending")
    }
    booking_id = database.add_booking(booking)
    return jsonify({"success": True, "id": booking_id})

# API: list bookings (admin only)
@app.route("/api/bookings", methods=["GET"])
def api_list_bookings():  # Function: api_list_bookings
    if not session.get("admin"):
        return jsonify({"error":"unauthorized"}), 401
    rows = database.get_bookings()
    bookings = [dict(row) for row in rows]
    return jsonify(bookings)

# API: delete booking (admin only)
@app.route("/api/bookings/<int:booking_id>", methods=["DELETE"])
def api_delete_booking(booking_id):  # Function: api_delete_booking
    if not session.get("admin"):
        return jsonify({"error":"unauthorized"}), 401
    database.delete_booking(booking_id)
    return jsonify({"success": True})

# API: clear all bookings (admin only)
@app.route("/api/bookings/clear", methods=["POST"])
def api_clear_bookings():  # Function: api_clear_bookings
    if not session.get("admin"):
        return jsonify({"error":"unauthorized"}), 401
    database.clear_bookings()
    return jsonify({"success": True})

# helper route to get a single booking (admin)
@app.route("/api/bookings/<int:booking_id>", methods=["GET"])
def api_get_booking(booking_id):  # Function: api_get_booking
    if not session.get("admin"):
        return jsonify({"error":"unauthorized"}), 401
    row = database.get_booking(booking_id)
    if row:
        return jsonify(dict(row))
    return jsonify({"error":"not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)