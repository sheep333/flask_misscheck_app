from flask import Flask, render_template, session, redirect, url_for, flash, abort
from form import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ttcxgRRgEFRAb5LR3akzrExXmyU4_f5A'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///misscheck.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ENV'] = True;

db = SQLAlchemy(app)

def hash_password(original_pass):
    return generate_password_hash(original_pass)

def verify_password(hash_pass, original_pass):
    return check_password_hash(hash_pass, original_pass)

def get_model_dict(model):
    return dict((column.name, getattr(model, column.name))
            for column in model.__table__.columns)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @staticmethod
    def login(email, password):
        '''
        ログイン実行
        '''
        u = User.query.filter_by(email=email).first()
        if u and verify_password(u.password, password):
            return u
        return None


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String,nullable=True)
    publish_date = db.Column(db.DateTime,nullable=True, default=datetime.now)
    content = db.Column(db.Text,nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user = db.relationship('User')

class MissCategory(db.Model):
    __tablename__ = 'miss_category'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String,nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)
    #ForeignKeys
    user = db.relationship('User')

class Miss(db.Model):
    __tablename__ = 'miss'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    category_id = db.Column(db.ForeignKey('miss_category.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String,nullable=True)
    content = db.Column(db.Text,nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)
    #ForeignKeys
    user = db.relationship('User')
    miss_category = db.relationship('MissCategory')

@app.route("/")
def index():
    posts = []
    misses = []
    if 'auth.user' in session:
        posts = Post.query.filter(Post.user_id == session['auth.user']['id']).order_by(Post.publish_date.desc()).all()
        misses = Miss.query.filter(Miss.user_id == session['auth.user']['id']).all()
    return render_template('index.html',posts=posts,misses = misses)


@app.route("/signup",methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u:
            flash('そのメールアドレスは既に利用されています。')
            return redirect(url_for('.signup'))

        user = User()
        form.populate_obj(user)
        user.password = hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('ユーザー登録が完了しました。ログインして下さい')
        return redirect(url_for(".signup"))

    return render_template('signup.html',form=form)


@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.login(form.email.data, form.password.data)
        if u is None:
            flash('ユーザー名とパスワードの組み合わせが違います。')
            return redirect(url_for('.login'))

        session['auth.user'] = get_model_dict(u)
        return redirect(url_for('.index'))

    return render_template(
        'login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.login'))

@app.route("/add_cat",methods=['GET','POST'])
def add_cat():
    form = MissCategoryForm() #フォーム作成
    if form.validate_on_submit():
        cat = MissCategory() #クラス(とテーブル定義が結びついたもの)作成
        form.populate_obj(cat)
        cat.id = None
        cat.user_id = session['auth.user']['id']
        db.session.add(cat)
        db.session.commit()

        flash('カテゴリーを登録しました！')
        return redirect(url_for(".index"))
    return render_template('add_cat.html', form=form)

@app.route("/add_miss",methods=['GET','POST'])
def add_miss():
    form = MissForm()
    categories = [(miss_cat.id, miss_cat.title) for miss_cat in MissCategory.query.all()]
    form.category.choices = categories
    if form.validate_on_submit():
        miss = Miss()
        form.populate_obj(miss)
        miss.id = None
        miss.category_id = form.category.data
        miss.user_id = session['auth.user']['id']
        db.session.add(miss)
        db.session.commit()

        flash('ミスを告白しました！')
        return redirect(url_for(".index"))
    return render_template('add_miss.html', form=form)

@app.route('/miss/<int:miss_id>')
def miss(miss_id):
    miss = Miss.query.filter(Miss.user_id == session['auth.user']['id'],Miss.id == miss_id).first()
    if not miss:
        abort(404)

    return render_template('miss.html',miss=miss)

@app.route('/category/<int:category_id>')
def category(category_id):
    miss_lists_by_category = Miss.query.filter(Miss.user_id == session['auth.user']['id'],Miss.category_id == category_id).all()
    if not miss:
        abort(404)

    return render_template('category.html',miss_lists_by_category = miss_lists_by_category)


@app.route('/edit_miss/<int:miss_id>')
def edit_miss(miss_id):
    miss = Miss.query.filter(Miss.user_id == session['auth.user']['id'],Miss.id == miss_id).first()
    form = MissForm()
    categories = [(miss_cat.id, miss_cat.title) for miss_cat in MissCategory.query.all()]
    form.category.choices = categories
    if not miss:
        abort(404)

    form.category.data = miss.category_id
    form.title.data = miss.title
    form.content.data = miss.content
    form.id.data = miss.id
    return render_template('update_miss.html',miss=miss,form=form)

@app.route('/update_miss/',methods=['POST'])
def update_miss():
    form = MissForm()
    categories = [(miss_cat.id, miss_cat.title) for miss_cat in MissCategory.query.all()]
    form.category.choices = categories
    #formカテゴリーデータを入れたい
    if form.validate_on_submit():
        miss = Miss.query.filter(Miss.user_id == session['auth.user']['id'],Miss.id == form.id.data).first()
        if form.update.data:
            # 更新
            miss.category_id = form.category.data
            miss.title = form.title.data
            miss.content = form.content.data
            db.session.add(miss)
            flash('記事内容を更新しました')
        else:
            # 削除
            db.session.delete(miss)
            flash('記事を削除しました')

        db.session.commit()
        return redirect(url_for('.index'))
    return redirect(url_for('.edit_miss',miss_id=form.id.data))

@app.route('/summary_miss/')
def summary_miss():
    miss_lists = Miss.query.filter(Miss.user_id == session['auth.user']['id']).order_by(Miss.modified).all()

    return render_template('summary_miss.html',miss_lists=miss_lists)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
