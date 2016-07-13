#-*- encoding=UTF-8 -*-

from Intasgraph import app, db, login_manager
from models import Image, User, Comment
from flask import render_template, redirect, flash, get_flashed_messages, request
from flask_login import login_user, logout_user, login_required, current_user
import random
import hashlib
import json


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


def redirect_with_msg(target, msg, category):
    if msg is not None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/')
def index():
    paginate = Image.query.paginate(page=1, per_page=3, error_out=False)
    return render_template('index.html', images=paginate.items, has_next=paginate.has_next)


@app.route('/index/images/<int:page_id>/<int:page_size>/')
def index_images(page_id, page_size):
    paginate = Image.query.paginate(page=page_id, per_page=page_size, error_out=False)
    json_data = {'zhang': 'SB250', 'has_next': paginate.has_next}
    images = []
    for m in paginate.items:
        user = User.query.filter_by(id=m.user_id).first()
        comments = Comment.query.filter_by(image_id=m.id).all()
        contens = []
        cuser_ids = []
        cuser_names = []
        for c in comments:
            contens.append(c.content)
            cuser_ids.append(c.user_id)
            cuser_names.append(c.user.username)
        imgvo = {'image_user_username': user.username, 'image_comments_length': len(m.comments), 'image_id': m.id, \
                 'image_url': m.url, 'image_user_id': user.id, 'comment_content': contens, 'comment_user_id': cuser_ids,\
                 'image_user_head_url': user.head_url, 'comment_user_username': cuser_names}
        images.append(imgvo)
    json_data['images'] = images
    return json.dumps(json_data)


@app.route('/image/<int:image_id>/')
@login_required
def image(image_id):
    image = Image.query.get(image_id)
    if image is None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3, error_out=False)
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)


@app.route('/profile/images/<int:user_id>/<int:page_id>/<int:page_size>/')
@login_required
def user_iamges(user_id, page_id, page_size):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page_id, per_page=page_size, error_out=False)
    json_data = {'zhang':'SB250', 'has_next':paginate.has_next}
    images = []
    for m in paginate.items:
        imgvo = {'id': m.id, 'url': m.url, 'comment_count': len(m.comments)}
        images.append(imgvo)
    json_data['images'] = images
    return json.dumps(json_data)


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect_with_msg('/relogin/', u'', category='relogin')
    elif request.method == "POST":
        username = request.values.get('username')
        password = request.values.get('password')
        if username is None or password is None:
            return redirect_with_msg('/relogin/', u'用户名或者密码为空', category='relogin')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return redirect_with_msg('/relogin/', u'用户不存在', category='relogin')
        m = hashlib.md5()
        m.update(password + user.salt)
        if m.hexdigest() != user.password:
            return redirect_with_msg('/relogin/', u'密码错误', category='relogin')
        login_user(user)
        next_page = request.values.get('next')
        if next_page is not None and next_page.startswith('/') > 0:
            return redirect(next_page)
        return redirect('/')


@app.route('/relogin/')
def relogin():
    msg = ''
    for m in get_flashed_messages(with_categories=False):
        msg += m
    return render_template('login.html', msg=msg, next=request.values.get('next'))#这里的ｎｅｘｔ是Ｆｌａｓｋ－Ｌｏｇｉｎ自动提交？


@app.route('/reg/', methods = ["GET", "POST"])
def reg():
    username = request.values.get('username')
    password = request.values.get('password')
    if username is None or password is None:
        return redirect_with_msg('/login/', u'用户名或密码为空', category='relogin')
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return redirect_with_msg('/login/', u'用户名已经存在', category='relogin')
    #yihou做更多验证。。。。
    m = hashlib.md5()
    salt = '.'.join(random.sample('123456789qwertyuiopasdfghjklzxcvbnm', 10))
    m.update(password + salt)
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    next_page = request.values.get('next')
    if next_page is not None and next_page.startswith('/') > 0:
        return redirect(next_page)
    return redirect('/')
