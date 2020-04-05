from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
from os.path import join, dirname
import psycopg2
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'username'

# connecting to database
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

if os.environ.get('DATABASE_URL'):
    DATABASE_URL = os.environ['DATABASE_URL']
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
else:
    con = psycopg2.connect(
        host=os.environ.get('host'),
        database=os.environ.get('database'),
        user=os.environ.get('user'),
        password=os.environ.get('password'),
        port=os.environ.get('port')
    )

cur = con.cursor()

user_name = None


def reseq(table_name):
    post_id = []
    cur.execute('select id from {}'.format(table_name))
    for id in cur.fetchall():
        post_id.append(id[0])

    if post_id:
        max_id = max(post_id)
    else:
        max_id = 0

    cur.execute('alter sequence {}_id_seq restart with {}'.format(table_name, max_id + 1))


# home page
@app.route('/')
def home():
    cur.execute('select * from posts')
    posts = cur.fetchall()
    print(session)
    if posts:
        latest_post = posts[-1]
    else:
        latest_post = []
    return render_template('home.html', posts=posts, latest_post=latest_post)


# posting page
@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'GET':
        return render_template('post.html')
    else:
        reseq("posts")

        data = request.form
        heading = data['heading']
        subtitle = data['subtitle']
        article = data['article']
        author = username

        cur.execute('insert into posts ("heading", "subtitle", "article", "author") values (%s, %s, %s, %s)',
                    (heading, subtitle, article, author))
        con.commit()

        return redirect('/')


# article page
@app.route('/article/<id>')
def ok(id):
    cur.execute('select article from posts where id={}'.format(id))
    article = cur.fetchall()

    return render_template('article.html', article=article[0][0])


# manage page
@app.route('/manage')
def manage():
    cur.execute('select * from posts')
    posts = cur.fetchall()
    return render_template('manage.html', posts=posts, sign='out')


# delete function
@app.route('/delete')
def delete():
    id = request.args['id']
    cur.execute('delete from posts where id=%s', id)
    con.commit()
    return redirect('/manage')


# edit function
@app.route('/edit', methods=['POST', 'GET'])
def edit():
    id = request.args['id']
    cur.execute('select * from posts where id=%s', id)
    edit_post = cur.fetchall()[0]
    if request.method == 'GET':
        return render_template('edit.html', post=edit_post)
    else:
        data = request.form

        heading = data['heading']
        subtitle = data['subtitle']
        article = data['article']
        author = data['author']

        cur.execute('update posts set heading=%s, subtitle=%s, article=%s, author=%s where id=%s',
                    (heading, subtitle, article, author, id))
        con.commit()
        return redirect('/manage')


# sign in function and page
@app.route('/sign', methods=['POST', 'GET'])
def sign():
    if request.method == 'GET':
        return render_template('sign.html')
    else:
        reseq("users")

        username = request.form['username']
        password = request.form['password']

        print(username, password)

        cur.execute('select * from users where name=%s', [username])
        user = cur.fetchall()
        if user:
            return render_template('sign.html', error=True)
        else:
            cur.execute('insert into users (name, password) values (%s,%s)', (username, password))
            con.commit()
            session['active_user'] = username
        return redirect('/')


# log in function and page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']

        cur.execute('select * from users where name=%s', [username])
        users = cur.fetchall()

        if users:
            if password == users[0][2]:
                session['active_user'] = username
                return redirect('/')
            else:
                return render_template('login.html', error='incorrect password')
        else:
            return render_template('login.html', error='n/a')


# sign out function
@app.route('/signout')
def signout():
    session.pop('active_user', None)
    return redirect('/')


@app.route('/test')
def test():
    return request.data


if __name__ == '__main__':
    app.run(debug=True, port=3000)
