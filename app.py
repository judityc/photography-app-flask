import os, glob

from cs50 import SQL
from flask import Flask, redirect, render_template, session, request
from flask_session import Session
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from helpers import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, login_required, allowed_file

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Database library
db = SQL("sqlite:///contacts.db")


@app.route("/", methods=['GET'])
def index():
    """Show portfolio index page"""

    return render_template("index.html")


@app.route("/gallery", methods=['GET'])
def gallery():
    """Show portfolio photo gallery"""
    images = []
    for extention in ALLOWED_EXTENSIONS:
        for image in glob.iglob(UPLOAD_FOLDER + "/*." + extention):
            images.append(os.path.basename(image))

    return render_template("gallery.html", images=images)


@app.route("/about", methods=['GET'])
def about():
    """Show portfolio about me page"""

    return render_template("about.html")


@app.route('/contacts', methods=['GET', "POST"])
def contacts():
    """Show contact forma for bookings"""

    # User reaches route via POST (by sybmitting message)
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        message = request.form.get("message")

        # Add message to database
        db.execute("INSERT INTO contacts (name, number, email, message) VALUES (?, ?, ?, ?)", name, phone, email, message)

        # Redirect to index page
        return redirect("/")

    else:
        return render_template("contacts.html")


@app.route("/login", methods=['GET', "POST"])
def login():
    """Admin login"""
    # Forget any user_id
    session.clear()

    # Admin reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("failure.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("failure.html")

        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("failure.html")

        # Remember admin logged in
        session["user_id"] = rows[0]["username"]

        # Redirect admin to admin page
        return redirect("/admin")

    # Admin reached route via GET (as by clicking a link)
    else:
        return render_template("login.html")


@app.route("/admin", methods=['GET', "POST"])
@login_required
def admin():
    """Show messages history to admin and let upload pictures to web"""
    # Admin reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # If upload file was selected upload image to gallery folder and display in galley page
        if 'file' not in request.files:
            return redirect(request.url)
        files = request.files.getlist("file")
        for file in files:
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        session.clear()

        return redirect("/gallery")

    else:
        # Display history of messages on admin.html
        rows = db.execute("SELECT * FROM contacts") or []

        return render_template("admin.html", messages=rows)