# Gestionnaire de Mots de Passe

Une application Flask sécurisée pour gérer vos mots de passe.

## Fonctionnalités

- Stockage sécurisé des mots de passe avec chiffrement
- Génération de mots de passe forts
- Évaluation de la force des mots de passe
- Interface utilisateur intuitive
- Protection contre les attaques CSRF
- Gestion des sessions utilisateur

## Prérequis

- Python 3.8+
- pip
- virtualenv (recommandé)

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/votre-username/password-manager.git
cd password-manager
```

2. Créer et activer l'environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

5. Initialiser la base de données :
```bash
flask db upgrade
```

## Utilisation

1. Démarrer l'application :
```bash
flask run
```

2. Accéder à l'application dans votre navigateur :
```
http://localhost:5000
```

## Sécurité

- Les mots de passe sont chiffrés avec Fernet (AES-128-CBC)
- Protection CSRF intégrée
- Validation des entrées utilisateur
- Gestion sécurisée des sessions
- Stockage sécurisé des clés de chiffrement

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 