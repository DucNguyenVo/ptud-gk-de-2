from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app.models import Task, User, db
from datetime import datetime
from functools import wraps
import os
from werkzeug.utils import secure_filename
import requests
import random

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_upload_folder():
    upload_folder = os.path.join(current_app.root_path, 'static', 'img', 'avatars')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    return upload_folder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Bạn không có quyền truy cập trang này!')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/update_avatar', methods=['POST'])
@login_required
def update_avatar():
    try:
        if 'avatar' not in request.files:
            return jsonify({'success': False, 'message': 'Không tìm thấy file'}), 400
        
        file = request.files['avatar']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Chưa chọn file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Thêm timestamp vào tên file để tránh trùng lặp
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            
            upload_folder = get_upload_folder()
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            # Cập nhật URL avatar trong database
            avatar_url = url_for('static', filename=f'img/avatars/{filename}')
            current_user.avatar = avatar_url
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Upload avatar thành công',
                'avatar_url': avatar_url
            })
        
        return jsonify({'success': False, 'message': 'File không hợp lệ'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi: {str(e)}'}), 500

@main.route('/generate_avatar')
@login_required
def generate_avatar():
    styles = ['adventurer', 'avataaars', 'bottts', 'pixel-art', 'personas']
    style = random.choice(styles)
    avatar_url = f'https://api.dicebear.com/6.x/{style}/svg?seed={current_user.username}'
    
    current_user.avatar = avatar_url
    db.session.commit()
    flash('Đã tạo avatar mới thành công!')
    return redirect(url_for('main.profile'))

@main.route('/')
@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        # Admin xem tất cả tasks
        tasks = Task.query.order_by(Task.created.desc()).all()
    else:
        # User thường chỉ xem tasks của mình
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created.desc()).all()
    overdue_count = current_user.get_overdue_tasks_count()
    return render_template('dashboard.html', tasks=tasks, overdue_count=overdue_count)

@main.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@main.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
        except:
            due_date = None
            
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            user_id=current_user.id
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash('Task created successfully')
        return redirect(url_for('main.dashboard'))
    return render_template('task/new.html')

@main.route('/task/<int:task_id>/complete')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized')
        return redirect(url_for('main.dashboard'))
        
    task.status = 'completed'
    task.finished = datetime.utcnow()
    db.session.commit()
    
    flash('Task marked as complete')
    return redirect(url_for('main.dashboard'))

@main.route('/task/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized')
        return redirect(url_for('main.dashboard'))
        
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted')
    return redirect(url_for('main.dashboard'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html') 