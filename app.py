from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from os.path import join, dirname
import psycopg2
import os

app = Flask(__name__)

# connecting to database
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

if os.environ.get('DATABASE_URL'):
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
else:
    con = psycopg2.connect(
        host=os.environ.get('host'),
        database=os.environ.get('database'),
        user=os.environ.get('user'),
        password=os.environ.get('password'),
        port=os.environ.get('port')
    )

cur = con.cursor()


# home page
@app.route('/')
def home():
    cur.execute('select * from posts order by id desc')

    posts = cur.fetchall()
    latest_post = posts[0]
    return render_template('home.html', posts=posts, latest_post=latest_post)


# posting page
@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'GET':
        return render_template('post.html')
    else:
        post_id = []
        cur.execute('select id from posts')
        for id in cur.fetchall():
            post_id.append(id[0])

        if post_id:
            max_id = max(post_id)
        else:
            max_id = 0

        cur.execute('alter sequence posts_id_seq restart with {}'.format(max_id + 1))

        data = request.form
        heading = data['heading']
        subtitle = data['subtitle']
        article = data['article']
        author = data['author']

        cur.execute('insert into posts ("heading", "subtitle", "article", "author") values (%s, %s, %s, %s)',
                    (heading, subtitle, article, author))
        con.commit()
        cur.execute('select * from posts')
        rows = cur.fetchall()

        return redirect('/post')


# article page
@app.route('/article/<id>')
def ok(id):
    cur.execute('select article from posts where id={}'.format(id))
    article = cur.fetchall()

    return render_template('article.html', article=article[0][0])


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


# edit function
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
