CREATE OR REPLACE PROCEDURE log_backup_error(p_error_message IN VARCHAR2) AS
BEGIN
    INSERT INTO backup_errors (error_id, error_message, backup_time)
    VALUES (error_id_sequence.NEXTVAL, p_error_message, SYSTIMESTAMP);
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        -- Gérer les erreurs lors de l'enregistrement de l'erreur
        -- Vous pouvez ajouter des actions de journalisation supplémentaires ici si nécessaire
        DBMS_OUTPUT.PUT_LINE('Erreur lors de l'enregistrement de l\'erreur : ' || SQLERRM);
        ROLLBACK; -- Rollback pour éviter de compromettre la transaction actuelle
END log_backup_error;
/
CREATE OR REPLACE PROCEDURE monitor_logs IS
BEGIN
    FOR log_info IN (SELECT group#, thread#, member FROM v$log)
    LOOP
        DBMS_OUTPUT.PUT_LINE('Log Group: ' || log_info.group# || ', Thread: ' || log_info.thread# || ', Member: ' || log_info.member);
    END LOOP;
END;
/

