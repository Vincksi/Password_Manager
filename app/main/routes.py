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
    form = PasswordGeneratorForm()
    if form.validate_on_submit():
        try:
            password = generate_secure_password(
                length=form.length.data,
                include_uppercase=form.include_uppercase.data,
                include_lowercase=form.include_lowercase.data,
                include_numbers=form.include_numbers.data,
                include_special=form.include_special.data
            )
            return jsonify({'password': password})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    return jsonify({'error': 'Invalid form data'}), 400

@bp.route('/evaluate_password', methods=['POST'])
@login_required
def evaluate_password():
    password = request.json.get('password')
    if not password:
        return jsonify({'error': 'No password provided'}), 400
    return jsonify(evaluate_password_strength(password))

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