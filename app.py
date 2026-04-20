import os
import json 
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text, func
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, instance_relative_config=True)

# ======================
# SECURITY
# ======================
app.secret_key = os.environ.get("SECRET_KEY", "dev-fallback-secret")

# ======================
# DATABASE CONFIG (RENDER SAFE)
# ======================
db_url = os.environ.get("DATABASE_URL")

if not db_url:
    db_path = os.path.join(app.instance_path, "database.db")
    os.makedirs(app.instance_path, exist_ok=True)
    db_url = "sqlite:///" + db_path.replace(os.path.sep, "/")

# Render fix
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ======================
# MODELS
# ======================
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="new")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ======================
# INIT DB
# ======================
with app.app_context():
    db.create_all()

    inspector = inspect(db.engine)
    columns = [c["name"] for c in inspector.get_columns("quote")]

    if "service" not in columns:
        db.session.execute(text("ALTER TABLE quote ADD COLUMN service VARCHAR(50)"))
        db.session.commit()

    admin_username = os.environ.get("ADMIN_USERNAME", "Tshepang")
    admin_password = os.environ.get("ADMIN_PASSWORD", "1234")

    if not User.query.filter_by(username=admin_username).first():
        user = User(username=admin_username)
        user.set_password(admin_password)
        db.session.add(user)
        db.session.commit()

# ======================
# ROUTES
# ======================
@app.route("/")
def index():
    return render_template("index.html", active_page="home")


@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


@app.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        new_quote = Quote(
            name=request.form["name"],
            phone=request.form["phone"],
            service=request.form.get("service"),
            description=request.form["description"]
        )
        db.session.add(new_quote)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("quote.html", active_page="quote")

# ======================
# AUTH
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()

        if user and user.check_password(request.form.get("password")):
            session["logged_in"] = True
            session["user_id"] = user.id
            return redirect(url_for("admin"))

        flash("Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# ======================
# ADMIN DASHBOARD
# ======================
@app.route("/admin")
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    total_quotes = Quote.query.count()

    # 📊 Quotes per day
    quotes_per_day = db.session.query(
        func.date(Quote.created_at),
        func.count(Quote.id)
    ).group_by(func.date(Quote.created_at)).all()

    # 📈 Services (FIXED NULL ISSUE)
    top_services = db.session.query(
        func.coalesce(Quote.service, "Unknown"),
        func.count(Quote.id)
    ).group_by(func.coalesce(Quote.service, "Unknown"))\
     .order_by(func.count(Quote.id).desc())\
     .all()

    return render_template(
        "admin.html",
        quotes=quotes,
        total_quotes=total_quotes,

        quotes_per_day=json.dumps([
            {"date": str(day), "count": count}
            for day, count in quotes_per_day
        ]),

        top_services=json.dumps([
            {"service": service, "count": count}
            for service, count in top_services
        ]),

        active_page="admin"
    )


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

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run()