from flask import Flask, render_template, render_template_string, request, url_for, redirect, flash, make_response, has_request_context
from sqlalchemy import and_, or_, not_
from datetime import datetime, date
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
from flask_paginate import Pagination, get_page_parameter
import time
import os

from .models import TS_Task, TS_User, db
from .sconfig import desteam, tstatus, rteam
from .config import file_log
from .func import *

#For logs
class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)

formatter = RequestFormatter('[%(asctime)s] [%(levelname)s] from %(remote_addr)s req: %(url)s > %(message)s')

#Init App
app = create_app()
db.init_app(app)
manager = LoginManager(app)
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
handler = RotatingFileHandler(file_log, maxBytes=1048576, backupCount=10)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)


@manager.user_loader
def load_user(user_id):
    return TS_User.query.get(user_id)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/myprofile')
@login_required
def myprofile():
    app.logger.info('[FUNC] [/MyProfile] [Succeess] User:<%s>',current_user.login)
    rid = f_rid_get(request)
    return render_template("myprofile.html", user=current_user, rteam=rteam, rid=rid)


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        ulogin = request.form['login']
        upassword = request.form['password']
        user = TS_User.query.filter_by(login=ulogin).first()
        if user and check_password_hash(user.password, upassword):
            login_user(user)
            resp = make_response(redirect(url_for('myprofile')))
            resp.set_cookie('rid', str(user.rid))
            app.logger.info('[AUTH] [LOGIN] [Succeess] User:<%s>, role: <%s>', current_user.login, current_user.rid)
            return resp
        else:
            flash('Login or password incorrect')
            app.logger.warning('[AUTH] [LOGIN] [Failed] User:<%s> Password:<%s>', ulogin, upassword)
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


@app.route('/logout', methods=['POST','GET'])
@login_required
def logout():
    app.logger.info('[AUTH] [LOGOUT] [Succeess] User:<%s>', current_user.login)
    logout_user()
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('rid', "", 0)
    return resp


@app.route('/reg', methods=['POST','GET'])
def reg():
    if request.method == "POST":
        ulogin=request.form['login']
        upassword=request.form['password']
        if not(ulogin or upassword):
            flash('Please, fill fileds: login, password')
            return redirect('/reg')
        elif not(TS_User.query.filter_by(login=ulogin).first()) and ulogin and upassword:
            user = TS_User(login=ulogin, password=generate_password_hash(upassword), email=request.form['email'], rid=0, token="")
            try:
                db.session.add(user)
                db.session.commit()
                app.logger.info('[AUTH] [REG] [Succeess] User:<%s>', ulogin)
                return redirect('/login')
            except:
                app.logger.error('[AUTH] [REG] [Failed] User:<%s>. Error DB insert.', ulogin)
                flash('Error DB insert')
                return redirect('/reg')
        else:
            app.logger.warning('[AUTH] [REG] [Failed] Please, enter other login or not null login or not null password')
            flash('Please, enter other login or not null login or not null password')
            return redirect('/reg')
    else:
        return render_template("reg.html")


