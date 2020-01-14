from alayatodo import app, db
from flask import (
    redirect,
    render_template,
    request,
    flash,
    jsonify
    )
from flask_paginate import Pagination, get_page_parameter
from flask_login import current_user, login_required, logout_user, login_user
from alayatodo.models import User, Todo


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = f.read()
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user == None or user.password != password:
        return redirect('/login')
    if user:
        login_user(user)
        return redirect('/todo')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todo.query.filter_by(id=id).first()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
@login_required
def todos():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = app.config['TODO_PER_PAGE']
    todos = Todo.query.paginate(page, app.config['TODO_PER_PAGE'], False)
    total_todos = Todo.query.count()
    pagination = Pagination(page=page, per_page=per_page, total=total_todos, record_name='todos', css_framework='foundation')
    return render_template('todos.html', todos=todos.items, pagination=pagination)


@app.route('/todo/<id>/json', methods=['GET'])
@login_required
def todo_json(id):
    todo = Todo.query.filter_by(id=id).first()
    return jsonify(todo.make_dict())


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
@login_required
def todos_POST():
    description = request.form.get('description')
    if description == "":
        flash("Description can't be blank")
        return redirect('/todo')
    todo = Todo(user_id=current_user.id, description=description)
    db.session.add(todo)
    db.session.commit()
    flash("New Todo added")
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted")
    return redirect('/todo')


@app.route('/todo/<id>/completed/<status>', methods=['POST'])
@login_required
def todo_completed(id, status):
    todo = Todo.query.filter_by(id=id).first()
    if status == '1':
        todo.mark_completed()
        db.session.commit()
        return redirect('/todo')
    else:
        todo.mark_uncompleted()
        db.session.commit()
        return redirect('/todo')