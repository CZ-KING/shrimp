DATABASE = {
    "mysql":{
        "host":"localhost",
        "port":3306,
        "username":"root",
        "password":"123456",
        "db":"shrimp"
    },
    "oracle":{
        "host":"localhost",
        "port":3306,
        "username":"chipscoco",
        "password":"tesT123.",
        "db":"chenzhan"
    },

    "elasticsearch":{
        "host":"localhost",
        "port":3306,
    },
}


class DatabaseType:
    MYSQL = 0
    ORACLE = 1
    ELASTICSEARCH = 2