@app.route('/passrec', methods=['POST','GET'])
def passrec():
    p = 0
    token = ""
    if len(request.args) > 0:
        if request.args.get('login'):
            ulogin = request.args.get('login')
            user = TS_User.query.filter(TS_User.login==ulogin).first()
            if user:
                token = jwt_encod(user)
                user.token = token
                try:
                    db.session.add(user)
                    db.session.commit()
                    flash('Token created...')
                    app.logger.info('[AUTH] [passrec] [Succeess] For User:<%s> token <%s> created', ulogin, token)
                except:
                    app.logger.error('[AUTH] [passrec] [Failed] User:<%s>. Error DB insert.', ulogin)
                    flash('Error DB insert')
            else:
                flash('Login incorrect')
                app.logger.warning('[AUTH] [passrec] [Failed] User:<%s> does not exist', ulogin)
        if request.args.get('token') and not request.args.get('password'):
            token = request.args.get('token')
            try:
                token_data = jwt_decod(token)
                app.logger.info('[AUTH] [passrec] [Succeess] For token: <%s> exist data: <%s>', token, token_data)
            except:
                p = 0
                token_data = ""
                flash('Token incorrect')
                app.logger.error('[AUTH] [passrec] [Failed] Token: <%s> incorrect', token)
            if token_data:
                uid = token_data["id"]
                user = TS_User.query.filter(TS_User.id==uid).first()
                if user:
                    p = 1
                    app.logger.info('[AUTH] [passrec] [Succeess] For token: <%s> exist user: <%s>', token, user.login)
                    return render_template("recpass.html", p=p, token=token)
                else:
                    p = 0
                    flash('Token incorrect')
                    app.logger.error('[AUTH] [passrec] [Failed] Token: <%s> incorrect. Not exist user.', token)
            else:
                p = 0
                app.logger.error('[AUTH] [passrec] [Failed] Token: <%s> incorrect. Not exist data.', token)
                flash('Token incorrect')
        if request.args.get('token') and request.args.get('password'):
            token = request.args.get('token')
            try:
                token_data = jwt_decod(token)
            except:
                p = 0
                token_data = ""
                app.logger.error('[AUTH] [passrec] [Failed] Token: <%s> incorrect. Not exist data. Password: <%s>', token, request.args.get('password'))
                flash('Token incorrect')
            if token_data:
                uid = token_data["id"]
                user = TS_User.query.filter(TS_User.id==uid).first()
                if user:
                    p = 0
                    user.password = generate_password_hash(request.args.get('password'))
                    user.token = ""
                    try:
                        db.session.add(user)
                        db.session.commit()
                        app.logger.info('[AUTH] [passrec] [Succeess] For User:<%s> change password', user.login)
                    except:
                        app.logger.error('[AUTH] [passrec] [Failed] User:<%s>. Error DB insert.', user.login)
                        flash('Error DB insert')
            else:
                p = 0
                flash('Token incorrect')
                app.logger.error('[AUTH] [passrec] [Failed] Token: <%s> incorrect. Not exist data.', token)
    else:
        pass
    return render_template("recpass.html", p=p, token=token)


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect('/login')
    return response


@app.route('/mytask')
@login_required
def mytask():
    tasks = TS_Task.query.filter(TS_Task.uid1==current_user.id).order_by(TS_Task.date.desc()).all()
    return render_template('task_mylist.html', tasks=tasks, desteam=desteam, tstatus=tstatus)


@app.route('/taskcreate', methods=['POST'])
@login_required
def taskcreate():
    if request.method == "POST":
        if (len(request.form['title']) > 2 and type(int(request.form['did'])) == int and type(eval(request.form['private'])) == bool):
            task = TS_Task(did=int(request.form['did']), title=request.form['title'], description=request.form['description'], private=eval(request.form['private']), uid1=current_user.id, uid2=-1)
            try:
                db.session.add(task)
                db.session.commit()
                app.logger.info('[FUNC] [/taskcreate] [Succeess] User:<%s> Title:<%s> Description:<%s>',current_user.login, task.title, task.description)
                return redirect(url_for('mytask'))
            except:
                app.logger.error('[FUNC] [/taskcreate] [Failed] User:<%s> Error DB insert',current_user.login)
                flash('Error DB insert')
                return redirect(url_for('mytask'))
        else:
            flash('Please, enter all rewuired data!')
            return redirect(url_for('mytask'))
    else:
        return redirect(url_for('mytask'))


@app.route('/task/<int:tid>')
@login_required
def task_detail(tid):
    task = TS_Task.query.filter(TS_Task.tid==tid).order_by(TS_Task.date.desc()).first()
    rid = f_rid_get(request)
    if task:
        task_access = f_task_acl(task, rid, current_user.id)
        if task_access:
            user2 = TS_User.query.filter(TS_User.id==task.uid2).order_by(TS_User.date.desc()).first()
            app.logger.info('[FUNC] [/task] [Succeess] User:<%s> Role:<%d> Read task: <%s> owner:<%s>', current_user.login, rid, task.tid, task.TS_User.login)
            return render_template("task_detail.html", task=task, tstatus=tstatus, desteam=desteam, user2=user2)
        else:
            return redirect(url_for('tasklist'))
    else:
        return redirect(url_for('tasklist'))


