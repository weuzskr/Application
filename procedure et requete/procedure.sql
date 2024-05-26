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
/
CREATE OR REPLACE PROCEDURE get_login_errors IS
BEGIN
    FOR login_error IN (
        SELECT username, timestamp, action_name, returncode
        FROM dba_audit_session
        WHERE action_name = 'LOGON' AND returncode != 0
    )
    LOOP
        DBMS_OUTPUT.PUT_LINE('Utilisateur: ' || login_error.username || ', Heure: ' || login_error.timestamp || ', Code de retour: ' || login_error.returncode);
    END LOOP;
END;
/
