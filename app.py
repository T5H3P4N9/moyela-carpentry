import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
from datetime import datetime
import secrets

app = Flask(__name__, instance_relative_config=True)
app.secret_key = secrets.token_hex(16)


os.makedirs(app.instance_path, exist_ok=True)
db_path = os.path.join(app.instance_path, "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path.replace(os.path.sep, "/")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Model
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="new")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
    db.create_all()
    inspector = inspect(db.engine)
    column_names = [column["name"] for column in inspector.get_columns("quote")]
    if "service" not in column_names:
        db.session.execute(text("ALTER TABLE quote ADD COLUMN service VARCHAR(50)"))
        db.session.commit()

@app.route("/")
def index():
    return render_template("index.html", active_page="home")

@app.route("/about")
@app.route("/about/")
def about():
    return render_template("about.html", active_page="about")

@app.route("/quote", methods=["GET", "POST"], strict_slashes=False)
def quote():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        service = request.form.get("service")
        description = request.form["description"]

        new_quote = Quote(name=name, phone=phone, service=service, description=description)
        db.session.add(new_quote)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("quote.html", active_page="quote")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "Tshepang" and password == "T5H3P4N9":  
            session["logged_in"] = True
            return redirect(url_for("admin"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("index"))

@app.route("/admin")
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    return render_template("admin.html", quotes=quotes, active_page="admin")

@app.route("/admin/status/<int:quote_id>", methods=["POST"])
def update_quote_status(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    quote.status = request.form.get("status", "done")
    db.session.commit()
    return redirect(url_for("admin"))

@app.route("/admin/delete/<int:quote_id>", methods=["POST"])
def delete_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run()