@app.route('/task/<int:tid>/edit', methods=['POST','GET'])
@login_required
def task_edit(tid):
    task = TS_Task.query.filter(and_(TS_Task.uid1==current_user.id, TS_Task.tid==tid)).order_by(TS_Task.date.desc()).first()
    if task:
        if request.method == "POST":
            if (len(request.form['title']) > 2 and type(int(request.form['did'])) == int and type(eval(request.form['private'])) == bool):
                task.title = request.form['title']
                task.description = request.form['description']
                task.did = int(request.form['did'])
                task.private = eval(request.form['private'])
                try:
                    db.session.commit()
                    app.logger.info('[FUNC] [/task/edit] [Succeess] User:<%s> Edit task: <%s> owner:<%s>', current_user.login, task.tid, task.TS_User.login)
                    return redirect(url_for('mytask'))
                except:
                    app.logger.error('[FUNC] [/task/edit] [Failed] User:<%s> Edit task: <%s> owner:<%s>. Error DB insert/', current_user.login, task.tid, task.TS_User.login)
                    flash('Error DB insert')
                    return redirect('/task/' + str(tid) + '/edit')
            else:
                flash('Please, enter all rewuired data!')
                return redirect('/task/' + str(tid) + '/edit')
        else:
            return render_template("task_edit.html", task=task, desteam=desteam)
    else:
        app.logger.warning('[FUNC] [/task/edit] [Failed] User:<%s> Edit task: <%s> owner:<%s>', current_user.login, task.tid, task.TS_User.login)
        return redirect(url_for('mytask'))


@app.route('/task/<int:tid>/del')
@login_required
def task_del(tid):
    task = TS_Task.query.filter(and_(TS_Task.uid1==current_user.id, TS_Task.tid==tid)).order_by(TS_Task.date.desc()).first()
    if task:
        try:
            db.session.delete(task)
            db.session.commit()
            app.logger.info('[FUNC] [/task/del] [Succeess] User:<%s> Del task: <%s> owner:<%s>', current_user.login, task.tid, task.TS_User.login)
        except:
            app.logger.error('[FUNC] [/task/del] [Failed] User:<%s> Del task: <%s> owner:<%s>. Error DB delete!', current_user.login, task.tid, task.TS_User.login)
            return "Error DB delete!"
    else:
        app.logger.warning('[FUNC] [/task/del] [Failed] User:<%s> Del task: <%s> owner:<%s>. Task not found!', current_user.login, task.tid, task.TS_User.login)
    return redirect(url_for('mytask'))


@app.route('/tasklist')
@login_required
def tasklist():
    rid = f_rid_get(request)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    if rid == 2:
        tasks = TS_Task.query.order_by(TS_Task.tid.desc()).paginate(page=page, per_page=10)
    if rid == 1:
        tasks = TS_Task.query.filter(or_(TS_Task.private==False, and_(TS_Task.uid1==current_user.id, TS_Task.private==True))).order_by(TS_Task.tid.desc()).paginate(page=page, per_page=10)
    if rid == 0:
        tasks = TS_Task.query.filter(TS_Task.uid1==current_user.id).order_by(TS_Task.tid.desc()).paginate(page=page, per_page=10)
    pagination = Pagination(page=page, total=tasks.total, record_name='tasks')
    app.logger.info('[FUNC] [/tasklist] [Succeess] User:<%s> Role:<%d>/<%d>', current_user.login, current_user.rid, rid)
    return render_template('task_list.html', tasks=tasks, desteam=desteam, tstatus=tstatus, pagination=pagination)


@app.route('/task/<int:tid>/towork')
@login_required
def task_towork(tid):
    task = TS_Task.query.filter(TS_Task.tid==tid).order_by(TS_Task.date.desc()).first()
    rid = f_rid_get(request)
    if task:
        task_access = f_task_acl(task, rid, current_user.id)
        if task_access:
            task.uid2 = current_user.id
            try:
                db.session.commit()
                app.logger.info('[FUNC] [/task/towork] [Succeess] User:<%s> Role:<%d> get task: <%s> owner:<%s>', current_user.login, rid, task.tid, task.TS_User.login)
            except:
                app.logger.error('[FUNC] [/task/towork] [Failed] User:<%s> get task: <%s> owner:<%s>. Error DB delete!', current_user.login, task.tid, task.TS_User.login)
                return "Error DB delete!"
    else:
        app.logger.warning('[FUNC] [/task/towork] [Failed] User:<%s> get task: <%s> owner:<%s>. Task not found!', current_user.login, task.tid, task.TS_User.login)
    return redirect(url_for('tasklist'))


