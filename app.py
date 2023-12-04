from flask import Flask, render_template
import cx_Oracle

app = Flask(__name__)

# Configuration de la base de données Oracle
app.config['ORACLE_USER'] = 'votre_utilisateur'
app.config['ORACLE_PASSWORD'] = 'votre_mot_de_passe'
app.config['ORACLE_DSN'] = 'votre_dsn'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/securite')
def securite():
    return render_template('securite.html')

#@app.route('/supervision')
#def supervision():
    # Ajoutez ici le code pour récupérer les informations de supervision depuis la base de données Oracle
   # return render_template('supervision.html')
# ...


@app.route('/supervision')
def supervision():
    # Connexion à la base de données Oracle
    connection = cx_Oracle.connect(app.config['ORACLE_USER'], app.config['ORACLE_PASSWORD'], app.config['ORACLE_DSN'])
    cursor = connection.cursor()

    # Ajoutez ici le code pour récupérer les informations de supervision depuis la base de données Oracle
    # Par exemple : 
    cursor.execute("SELECT * FROM table_supervision")
    supervision_data = cursor.fetchall()  # Ceci est un exemple, adaptez-le en fonction de votre structure de données

    # Fermez la connexion
    cursor.close()
    connection.close()

    return render_template('supervision.html', supervision_data=supervision_data)

if __name__ == '__main__':
    app.run(debug=True)
# Importez le module cx_Oracle en haut du fichier

