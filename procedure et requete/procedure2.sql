CREATE OR REPLACE TRIGGER connection_audit_trigger
AFTER LOGON ON DATABASE
DECLARE
    v_status VARCHAR2(10);
BEGIN
    -- Vérifier si la connexion est réussie ou échouée
    IF SYS_CONTEXT('USERENV', 'SESSION_USER') IS NOT NULL THEN
        v_status := 'SUCCESS';
    ELSE
        v_status := 'FAILURE';
    END IF;

    -- Enregistrer les informations de connexion dans la table de journalisation
    INSERT INTO connection_log (log_id, username, login_time, status)
    VALUES (connection_log_seq.nextval, USER, SYSTIMESTAMP, v_status);
END;
/
CREATE OR REPLACE TRIGGER logon_trigger
AFTER LOGON ON DATABASE
BEGIN
    DBMS_OUTPUT.PUT_LINE('Bonjour');
END;
/