@app.route('/kanban')
@login_required
def kanban():
    tasks = TS_Task.query.filter(TS_Task.uid2==current_user.id).order_by(TS_Task.date.desc()).all()
    return render_template('task_kanban.html', tasks=tasks, desteam=desteam, tstatus=tstatus, login=current_user.login)


@app.route('/task/<int:tid>/bstatus')
@login_required
def task_bstatus(tid):
    task = TS_Task.query.filter(TS_Task.tid==tid).order_by(TS_Task.date.desc()).first()
    rid = f_rid_get(request)
    if task:
        task_access = f_task_acl(task, rid, current_user.id)
        if task_access:
            if task.kstatus != 0:
                task.kstatus -= 1
            try:
                db.session.commit()
                app.logger.info('[FUNC] [/task/bstatus] [Succeess] User:<%s> Role:<%d> BackStatus task: <%s> owner:<%s>', current_user.login, rid, task.tid, task.TS_User.login)
            except:
                app.logger.error('[FUNC] [/task/bstatus] [Failed] User:<%s> BackStatus task: <%s> owner:<%s>. Error DB delete!', current_user.login, task.tid, task.TS_User.login)
                return "Error DB delete!"
    else:
        app.logger.warning('[FUNC] [/task/bstatus] [Failed] User:<%s> BackStatus task: <%s> owner:<%s>. Task not found!', current_user.login, task.tid, task.TS_User.login)
    return redirect(url_for('kanban'))


@app.route('/task/<int:tid>/nstatus')
@login_required
def task_nstatus(tid):
    task = TS_Task.query.filter(TS_Task.tid==tid).order_by(TS_Task.date.desc()).first()
    rid = f_rid_get(request)
    if task:
        task_access = f_task_acl(task, rid, current_user.id)
        if task_access:
            if task.kstatus != 2:
                task.kstatus += 1
            try:
                db.session.commit()
                app.logger.info('[FUNC] [/task/nstatus] [Succeess] User:<%s> Role:<%d> NextStatus task: <%s> owner:<%s>', current_user.login, rid, task.tid, task.TS_User.login)
            except:
                app.logger.error('[FUNC] [/task/nstatus] [Failed] User:<%s> NextStatus task: <%s> owner:<%s>. Error DB delete!', current_user.login, task.tid, task.TS_User.login)
                return "Error DB delete!"
    else:
        app.logger.warning('[FUNC] [/task/nstatus] [Failed] User:<%s> NextStatus task: <%s> owner:<%s>. Task not found!', current_user.login, task.tid, task.TS_User.login)
    return redirect(url_for('kanban'))


@app.route('/userstatus')
@login_required
def userstatus():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    users = TS_User.query.order_by(TS_User.id.desc()).paginate(page=page, per_page=10)
    pagination = Pagination(page=page, total=users.total, record_name='users')
    return render_template("userstatus.html", users=users, pagination=pagination)


@app.route('/search', methods=['GET'])
@login_required
def search():
    tsearch = request.args.get('search')
    if tsearch:
        rid = f_rid_get(request)
        if rid == 2:
            tasks = TS_Task.query.filter(TS_Task.title.contains(tsearch)).order_by(TS_Task.date.desc()).all()
        if rid == 1:
            tasks = TS_Task.query.filter(and_(or_(TS_Task.private==False, and_(TS_Task.uid1==current_user.id, TS_Task.private==True)), TS_Task.title.contains(tsearch))).order_by(TS_Task.date.desc()).all()
        if rid == 0:
            tasks = TS_Task.query.filter(and_(TS_Task.uid1==current_user.id, TS_Task.title.contains(tsearch))).order_by(TS_Task.date.desc()).all()
        app.logger.info('[FUNC] [/search] [Succeess] User:<%s> Role:<%d> Data:<%s>',current_user.login, rid, tsearch)
        return render_template("searchlist.html", tasks=tasks, tstatus=tstatus, tsearch=render_template_string(tsearch))
    else:
        return redirect(url_for('index'))


