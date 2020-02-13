from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


class User(db.Model):
    def __init__(self, name, location):
        self.name = name
        self.location = location

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.now)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/add', methods=['post'])
def add_to_db():
    user = request.form['user']
    location = request.form['location']

    new_task = User(user, location)
    try:
        db.session.add(new_task)
        db.session.commit()
    except:
        return "Error Occurred"

    return redirect('/')


@app.route('/delete page')
def show():
    return render_template('delete.html')


@app.route('/delete', methods=['post'])
def delete():
    user = request.form['user']
    if user == 'all':
        User.query.delete()
        db.session.commit()

        return redirect('/delete page')
    else:
        remove = User.query.filter_by(name=user).first()

        if remove is None:
            return render_template('delete.html', error="Cant find that")
        else:
            db.session.delete(remove)
            db.session.commit()
            return redirect('/delete page')


@app.route('/data')
def data():
    users = User.query.all()
    return render_template('see.html', users=users)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
