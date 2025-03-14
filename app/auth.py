from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db
import requests
import os
from werkzeug.utils import secure_filename
import random

auth = Blueprint('auth', __name__)

def get_random_avatar():
    try:
        # Sử dụng DiceBear API để tạo avatar
        styles = ['adventurer', 'avataaars', 'bottts', 'initials']
        style = random.choice(styles)
        avatar_url = f'https://api.dicebear.com/6.x/{style}/svg'
        response = requests.get(avatar_url)
        if response.status_code == 200:
            return avatar_url
        return 'https://ui-avatars.com/api/?name=User&background=random'
    except:
        return 'https://ui-avatars.com/api/?name=User&background=random'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password')
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))
            
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Tạo avatar từ username
        user.avatar = f'https://ui-avatars.com/api/?name={username}&background=random'
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 