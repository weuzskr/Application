CREATE TABLE login_failure_log (
    log_id NUMBER GENERATED ALWAYS AS IDENTITY,
    username VARCHAR2(50),
    ip_address VARCHAR2(50),
    attempt_timestamp TIMESTAMP,
    CONSTRAINT login_failure_log_pk PRIMARY KEY (log_id)
);
