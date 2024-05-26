CREATE OR REPLACE PROCEDURE handle_login_failure (
    p_username IN VARCHAR2,
    p_ip_address IN VARCHAR2
) AS
BEGIN
    -- Enregistrez les détails de la tentative de connexion échouée dans une table de journal
    INSERT INTO login_failure_log (username, ip_address, attempt_timestamp)
    VALUES (p_username, p_ip_address, SYSTIMESTAMP);

    -- Vous pouvez également vérifier si le compte est bloqué et envoyer une alerte si nécessaire

    -- Envoyez une alerte JavaScript à l'application web
    DBMS_APPLICATION_INFO.SET_CLIENT_INFO('LOGIN_FAILURE');

    -- Vous pouvez également envoyer une alerte via DBMS_SCHEDULER ou une autre méthode
END;

/CREATE OR REPLACE PROCEDURE send_email_procedure(
    p_sender_email    IN VARCHAR2,
    p_recipient_email IN VARCHAR2,
    p_subject         IN VARCHAR2,
    p_body            IN VARCHAR2
) AS
    mail_conn   utl_smtp.connection;
BEGIN
    -- Ouvrir la connexion SMTP
    mail_conn := utl_smtp.open_connection('smtp.example.com', 25);
    
    -- Authentifier si nécessaire
    -- utl_smtp.helo(mail_conn, 'my_client.example.com');
    -- utl_smtp.command(mail_conn, 'AUTH LOGIN');
    -- utl_smtp.command(mail_conn, utl_raw.cast_to_varchar2(utl_encode.base64_encode(utl_raw.cast_to_raw('username'))));
    -- utl_smtp.command(mail_conn, utl_raw.cast_to_varchar2(utl_encode.base64_encode(utl_raw.cast_to_raw('password'))));
    
    -- Définir l'expéditeur et le destinataire
    utl_smtp.mail(mail_conn, p_sender_email);
    utl_smtp.rcpt(mail_conn, p_recipient_email);
    
    -- Écrire le message
    utl_smtp.open_data(mail_conn);
    utl_smtp.write_data(mail_conn, 'Subject: ' || p_subject);
    utl_smtp.write_data(mail_conn, 'From: ' || p_sender_email);
    utl_smtp.write_data(mail_conn, 'To: ' || p_recipient_email);
    utl_smtp.write_data(mail_conn, ' ');
    utl_smtp.write_data(mail_conn, p_body);
    utl_smtp.close_data(mail_conn);
    
    -- Fermer la connexion SMTP
    utl_smtp.quit(mail_conn);
EXCEPTION
    WHEN OTHERS THEN
        -- Gérer les erreurs
        NULL;
END;
/

