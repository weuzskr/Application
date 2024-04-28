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

with app.test_client() as client:

    def test_stockage_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/stockage')
            assert response.status_code == 200
            # Ajoutez d'autres assertions pour vérifier le contenu de la réponse si nécessaire

    def test_dashboard_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/dashboard')
            assert response.status_code == 200
            # Ajoutez d'autres assertions pour vérifier le contenu de la réponse si nécessaire

    def test_awr_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/awr')
            assert response.status_code == 200
            # Ajoutez d'autres assertions pour vérifier le contenu de la réponse si nécessaire
    def test_teste_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/teste')
            assert response.status_code == 200
            
            # Ajoutez d'autres assertions pour vérifier le contenu de la réponse si nécessaire

    def test_incident_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/incident')
            assert response.status_code == 200
            
            # Ajoutez d'autres assertions pour vérifier le contenu de la réponse si nécessaire

    def test_signup_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/signup')
            assert response.status_code == 200
            
    def test_audit_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/audit')
            assert response.status_code == 200
            
    def test_supervision_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/supervision')
            assert response.status_code == 200
           
    def test_login_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/login')
            assert response.status_code == 200
            
    def test_home_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/home')
            assert response.status_code == 200

    def test_home1_route():
        app.config['ORACLE_CONFIG'] = ORACLE_CONFIG
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200            
            
            # Ajoutez d'autres assertions pour vérifier le contenu de la réponse si nécessaire
