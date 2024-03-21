CREATE TABLE login_failure_log (
    log_id NUMBER GENERATED ALWAYS AS IDENTITY,
    username VARCHAR2(50),
    ip_address VARCHAR2(50),
    attempt_timestamp TIMESTAMP,
    CONSTRAINT login_failure_log_pk PRIMARY KEY (log_id)
);

/* Informations sur les tablespaces */

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
WHERE t1.tablespace_name = t2.tablespace_name;


/* Espaces des fichiers journales : */

SELECT
    GROUP# AS "Group Number",
    THREAD# AS "Thread Number",
    SEQUENCE# AS "Sequence Number",
    BYTES AS "Bytes",
    BLOCKSIZE AS "Blocks",
    FIRST_CHANGE# AS "First Change#",
    NEXT_CHANGE# AS "Next Change#",
    FIRST_TIME AS "First Time",
    NEXT_TIME AS "Next Time",
    STATUS AS "Status"
FROM
    V$LOG
ORDER BY
    THREAD#,
    SEQUENCE#;
