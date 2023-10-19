from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Tomiris"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


context = app.app_context()
with context:
    db.create_all()


@app.route("/")
def index():
    students: list[Student] = db.session.query(Student).all()

    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_user():
    user = Student(
        name=request.form.get("name"),
        email=request.form.get("email"),
        phone=request.form.get("phone"),
    )
    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/update/<int:id>", methods=["POST"])
def update_user(id):
    user = Student.query.get(id)
    user.name = request.form.get("name")
    user.email = request.form.get("email")
    user.phone = request.form.get("phone")
    db.session.commit()

    return redirect("/")


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = Student.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
