from flask import Flask, redirect, render_template,request, url_for, session
import cx_Oracle
from config import ORACLE_CONFIG
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import smtplib
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from datetime import datetime
from flask_scss import Scss
import tkinter as tk
from tkinter import ttk
import plotly.graph_objs as go
import json
import numpy as np
app = Flask(__name__)

app.config['ORACLE_DSN'] = (
    f"(DESCRIPTION="
    f"    (ADDRESS=(PROTOCOL=TCP)(HOST={ORACLE_CONFIG['HOST']})(PORT={ORACLE_CONFIG['PORT']}))"
    f"    (CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME={ORACLE_CONFIG['SERVICE_NAME']}))"
    f")"
)
def update_pie_chart():
    # Mettre à jour le graphique à l'intérieur de cette fonction
    total_space = 100  # Remplacer cela par vos propres données
    disk_usage = {'free': 50}  # Remplacer cela par vos propres données

    plt.clf()  # Efface le graphique précédent
    plt.pie([total_space, disk_usage['free']], labels=['Occupied Space (GB)', 'Free Space (GB)'], autopct='%1.1f%%', startangle=90)
    plt.draw()  # Dessine le nouveau graphique

    # Créer une fenêtre Tkinter
    root = tk.Tk()
    root.title("Disk Usage")

    # Créer un widget pour afficher le graphique
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Ajouter un bouton pour mettre à jour le graphique
    update_button = ttk.Button(root, text="Update", command=update_pie_chart)
    update_button.pack()

    # Fonction pour quitter l'application proprement
    def close_window():
        root.destroy()

    # Lier la fonction de fermeture de fenêtre à l'événement de fermeture de la fenêtre
    root.protocol("WM_DELETE_WINDOW", close_window)

    # Lancer la boucle principale d'événements
    root.mainloop()



import plotly.graph_objs as go
import plotly.express as px
@app.route('/teste')
def teste():
    try:
        connection = cx_Oracle.connect(
            ORACLE_CONFIG['USER'],
            ORACLE_CONFIG['PASSWORD'],
            app.config['ORACLE_DSN']
        )
        
       
            # Closing cursor and connection
        cursor.close()
        connection.close()


        return render_template('alerte.html')

    except cx_Oracle.Error as e:
        return f"Erreur de connexion à la base de données: {e}"

