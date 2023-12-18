CREATE TABLE connection_log (
    log_id NUMBER PRIMARY KEY,
    username VARCHAR2(50),
    login_time TIMESTAMP,
    status VARCHAR2(10)
);
