from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(200), default='default.jpg')
    is_admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='assigned_to', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_overdue_tasks_count(self):
        return Task.query.filter_by(
            user_id=self.id,
            status='pending',
            finished=None
        ).filter(Task.due_date < datetime.utcnow()).count()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    created = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    finished = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def is_overdue(self):
        return self.status == 'pending' and self.due_date and self.due_date < datetime.utcnow() 