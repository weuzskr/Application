# Projet Flask de Déconnexion d'Utilisateur

## Description
Ce projet est une application web simple développée avec Flask qui permet de déconnecter un utilisateur. Lorsqu'un utilisateur est déconnecté, un message de confirmation ou d'erreur est affiché sur une page dédiée avec une mise en forme soignée.

## Fonctionnalités
- Déconnexion de l'utilisateur via un formulaire.
- Affichage d'un message de succès ou d'erreur.
- Le nom de l'utilisateur est mis en évidence dans le message de déconnexion.

## Prérequis
- Python 3.x
- Flask

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/votre-utilisateur/votre-repo.git
    cd votre-repo
    ```

2. Créez et activez un environnement virtuel :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
Assurez-vous d'avoir une fonction `disconnect_user` définie dans votre projet. Voici un exemple de structure du fichier principal de l'application :

```python
from flask import Flask, request, render_template

app = Flask(__name__)

def disconnect_user(username):
    # Logique pour déconnecter l'utilisateur
    # Retourne True si la déconnexion est réussie, sinon False
    pass

@app.route("/disconnect", methods=['POST'])
def disconnect():
    username = request.form.get('username')
    if disconnect_user(username):
        msg = "Utilisateur déconnecté avec succès."
    else:
        msg = "Erreur lors de la déconnexion de l'utilisateur."
    return render_template('exit.html', msg=msg, username=username)

if __name__ == "__main__":
    app.run(debug=True)
