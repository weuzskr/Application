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
