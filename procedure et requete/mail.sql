CREATE OR REPLACE TRIGGER send_email_trigger
AFTER INSERT ON ma_table
FOR EACH ROW
DECLARE
    mail_conn utl_smtp.connection;
BEGIN
    -- Ouvrir la connexion SMTP
    mail_conn := utl_smtp.open_connection('smtp.example.com', 25);
    
    -- Authentifier si nécessaire
    -- utl_smtp.helo(mail_conn, 'my_client.example.com');
    -- utl_smtp.command(mail_conn, 'AUTH LOGIN');
    -- utl_smtp.command(mail_conn, utl_raw.cast_to_varchar2(utl_encode.base64_encode(utl_raw.cast_to_raw('username'))));
    -- utl_smtp.command(mail_conn, utl_raw.cast_to_varchar2(utl_encode.base64_encode(utl_raw.cast_to_raw('password'))));
    
    -- Définir l'expéditeur et le destinataire
    utl_smtp.mail(mail_conn, 'expediteur@example.com');
    utl_smtp.rcpt(mail_conn, 'destinataire@example.com');
    
    -- Écrire le message
    utl_smtp.open_data(mail_conn);
    utl_smtp.write_data(mail_conn, 'Subject: Nouvelle insertion dans ma_table');
    utl_smtp.write_data(mail_conn, 'From: expediteur@example.com');
    utl_smtp.write_data(mail_conn, 'To: destinataire@example.com');
    utl_smtp.write_data(mail_conn, ' ');
    utl_smtp.write_data(mail_conn, 'Une nouvelle ligne a été insérée dans ma_table.');
    utl_smtp.close_data(mail_conn);
    
    -- Fermer la connexion SMTP
    utl_smtp.quit(mail_conn);
EXCEPTION
    WHEN OTHERS THEN
        -- Gérer les erreurs
        NULL;
END;
/
