from flask import Flask, session, render_template, redirect, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/flask/test2.db'
app.config['SECRET_KEY'] = 'asdfasdf:'
app.config['DEBUG'] = True
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    content = db.Column(db.Text())
    timing = db.Column(db.Integer)
    persons = db.Column(db.Integer)
    ingredients = db.Column(db.Text())
    tools = db.Column(db.Text())
    summary = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

manager.add_command("db", MigrateCommand)

@app.route('/')
def index():
    return render_template('recettes.html', recettes = Receipt.query.all())

@app.route('/new', methods = ['POST'])
def new_receipt():
    receipt = Receipt(request.form['name'])
    receipt.timing = request.form['timing']
    receipt.persons = request.form['persons']
    receipt.summary = request.form['summary']
    receipt.ingredients = request.form['ingredients']
    receipt.tools = request.form['tools']
    receipt.content = request.form['content']
    db.session.add(receipt)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    manager.run()
