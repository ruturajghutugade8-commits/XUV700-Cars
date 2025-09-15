# XUV700-Cars
this project makes using Python, flask, sqllite

# 📚 Library Booking & Management System

A **Flask-based web application** for handling bookings, payments, ratings, and admin management.  
This project uses **Flask (Python)**, **SQLite** databases, and includes a simple frontend with **HTML, CSS, and JavaScript**.

---

## 🚀 Features
- User booking system
- Admin login (with secure password hashing)
- Payment page
- User rating system
- Admin dashboard to view/manage data
- SQLite database integration

---

## 📂 Project Structure

app.py # Main Flask app
database.py # Database initialization & queries
bookings.db # Database file (bookings)
library.db # Database file (library data)
templates/ # HTML templates (frontend)
static/css/ # CSS files (styling)
static/js/ # JavaScript files (frontend logic)


---

## ⚙️ Installation & Run (One Command Setup)

👉 Copy-paste the below block in your terminal:

``it is for bash:


# Clone repo
git clone https://github.com/your-username/library-booking-system.git && cd library-booking-system && \

# Create virtual environment
python -m venv venv && \

# Activate venv (Windows)
source venv/Scripts/activate || \

# Activate venv (Linux/Mac)
source venv/bin/activate && \

# Install dependencies
pip install -r requirements.txt && \

# Run the app
python app.py


Open browser:
👉 http://127.0.0.1:5000/

Available routes:

/ → Homepage

/book → Booking page

/pay → Payment page

/rate → User rating page

/admin → Admin login
