from alayatodo import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    completed = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Todo {}>'.format(self.description)

    def mark_completed(self):
        self.completed = 1

    def mark_uncompleted(self):
        self.completed = 0

    def make_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'description': self.description,
            'completed': True if self.completed==0 else False
        }