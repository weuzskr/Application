from flask import Flask, render_template,request
import cx_Oracle
from config import ORACLE_CONFIG
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

app = Flask(__name__)

app.config['ORACLE_DSN'] = (
    f"(DESCRIPTION="
    f"    (ADDRESS=(PROTOCOL=TCP)(HOST={ORACLE_CONFIG['HOST']})(PORT={ORACLE_CONFIG['PORT']}))"
    f"    (CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME={ORACLE_CONFIG['SERVICE_NAME']}))"
    f")"
)

@app.route('/')
def home():

    connection = cx_Oracle.connect(
    ORACLE_CONFIG['USER'],
    ORACLE_CONFIG['PASSWORD'],
    app.config['ORACLE_DSN']
        )
    cursor = connection.cursor()
    query = """ SELECT * FROM sys.connection_log ORDER BY login_time DESC FETCH FIRST 5 ROWS ONLY """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return render_template('home.html',result=result)

#@app.route('/securite')
#def securite():
 #   return render_template('securite.html')

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
        # Exécutez la requête SQL pour obtenir la liste des utilisateurs
        query = "SELECT username FROM all_users WHERE ROWNUM <= 5"
        cursor.execute(query)

        # Récupérez tous les utilisateurs dans une liste
        users = [row[0] for row in cursor.fetchall()]

        query_tables = "SELECT table_name FROM all_tables WHERE owner = 'OUSMANE'"
        cursor.execute(query_tables)
        tables = [row[0] for row in cursor.fetchall()]

        query_sessions = " SELECT USERNAME,MACHINE,PROGRAM,LOGON_TIME FROM V$SESSION WHERE TRUNC(LOGON_TIME) = TRUNC(SYSDATE) "

        cursor.execute(query_sessions)
        sessions = cursor.fetchall()

        query_sql = """
        SELECT
            SQL_TEXT,
            LAST_ACTIVE_TIME
        FROM
            V$SQL
        WHERE
            PARSING_USER_ID = (SELECT USER_ID FROM DBA_USERS WHERE USERNAME = 'OUSMANE')
            AND TRUNC(LAST_ACTIVE_TIME) = TRUNC(SYSDATE)
        """
        cursor.execute(query_sql)
        sql_queries = cursor.fetchall()

        cursor.close()
        connection.close()

        message = "Connexion à la base de données réussie."

    except cx_Oracle.Error as e:
        # Gestion de l'erreur en cas d'échec de la connexion
        print("Erreur de connexion à la base de données:", e)
        message = "Échec de la connexion à la base de données."
        users = []  # Définissez la liste des utilisateurs comme vide en cas d'échec de la connexion
        tables = []
        sessions = []
        sql_queries = []
    return render_template('supervision.html', message=message, users=users,tables=tables, sessions=sessions, sql_queries=sql_queries)

# Configuration de la connexion Oracle



