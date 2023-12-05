from flask import Flask, render_template
import cx_Oracle
from config import ORACLE_CONFIG

app = Flask(__name__)

app.config['ORACLE_DSN'] = (
    f"(DESCRIPTION="
    f"    (ADDRESS=(PROTOCOL=TCP)(HOST={ORACLE_CONFIG['HOST']})(PORT={ORACLE_CONFIG['PORT']}))"
    f"    (CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME={ORACLE_CONFIG['SERVICE_NAME']}))"
    f")"
)

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
    try:
        connection = cx_Oracle.connect(
            ORACLE_CONFIG['USER'],
            ORACLE_CONFIG['PASSWORD'],
            app.config['ORACLE_DSN']
        )
        cursor = connection.cursor()

        # Ajoutez ici le code pour récupérer les informations de supervision depuis la base de données Oracle
        # Par exemple :
        cursor.execute("SELECT * FROM personne")
        supervision_data = cursor.fetchall()  # Ceci est un exemple, adaptez-le en fonction de votre structure de données

        # Fermez la connexion
        cursor.close()
        connection.close()

        message = "Connexion à la base de données réussie."

    except cx_Oracle.Error as e:
        # Gestion de l'erreur en cas d'échec de la connexion
        print("Erreur de connexion à la base de données:", e)
        message = "Échec de la connexion à la base de données."

    return render_template('supervision.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
# Importez le module cx_Oracle en haut du fichier

