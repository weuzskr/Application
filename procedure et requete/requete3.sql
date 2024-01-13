CREATE TABLE backup_errors (
    error_id NUMBER PRIMARY KEY,
    error_message VARCHAR2(500),
    backup_time TIMESTAMP
);
