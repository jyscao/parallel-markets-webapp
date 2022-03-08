import flask as flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

import datetime, os, os.path

APP_DATADIR = "/tmp/parallel-markets"
DB_FILEPATH = f"{APP_DATADIR}/app.db"
UPLOAD_FOLDER = f"{APP_DATADIR}/uploads"


app = flask.Flask(__name__)
app.secret_key = b"super secret key for parallel markets"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILEPATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
db = SQLAlchemy(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    if flask.request.method == "GET":
        return flask.render_template("index.html")
    elif flask.request.method == "POST":
        save_investor_info()
        return flask.redirect(flask.url_for("index"))
    else:
        assert False, "this should never be reached!"


def save_investor_info():
    try:
        fdat = flask.request.form
        investor = init_investor(fdat)
        db.session.add(investor)

        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        for f in flask.request.files.getlist("files"):
            doc = init_document(f, investor)
            db.session.add(doc)

        db.session.commit()
        flask.flash(f"success: investor {fdat['firstname']} {fdat['lastname']} saved", "error")

    except ValueError:
        flask.flash("failure: please enter all info in the correct format", "error")


def init_investor(form_data):
    return Investor(
        firstname    = form_data["firstname"].strip(),
        lastname     = form_data["lastname"].strip(),
        dob          = get_dob_data(form_data["dob"]),
        phone_number = "".join(form_data["phone-num"].split("-")),

        addr_street = form_data['address-street'],
        addr_state  = form_data['address-state'],
        addr_zip    = form_data['address-zip'],
    )


def init_document(f, investor):
    fname = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
    return Document(
        filename = fname,
        investor = investor,
    )


def get_dob_data(dob_str):
    return datetime.date(*[int(dt) for dt in dob_str.split("-")])


class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    addr_street = db.Column(db.String(128), nullable=False)
    addr_state  = db.Column(db.String(2), nullable=False)
    addr_zip    = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f"<Investor: {self.firstname} {self.lastname}>"


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)

    investor_id = db.Column(db.Integer, db.ForeignKey('investor.id'), nullable=False)
    investor = db.relationship('Investor', backref=db.backref('documents', lazy=True))

    def __repr__(self):
        return f"<Uploaded document: {self.filename}>"
