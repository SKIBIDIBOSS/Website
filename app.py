from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)

# ======================
# DATABASE
# ======================

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    tier = db.Column(db.String(10))

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

# ======================
# LOGIN SYSTEM
# ======================

USERNAME = "skibidiboss123"
PASSWORD = "skibidiboss123"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]

        if user == USERNAME and pw == PASSWORD:
            session["user"] = user
            return redirect("/dashboard")

    return render_template("login.html")

# ======================
# LANDING PAGE
# ======================

@app.route("/")
def home():
    players = Player.query.all()
    return render_template("leaderboard.html", players=players)

# ======================
# QUEUE SYSTEM
# ======================

@app.route("/join_queue", methods=["POST"])
def join_queue():
    name = request.form["name"]
    q = Queue(name=name)
    db.session.add(q)
    db.session.commit()
    return redirect("/")

# ======================
# DASHBOARD (ADMIN/TESTER)
# ======================

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    queue = Queue.query.all()

    if request.method == "POST":
        name = request.form["name"]
        tier = request.form["tier"]

        player = Player(name=name, tier=tier)
        db.session.add(player)

        # remove from queue
        q = Queue.query.filter_by(name=name).first()
        if q:
            db.session.delete(q)

        db.session.commit()

    return render_template("dashboard.html", queue=queue)

# ======================
# RUN
# ======================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=3000)
