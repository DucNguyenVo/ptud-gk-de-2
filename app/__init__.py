from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_default_admin():
    from app.models import User
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True,
            avatar='https://ui-avatars.com/api/?name=Admin&background=red'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Tài khoản admin đã được tạo thành công!')
        print('Username: admin')
        print('Password: admin123')

def create_app():
    app = Flask(__name__)
    
    # Cấu hình
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/img/avatars')
    
    # Khởi tạo extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Đảm bảo thư mục upload tồn tại
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Import và đăng ký blueprints
    from app.routes import main
    from app.auth import auth
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    with app.app_context():
        db.create_all()
        create_default_admin()  # Tạo tài khoản admin mặc định
    
    return app 