@app.route('/adm')
@login_required
def adm():
    reg = 0
    rid = f_rid_get(request)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    if rid == 2:
        users = TS_User.query.order_by(TS_User.id.desc()).paginate(page=page, per_page=10)
        pagination = Pagination(page=page, total=users.total, record_name='users')
        app.logger.info('[FUNC] [/adminpanel] [Succeess] User:<%s> Role:<%d>/<%d> Read users: <%d>', current_user.login, current_user.rid, rid, len(users.items))
        return render_template("admpanel.html", users=users, rteam=rteam, reg=reg, pagination=pagination)
    else:
        users = TS_User.query.filter(TS_User.rid==2).order_by(TS_User.id.desc()).all()
        if len(users) == 0:
            reg = 1
            app.logger.info('[FUNC] [/adminpanel] [Succeess] User:<%s> Role:<%d>/<%d> Start initialization >> Registration of a new captain for the service', current_user.login, current_user.rid, rid)
            return render_template("admpanel.html", users=users, rteam=rteam, reg=reg)
        else:
            app.logger.warning('[FUNC] [/adminpanel] [Failed] User:<%s> Access is denied', current_user.login)
            return redirect(url_for('index'))


@app.route('/adm/<int:id>/nrteam')
@login_required
def adm_nrteam(id):
    rid = f_rid_get(request)
    if rid == 2:
        user = TS_User.query.filter(TS_User.id==id).order_by(TS_User.date.desc()).first()
        if user:
            if user.rid != 2:
                user.rid += 1
                try:
                    db.session.commit()
                    app.logger.info('[FUNC] [/adminpanel/nrteam] [Succeess] User:<%s> Role:<%d>/<%d> For user:<%s> upd role to:<%d>', current_user.login, current_user.rid, rid, user.login, user.rid)
                except:
                    app.logger.error('[FUNC] [/adminpanel/nrteam] [Succeess] User:<%s> Role:<%d> For user:<%s> upd role to:<%d>. Error DB delete!', current_user.login, current_user.rid, user.login, user.rid)
                    return "Error DB delete!"
        else:
            app.logger.warning('[FUNC] [/adminpanel/nrteam] [Failed] User:<%s> Role:<%d> For user:<%s> upd role to:<%d> User not found!', current_user.login, current_user.rid, user.login, user.rid)
        return redirect(url_for('adm'))
    else:
        redirect(url_for('index'))


@app.route('/adm/<int:id>/brteam')
@login_required
def adm_brteam(id):
    rid = f_rid_get(request)
    if rid == 2:
        user = TS_User.query.filter(TS_User.id==id).order_by(TS_User.date.desc()).first()
        if user:
            if user.rid != 0:
                user.rid -= 1
                try:
                    db.session.commit()
                    app.logger.info('[FUNC] [/adminpanel/brteam] [Succeess] User:<%s> Role:<%d>/<%d> For user:<%s> upd role to:<%d>', current_user.login, current_user.rid, rid, user.login, user.rid)
                except:
                    app.logger.error('[FUNC] [/adminpanel/brteam] [Succeess] User:<%s> Role:<%d> For user:<%s> upd role to:<%d>. Error DB delete!', current_user.login, current_user.rid, user.login, user.rid)
                    return "Error DB delete!"
        else:
            app.logger.warning('[FUNC] [/adminpanel/brteam] [Failed] User:<%s> Role:<%d> For user:<%s> upd role to:<%d> User not found!', current_user.login, current_user.rid, user.login, user.rid)
        return redirect(url_for('adm'))
    else:
        redirect(url_for('index'))


@app.route('/admreg', methods=['POST'])
@login_required
def admreg():
    if request.method == "POST":
        ulogin=request.form['login']
        upassword=request.form['password']
        if not(ulogin or upassword):
            flash('Please, fill fileds: login, password')
            return redirect(url_for('adm'))
        elif not(TS_User.query.filter_by(login=ulogin).first()) and ulogin and upassword:
            user = TS_User(login=ulogin, password=generate_password_hash(upassword), email=request.form['email'], rid=2, token="")
            try:
                db.session.add(user)
                db.session.commit()
                app.logger.info('[AUTH] [admreg] [Succeess] User:<%s> Role:<%d> registartion captain:<%s>',current_user.login, current_user.rid, ulogin)
                return redirect(url_for('adm'))
            except:
                app.logger.error('[AUTH] [admreg] [Failed] User:<%s>. Error DB insert.', ulogin)
                flash('Error DB insert')
                return redirect(url_for('adm'))
        else:
            app.logger.warning('[AUTH] [admreg] [Failed] Please, enter other login or not null login or not null password')
            flash('Please, enter other login or not null login or not null password')
            return redirect(url_for('adm'))
    else:
        redirect(url_for('index'))