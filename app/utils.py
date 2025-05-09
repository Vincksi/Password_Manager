from cryptography.fernet import Fernet
from flask import current_app
import string
import random
import re

def get_encryption_key():
    """Génère ou récupère la clé de chiffrement"""
    key = current_app.config.get('ENCRYPTION_KEY')
    if not key:
        key = Fernet.generate_key()
        current_app.config['ENCRYPTION_KEY'] = key
    return key

def encrypt_password(password):
    """Chiffre un mot de passe"""
    f = Fernet(get_encryption_key())
    return f.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    """Déchiffre un mot de passe"""
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted_password.encode()).decode()

def evaluate_password_strength(password):
    """
    Évalue la robustesse d'un mot de passe et retourne un score de 0 à 100
    et des suggestions d'amélioration.
    """
    score = 0
    suggestions = []

    # Longueur
    if len(password) < 8:
        suggestions.append("Le mot de passe devrait faire au moins 8 caractères")
    else:
        score += min(len(password) * 4, 40)  # Max 40 points pour la longueur

    # Complexité
    if re.search(r'[A-Z]', password):
        score += 15
    else:
        suggestions.append("Ajoutez des lettres majuscules")
    
    if re.search(r'[a-z]', password):
        score += 15
    else:
        suggestions.append("Ajoutez des lettres minuscules")
    
    if re.search(r'[0-9]', password):
        score += 15
    else:
        suggestions.append("Ajoutez des chiffres")
    
    if re.search(r'[^A-Za-z0-9]', password):
        score += 15
    else:
        suggestions.append("Ajoutez des caractères spéciaux")

    # Évaluation finale
    if score < 40:
        strength = "Très faible"
    elif score < 60:
        strength = "Faible"
    elif score < 80:
        strength = "Moyen"
    elif score < 90:
        strength = "Fort"
    else:
        strength = "Très fort"

    return {
        'score': score,
        'strength': strength,
        'suggestions': suggestions
    }

def generate_secure_password(length=16, include_uppercase=True, include_lowercase=True,
                           include_numbers=True, include_special=True):
    """
    Génère un mot de passe sécurisé avec les critères spécifiés.
    """
    characters = ''
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    if not characters:
        raise ValueError("Au moins un type de caractère doit être inclus")

    # S'assurer que le mot de passe contient au moins un caractère de chaque type sélectionné
    password = []
    if include_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if include_lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if include_numbers:
        password.append(random.choice(string.digits))
    if include_special:
        password.append(random.choice(string.punctuation))

    # Compléter le reste du mot de passe
    remaining_length = length - len(password)
    password.extend(random.choice(characters) for _ in range(remaining_length))

    # Mélanger le mot de passe
    random.shuffle(password)
    return ''.join(password)