from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import PasswordForm, PasswordGeneratorForm
from app.models import Password
from app.utils import encrypt_password, decrypt_password, evaluate_password_strength, generate_secure_password

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    passwords = Password.query.filter_by(user_id=current_user.id).all()
    return render_template('main/index.html', title='Home', passwords=passwords)

@bp.route('/add_password', methods=['GET', 'POST'])
@login_required
def add_password():
    form = PasswordForm()
    generator_form = PasswordGeneratorForm()
    
    if form.validate_on_submit():
        password = Password(
            title=form.title.data,
            username=form.username.data,
            encrypted_password=encrypt_password(form.password.data),
            url=form.url.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(password)
        db.session.commit()
        flash('Your password has been saved.')
        return redirect(url_for('main.index'))
    
    return render_template('main/add_password.html', 
                         title='Add Password', 
                         form=form,
                         generator_form=generator_form)

@bp.route('/generate_password', methods=['POST'])
@login_required
def generate_password():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract parameters with defaults
        length = int(data.get('length', 16))
        include_uppercase = data.get('include_uppercase', True)
        include_lowercase = data.get('include_lowercase', True)
        include_numbers = data.get('include_numbers', True)
        include_special = data.get('include_special', True)

        # Validate length
        if length < 8 or length > 64:
            return jsonify({'error': 'Password length must be between 8 and 64 characters'}), 400

        # Generate password
        password = generate_secure_password(
            length=length,
            include_uppercase=include_uppercase,
            include_lowercase=include_lowercase,
            include_numbers=include_numbers,
            include_special=include_special
        )
        return jsonify({'password': password})
    except Exception as e:
        current_app.logger.error(f'Error generating password: {str(e)}')
        return jsonify({'error': 'Error generating password'}), 500

@bp.route('/evaluate_password', methods=['POST'])
@login_required
def evaluate_password():
    try:
        data = request.get_json()
        if not data or 'password' not in data:
            return jsonify({'error': 'No password provided'}), 400
        
        password = data['password']
        if not isinstance(password, str):
            return jsonify({'error': 'Invalid password format'}), 400
            
        result = evaluate_password_strength(password)
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f'Error evaluating password: {str(e)}')
        return jsonify({'error': 'Error evaluating password strength'}), 500

@bp.route('/view_password/<int:id>')
@login_required
def view_password(id):
    password = Password.query.get_or_404(id)
    if password.user_id != current_user.id:
        flash('You do not have permission to view this password.')
        return redirect(url_for('main.index'))
    decrypted_password = decrypt_password(password.encrypted_password)
    return render_template('main/view_password.html', 
                         title='View Password',
                         password=password, 
                         decrypted_password=decrypted_password)

@bp.route('/delete_password/<int:id>')
@login_required
def delete_password(id):
    password = Password.query.get_or_404(id)
    if password.user_id != current_user.id:
        flash('You do not have permission to delete this password.')
        return redirect(url_for('main.index'))
    db.session.delete(password)
    db.session.commit()
    flash('Password has been deleted.')
    return redirect(url_for('main.index'))