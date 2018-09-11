from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
    username = StringField('ユーザー名', validators=[
        DataRequired(message='ユーザー名が未登録です'),
        Length(max=10,message='ユーザー名は10文字までにして下さい')
    ])

    email = StringField('Eメールアドレス', validators=[
        Email(message='メールアドレスが未入力か、正しいアドレスではありません'),
    ])
    password = PasswordField('パスワード', validators=[
        DataRequired(message='パスワードを入力して下さい'),
    ])


class LoginForm(Form):
    email = StringField('Eメールアドレス', validators=[
        Email(message='メールアドレスが未入力か、正しいアドレスではありません'),
    ])
    password = PasswordField('パスワード', validators=[
        DataRequired(message='パスワードを入力して下さい'),
    ])


class MissCategoryForm(Form):
    title = StringField('ミスのカテゴリー', validators=[
        DataRequired(message='ミスのカテゴリーを入力して下さい'),
    ])
    update = SubmitField(label='更新する')
    delete = SubmitField(label='削除する')
    id = HiddenField()

class MissForm(Form):
    category = SelectField('ミスのカテゴリー', coerce=int)
    title = StringField('ミスの概要', validators=[
        DataRequired(message='ミスの概要を入力してください'),
    ])
    content = TextAreaField('ミスの詳細', validators=[
        DataRequired(message='ミスの詳細を入力して下さい'),
    ],id='editor')

    update = SubmitField(label='更新する')
    delete = SubmitField(label='削除する')
    id = HiddenField()
