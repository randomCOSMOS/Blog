from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


# table
class Post(db.Model):
    def __init__(self, heading, subtitle, article, author):
        self.heading = heading
        self.subtitle = subtitle
        self.article = article
        self.author = author

    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    article = db.Column(db.String(100))
    author = db.Column(db.String(20))
    datetime = db.Column(db.DateTime, default=datetime.utcnow())


# home page
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    latest_post = posts[0]
    return render_template('home.html', posts=posts, latest_post=latest_post)


# posting page
@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'GET':
        return render_template('post.html')
    else:
        data = request.form
        heading = data['heading']
        subtitle = data['subtitle']
        article = data['article']
        author = data['author']

        new_post = Post(heading, subtitle, article, author)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/post')


# article page
@app.route('/article/<id>')
def ok(id):
    this_post = Post.query.get(id)
    return render_template('article.html', post=this_post)


# manage page
@app.route('/manage')
def manage():
    posts = Post.query.all()
    return render_template('manage.html', posts=posts)


# delete function
@app.route('/delete/<id>')
def delete(id):
    delete_post = Post.query.get(id)
    if delete_post is None:
        error = "Can't find post with id {}".format(id)
        return render_template('manage.html', error=error)
    else:
        db.session.delete(delete_post)
        db.session.commit()
        return redirect('/manage')


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    edit_post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('edit.html', post=edit_post)
    else:
        data = request.form

        edit_post.heading = data['heading']
        edit_post.subtitle = data['subtitle']
        edit_post.article = data['article']
        edit_post.author = data['author']
        db.session.commit()
        return redirect('/manage')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