@app.route('/incident')
def incident():
    try:
        connection = cx_Oracle.connect(
            ORACLE_CONFIG['USER'],
            ORACLE_CONFIG['PASSWORD'],
            app.config['ORACLE_DSN']
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM V$DIAG_INFO")
        results = cursor.fetchall()
       
        
        # Extraction des données pour le diagramme
        labels = [row[0] for row in results]
        values = [row[1] for row in results]

            # Création des données de la barre
        bar = go.Bar(
            x=values,
            y=labels,
            orientation='v',  # horizontal
            marker=dict(color='rgb(65, 105, 225)')  # Couleur de la barre
        )
        # Création de la mise en page du graphique
        layout = go.Layout(
            title='Diagramme à barres des résultats de la requête',
            xaxis=dict(title='Valeurs'),  # Titre de l'axe x
            yaxis=dict(title='Labels'),  # Titre de l'axe y
            plot_bgcolor='rgba(0,0,0,0)',  # Couleur de fond du graphique
            paper_bgcolor='rgba(0,0,0,0)',  # Couleur de fond du papier
            font=dict(color='black')  # Couleur du texte
        )

        # Création de la figure
        fig = go.Figure(data=[bar], layout=layout)

        # Convertir le graphique en code HTML
        graph_html1 = fig.to_html(full_html=False)

            # Closing cursor and connection
        cursor.close()
        connection.close()


        return render_template('incident.html',graph_html=graph_html1)

    except cx_Oracle.Error as e:
        return f"Erreur de connexion à la base de données: {e}"


 



@app.route("/awr")
def awr():
    try:
        conn = cx_Oracle.connect(
            ORACLE_CONFIG['USER'],
            ORACLE_CONFIG['PASSWORD'],
            app.config['ORACLE_DSN']
        )

        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                SQL_ID,
                EXECUTIONS_DELTA AS EXECUTIONS,
                ELAPSED_TIME_DELTA / 1000000 AS ELAPSED_TIME_SEC,
                CPU_TIME_DELTA / 1000000 AS CPU_TIME_SEC,
                IOWAIT_DELTA / 1000000 AS IOWAIT_SEC,
                CLWAIT_DELTA / 1000000 AS CLWAIT_SEC,
                APWAIT_DELTA / 1000000 AS APWAIT_SEC,
                ROWS_PROCESSED_DELTA
            FROM 
                DBA_HIST_SQLSTAT
            ORDER BY 
                SQL_ID DESC
        """)
        
        # Récupérer les résultats de la requête
        data = []
        for row in cursor.fetchall():
            data.append({
                'SQL_ID': row[0],
                'EXECUTIONS': row[1],
                'ELAPSED_TIME_SEC': row[2],
                'CPU_TIME_SEC': row[3],
                'IOWAIT_SEC': row[4],
                'CLWAIT_SEC': row[5],
                'APWAIT_SEC': row[6],
                'ROWS_PROCESSED_DELTA': row[7]
            })
        cursor = conn.cursor()
        cursor.execute("""
            SELECT NAME, BYTES/1024/1024 AS MEGABYTES
            FROM V$SGAINFO
        """)
        data = cursor.fetchall()
        
        # Formater les données pour Chart.js
        labels = [row[0] for row in data]
        values = [row[1] for row in data]


        cursor.execute("""
            SELECT sql_id, sql_text, executions, buffer_gets, disk_reads, cpu_time, elapsed_time
            FROM (SELECT sql_id, sql_text, executions, buffer_gets, disk_reads, cpu_time, elapsed_time,
                         ROW_NUMBER() OVER (ORDER BY cpu_time DESC) AS cpu_rank
                  FROM (SELECT sql_id, sql_text, executions, buffer_gets, disk_reads, cpu_time, elapsed_time
                        FROM v$sql
                        WHERE sql_text NOT LIKE '%v$sql%'
                        ORDER BY cpu_time DESC)
                 )
            WHERE cpu_rank <= 10
        """)
        
        # Récupère tous les résultats
        results = cursor.fetchall()

        return render_template('awr.html', data=data, labels=labels, values=values, results=results)

    except cx_Oracle.Error as e:
        return f"Erreur de connexion à la base de données: {e}"






# Route pour le formulaire d'inscription
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    messages = None  # Initialisez la variable de message à None
    try:
        conn = cx_Oracle.connect(
            ORACLE_CONFIG['USER'],
            ORACLE_CONFIG['PASSWORD'],
            app.config['ORACLE_DSN']
        )
        cursor = conn.cursor()
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            cursor = conn.cursor()
            # Exécution de la requête d'insertion
            cursor.execute("INSERT INTO utilisateurs (username, email, password) VALUES (:username, :email, :password)",
                        {'username': username, 'email': email, 'password': password})
            conn.commit()
            cursor.close()
            messages = 'Utilisateur enregistré avec succès !'
            return render_template('login.html',messages=messages,show_popup=True)
    except cx_Oracle.Error as e:
        # Gestion de l'erreur en cas d'échec de la connexion
        print("Erreur de connexion à la base de données:", e)
        message = "Échec de la connexion à la base de données." # Définissez la liste des utilisateurs comme vide en cas d'échec de la connexion
        sessions = []
        sql_queries = []
    return render_template('login.html')

@app.route('/')
def home():
    
    return render_template('login.html')

def disconnect_user(username):
    try:
        conn = cx_Oracle.connect(ORACLE_CONFIG['USER'], ORACLE_CONFIG['PASSWORD'], app.config['ORACLE_DSN'])
        cursor = conn.cursor()

        # Sélectionnez SID et SERIAL# pour l'utilisateur spécifié
        query = "SELECT sid, serial# FROM v$session WHERE username = :username"
        cursor.execute(query, username=username)
        result = cursor.fetchone()

        # Vérifiez s'il y a une session pour l'utilisateur
        if result:
            sid, serial = result
            # Utilisez les valeurs SID et SERIAL# pour déconnecter la session
            cursor.execute(f"ALTER SYSTEM KILL SESSION '{sid},{serial}' IMMEDIATE")
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            # Aucune session trouvée pour l'utilisateur spécifié
            cursor.close()
            conn.close()
            return False
    except cx_Oracle.Error as e:
        print("Erreur lors de la déconnexion de l'utilisateur:", e)
        return False


@app.route("/disconnect", methods=['POST'])
def disconnect():
    username = request.form.get('username')
    if disconnect_user(username):
        return "Utilisateur déconnecté avec succès."
    else:
        return "Erreur lors de la déconnexion de l'utilisateur."


@app.route('/home', methods=['GET', 'POST'])
def acceuil():
    rows = []
    result=[]
    users=[]
    tables=[]
    try:
        conn = cx_Oracle.connect(
        ORACLE_CONFIG['USER'],
        ORACLE_CONFIG['PASSWORD'],
        app.config['ORACLE_DSN']
            )
        
        cursor = conn.cursor()
        query = """ SELECT * FROM connection_log ORDER BY login_time DESC FETCH FIRST 5 ROWS ONLY """

        cursor.execute(query)
        result = cursor.fetchall()

        # Exécutez la requête SQL pour obtenir la liste des utilisateurs
        query1 = "SELECT username FROM dba_users WHERE created > SYSDATE - 30  AND default_tablespace NOT IN ('SYSTEM', 'SYSAUX') ORDER BY created ";

        cursor.execute(query1)

        users = [row[0] for row in cursor.fetchall()]

        query_tables = "SELECT table_name FROM all_tables WHERE owner = 'OUSMANE'"
        cursor.execute(query_tables)
        tables = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT OWNER, TABLE_NAME, TABLESPACE_NAME, NUM_ROWS, LAST_ANALYZED FROM ALL_TABLES FETCH FIRST 15 ROWS ONLY")
        rows = cursor.fetchall()
        
         # Transformation des données en format adapté pour Chart.js
        owners = [row[0] for row in rows]
        num_rows = [row[3] for row in rows]
        
        query1 = "SELECT username FROM dba_users WHERE created > SYSDATE - 30 AND default_tablespace NOT IN ('SYSTEM', 'SYSAUX') ORDER BY created"
        cursor.execute(query1)
        users_conn = cursor.fetchall()

        quer=("SELECT name, value FROM v$sysstat WHERE name LIKE 'bytes%'")

        # Récupérer les résultats de la requête
        cursor.execute(quer)
        data = cursor.fetchall()
        names = [row[0] for row in data]
        values = [row[1] for row in data]

        # Créer un diagramme circulaire avec Plotly
        pie_chart = go.Pie(labels=names, values=values)

        # Convertir le diagramme circulaire en HTML
        graph_html = go.Figure(pie_chart).to_html(full_html=False)
        now = datetime.now().strftime("%H:%M:%S")

        

        cursor.close()
        conn.close()
        
        return render_template('home.html', current_date=now,graph=graph_html,users_conn=users_conn, owners=owners, num_rows=num_rows,rows=rows, result=result,users=users,tables=tables)
    except cx_Oracle.Error as e:
        return f"Erreur de connexion à la base de données: {e}"

@app.route("/audit",  methods=['GET', 'POST'])
def audit():
    try:
        conn = cx_Oracle.connect(
            ORACLE_CONFIG['USER'],
            ORACLE_CONFIG['PASSWORD'],
             app.config['ORACLE_DSN']
        )

        if request.method == 'POST':
            selected_user = request.form['users']
            audit_results = perform_audit(conn, selected_user)
            return render_template('audit.html', audit_results=audit_results)
        else:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM dba_users WHERE created > SYSDATE - 30  AND default_tablespace NOT IN ('SYSTEM', 'SYSAUX') ORDER BY created")
            users = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()
        
        return render_template('audit.html', users=users)

    except cx_Oracle.Error as e:
        return f"Erreur de connexion à la base de données: {e}"

def perform_audit(conn, username):
    cursor = conn.cursor()
    query = """
        SELECT TIMESTAMP, OS_USERNAME, USERHOST, TERMINAL, ACTION_NAME, OBJ_NAME, SQL_TEXT
        FROM (
            SELECT TIMESTAMP, OS_USERNAME, USERHOST, TERMINAL, ACTION_NAME, OBJ_NAME, SQL_TEXT
            FROM DBA_AUDIT_TRAIL
            WHERE USERNAME = :username
            ORDER BY TIMESTAMP DESC
        )
        WHERE ROWNUM <= 10
    """
    cursor.execute(query, username=username)
    audit_results = cursor.fetchall()
    cursor.close()
    return audit_results


@app.route('/login', methods=['GET', 'POST'])
def login():
    messages = None
    if request.method == 'POST':
        try:
            conn = cx_Oracle.connect(
                ORACLE_CONFIG['USER'],
                ORACLE_CONFIG['PASSWORD'],
                app.config['ORACLE_DSN']
            )
            cursor = conn.cursor()
            
            email = request.form['email']
            password = request.form['password']

            # Exécuter la requête pour vérifier si l'utilisateur existe
            cursor.execute("SELECT * FROM utilisateurs WHERE email = :email AND password = :password", {'email': email, 'password': password})
            user = cursor.fetchone()  # Récupérer le premier utilisateur correspondant

            cursor.close()
            conn.close()

            if user:
                # Utilisateur trouvé, rediriger ou afficher un message de succès
                return redirect(url_for('acceuil'))
            else:
                # Utilisateur non trouvé, afficher un message d'erreur
                messages = "L'email ou le mot de passe est incorrect."
        except cx_Oracle.Error as e:
            print("Erreur de connexion à la base de données:", e)
            messages = "Échec de la connexion à la base de données."
    
    return render_template('login.html',messages=messages)

@app.route('/supervision')
def supervision():
    try:
        connection = cx_Oracle.connect(
            ORACLE_CONFIG['USER'],
            ORACLE_CONFIG['PASSWORD'],
            app.config['ORACLE_DSN']
        )
        cursor = connection.cursor()
       

        # Récupérez tous les utilisateurs dans une liste

        

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
        message = "Échec de la connexion à la base de données." # Définissez la liste des utilisateurs comme vide en cas d'échec de la connexion
        sessions = []
        sql_queries = []
    return render_template('supervision.html', message=message, sessions=sessions, sql_queries=sql_queries)

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
        
        # Obtention de l'espace disponible sur le système d'exploitation (exemple avec shutil)
        #import shutil
        #disk_usage = shutil.disk_usage("C:\\")  # Remplacez "/path/to/your/drive" par le chemin de votre disque

        # Génération du diagramme circulaire
        
        cursor = connection.cursor()
        cursor.execute("""
        SELECT t1.tablespace_name,
               ROUND((MAXbytes - Usedbytes) / 1024 / 1024, 2) AS FreeSpaceMB,
               ROUND((Usedbytes / 1024 / 1024), 2) AS UsedSpaceMB,
               ROUND((MAXbytes / 1024 / 1024), 2) AS TotalSpaceMB,
               ROUND(((Usedbytes / MAXbytes) * 100), 2) AS UsedPercent
        FROM (SELECT tablespace_name,
                     SUM(bytes) Usedbytes
              FROM dba_segments
              GROUP BY tablespace_name) t1,
             (SELECT tablespace_name,
                     SUM(bytes) MAXbytes
              FROM dba_data_files
              GROUP BY tablespace_name) t2
        WHERE t1.tablespace_name = t2.tablespace_name
    """)
    
        # Fetching all rows from the cursor
        tablespace_rows = cursor.fetchall()

        cursor = connection.cursor()
        cursor.execute("""
        SELECT t1.tablespace_name,
               ROUND((MAXbytes - Usedbytes) / 1024 / 1024, 2) AS FreeSpaceMB,
               ROUND((Usedbytes / 1024 / 1024), 2) AS UsedSpaceMB,
               ROUND((MAXbytes / 1024 / 1024), 2) AS TotalSpaceMB,
               ROUND(((Usedbytes / MAXbytes) * 100), 2) AS UsedPercent
        FROM (SELECT tablespace_name,
                     SUM(bytes) Usedbytes
              FROM dba_segments
              GROUP BY tablespace_name) t1,
             (SELECT tablespace_name,
                     SUM(bytes) MAXbytes
              FROM dba_data_files
              GROUP BY tablespace_name) t2
        WHERE t1.tablespace_name = t2.tablespace_name
    """)
    
    
        # Récupération des résultats
        results = cursor.fetchall()

        cursor.execute("SELECT SUM(bytes) FROM dba_data_files")
        result1 = cursor.fetchone()
        occupied_space_bytes = result1[0]
        occupied_space_gb = occupied_space_bytes / (1024 ** 3)  # Convertir en gigaoctets

        # Récupérer la capacité totale du disque C
        total_space_gb = 1000  # Remplacez par la capacité totale réelle de votre disque C en gigaoctets

        # Calculer le pourcentage d'espace occupé
        occupancy_percentage = (occupied_space_gb / total_space_gb) * 100

        # Closing cursor and connection
        cursor.close()
        connection.close()


        return render_template('stockage.html',data=tablespace_rows,results=results,occupied_space_gb=occupied_space_gb, total_space_gb=total_space_gb, occupancy_percentage=occupancy_percentage)

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

# Établir une connexion à la base de données Oracle
connection = cx_Oracle.connect(
     ORACLE_CONFIG['USER'],
     ORACLE_CONFIG['PASSWORD'],
     app.config['ORACLE_DSN'],
     encoding="UTF-8"
)
cursor = connection.cursor()

try:
    # Exécuter la requête pour récupérer le nombre de sessions actives
    cursor.execute("SELECT COUNT(*) FROM v$session WHERE status = 'ACTIVE'")
    active_sessions_count = cursor.fetchone()[0]

    # Exécuter la requête pour récupérer les noms d'utilisateur des sessions actives distinctes
    cursor.execute("SELECT DISTINCT username FROM v$session WHERE status = 'ACTIVE'")
    active_users = cursor.fetchall()

    # Paramètres d'envoi d'e-mail
    from_email = "weuzskr@gmail.com"
    to_email = "sankhare1999@outlook.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "weuzskr@gmail.com"
    smtp_password = "jmwl dutn dxnb ojcc"

    # Construire le corps du message avec les informations récupérées
    message_body = f"Nombre de sessions actives : {active_sessions_count}\n\n"
    message_body += "Utilisateurs actifs sont  : \n"
    for user in active_users:
        message_body += f"- {user[0]}\n"

    # Créer l'objet MIMEText
    msg = MIMEText(message_body)

    # Configurer l'en-tête du message
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "Rapport de Supervision Oracle"

    try:
        # Configurer le serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)

        # Envoyer l'e-mail
        #server.sendmail(from_email, to_email, msg.as_string())
        print("E-mail envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {str(e)}")
    finally:
        # Fermer la connexion SMTP
        server.quit() if "server" in locals() else None

except Exception as e:
    print(f"Erreur lors de l'exécution de la requête SQL : {str(e)}")
finally:
    # Fermer la connexion Oracle
    cursor.close()
    connection.close()

#def handle_login_failure(username, ip_address):
    #with cx_Oracle.connect(app.config['ORACLE_DSN']) as connection:
        #with connection.cursor() as cursor:
            #cursor.callproc('handle_login_failure', [username, ip_address])

@app.route('/loginn', methods=['POST'])
def loggin():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Code pour la vérification des informations d'identification
    # ...

    # En cas d'échec de connexion, appelez la fonction handle_login_failure
    #handle_login_failure(username, request.remote_addr)
    
    return render_template('home.html')

@app.route('/connexion', methods=['POST'])
def tentative_connexion():

    return render_template('votre_page_html.html')


    

if __name__ == '__main__':
    app.run(debug=True)