@app.route('/stockage')
def stockage():
    try:
        connection = cx_Oracle.connect(
            ORACLE_CONFIG['USER'],
            ORACLE_CONFIG['PASSWORD'],
            app.config['ORACLE_DSN']
        )
        cursor = connection.cursor()

        # Exécution de la requête SQL pour obtenir la taille totale de l'espace de stockage de la base de données
        query_sql_total_space = """
            SELECT
                ROUND(SUM(bytes) / POWER(1024, 3), 2) AS total_space_gb
            FROM
                dba_data_files
        """
        cursor.execute(query_sql_total_space)
        total_space = cursor.fetchone()[0]

        # Obtention de l'espace disponible sur le système d'exploitation (exemple avec shutil)
        import shutil
        disk_usage = shutil.disk_usage("C:\\")  # Remplacez "/path/to/your/drive" par le chemin de votre disque

        # Génération du diagramme circulaire
        plt.pie([total_space, disk_usage.free / (1024 ** 3)], labels=['Occupied Space (GB)', 'Free Space (GB)'], autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Enregistrement du diagramme dans un objet BytesIO
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        # Conversion de l'image en base64 pour l'afficher dans le template HTML
        image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

        # Fermeture des ressources
        plt.close()
        cursor.close()
        connection.close()

        return render_template('stockage.html', total_space=total_space, free_space=disk_usage.free / (1024 ** 3), image_base64=image_base64)

    except cx_Oracle.Error as e:
        return f"Erreur de connexion à la base de données: {e}"


@app.route('/dashboard')
def dashboard():
    try:
        connection = cx_Oracle.connect(
            ORACLE_CONFIG['USER'],
            ORACLE_CONFIG['PASSWORD'],
            app.config['ORACLE_DSN']
        )

        # Exécuter les requêtes et récupérer les résultats
        cursor = connection.cursor()

        cursor.execute("SELECT name, value FROM V$SYSSTAT WHERE name IN ('physical reads', 'physical writes')")
        result1 = cursor.fetchall()

        cursor.execute("SELECT METRIC_NAME, VALUE FROM V$SYSMETRIC WHERE METRIC_NAME = 'CPU Usage Per Sec'")
        result2 = cursor.fetchall()

        cursor.execute("SELECT METRIC_NAME, VALUE FROM V$SYSMETRIC WHERE METRIC_NAME LIKE 'Host CPU Utilization%' OR METRIC_NAME LIKE 'SGA Memory%' OR METRIC_NAME LIKE 'PGA Memory%'")
        result3 = cursor.fetchall()

        cursor.execute("SELECT DISTINCT METRIC_NAME FROM V$SYSMETRIC")
        result4 = cursor.fetchall()

        cursor.execute("SELECT METRIC_NAME, VALUE FROM V$SYSMETRIC WHERE METRIC_NAME LIKE 'Host CPU Utilization%' OR METRIC_NAME LIKE 'SGA Memory%' OR METRIC_NAME LIKE 'PGA Memory%' OR METRIC_NAME LIKE 'CPU Usage Per Sec%'")
        result5 = cursor.fetchall()

        # Fermer les curseurs et la connexion à la base de données
        cursor.close()
        connection.close()

    # Rendre le modèle HTML avec les résultats
    
        return render_template('dashboard.html', result1=result1, result2=result2, result3=result3, result4=result4, result5=result5)

    except cx_Oracle.Error as e:
        return f"Erreur de connexion à la base de données: {e}"

# ...




def handle_login_failure(username, ip_address):
    with cx_Oracle.connect(app.config['ORACLE_DSN']) as connection:
        with connection.cursor() as cursor:
            cursor.callproc('handle_login_failure', [username, ip_address])

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Code pour la vérification des informations d'identification
    # ...

    # En cas d'échec de connexion, appelez la fonction handle_login_failure
    handle_login_failure(username, request.remote_addr)
    
    return render_template('home.html')
from flask import Flask, render_template, request, session
#import cx_Oracle

@app.route('/connexion', methods=['POST'])
def tentative_connexion():
    username = request.form['username']
    password = request.form['password']

    # Configurez votre DSN Oracle
    dsn = (
        f"(DESCRIPTION="
        f"    (ADDRESS=(PROTOCOL=TCP)(HOST={ORACLE_CONFIG['HOST']})(PORT={ORACLE_CONFIG['PORT']}))"
        f"    (CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME={ORACLE_CONFIG['SERVICE_NAME']}))"
        f")"
    )

    try:
        # Tentez de vous connecter à la base de données Oracle
        connection = cx_Oracle.connect(username, password, dsn)

        # Enregistrez la tentative de connexion réussie dans la session utilisateur
        session['connexion_reussie'] = True
        connection.close()

    except cx_Oracle.DatabaseError as e:
        # Enregistrez la tentative de connexion échouée dans la session utilisateur
        session['connexion_reussie'] = False

    return render_template('votre_page_html.html')



if __name__ == '__main__':
    app.run(debug=True)

















if __name__ == '__main__':
    app.run(debug=True)
# Importez le module cx_Oracle en haut du fichier

