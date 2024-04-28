from flask import Flask
from app import app, stockage

# Mock de la configuration d'Oracle
ORACLE_CONFIG = {
    'USER': 'ousmane',
    'PASSWORD': '1234',
    'HOST': 'localhost',
    'PORT': '1521',
    'SERVICE_NAME': 'orcl',
}

def test_stockage_route():
    app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
    with app.test_client() as client:
        response = client.get('/stockage')
        assert response.status_code == 200
        # Ajoutez d'autres assertions pour vérifier le contenu de la réponse si nécessaire
