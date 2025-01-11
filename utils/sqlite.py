import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(loger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        
        
        CREATE TABLE users (
        id INT NOT NULL,
        name VARCHAR (255),
        is_sub BOOL DEFAULT False,
        lang VARCHAR (5),
        sub_expiration VARCHAR,
        PRIMARY KEY (id)


        );
        """
        self.execute(sql, commit=True)

    def add_new_user(self, id, name, ):
        sql = """
        INSERT INTO users (id, name) VALUES (?, ?) 
        """
        self.execute(sql, parameters=(id, name,), commit=True)

    def user_exist(self, id):
        sql = "SELECT * FROM users WHERE id=?"
        return self.execute(sql, parameters=(id,), fetchall=True)

    def insert_lang(self, id, lang):
        if lang == "uz":
            sql = "UPDATE users SET lang='uz' WHERE id=?"
        else:
            sql = "UPDATE users SET lang='ru' WHERE id=?"
        self.execute(sql, parameters=(id,), commit=True)

    def get_user_lang(self, id):
        sql = "SELECT lang FROM users WHERE id=?"
        return self.execute(sql, parameters=(id,), fetchone=True)

    def get_user_name(self, id):
        sql = "SELECT name FROM users WHERE id=?"
        return self.execute(sql, parameters=(id,), fetchone=True)

    def update_user_name(self, name, id):
        sql = "UPDATE users SET name=? WHERE id=?"
        self.execute(sql, parameters=(name, id,), commit=True)


def loger(statement):
    print(f"""
---------------------------------------------
Ececuting:
{statement}
---------------------------------------------
""")


