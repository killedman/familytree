import pymysql.cursors


class DbUtils:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def db_connect(self):
        connect = pymysql.connect(host=self.host,
                                  user=self.user,
                                  password=self.password,
                                  db=self.db,
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
        return connect

    def insert_data(self, table_name, data):
        conn = self.db_connect()
        try:
            with conn.cursor() as cursor:
                table_keys = ', '.join(list(data.keys()))
                # 值需要用单引号括起来
                table_values = ', '.join(
                    "'" + v + "'" for v in list(data.values()))
                sql = "INSERT INTO {0} ({1}) VALUES ({2})".format(
                    table_name, table_keys, table_values)
                # 这里需要添加单引号
                user_name = list(data.values())[0]
                id = self.search_data(table_name, user_name)
                if not id:
                    cursor.execute(sql)
                    conn.commit()
                else:
                    print("{0}已经添加过，id={1},不需要重复添加!".format(
                        user_name, id))
        finally:
            conn.close()

    def search_all_data(self, table_name):
        conn = self.db_connect()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM {0};".format(table_name)
                cursor.execute(sql)
                result = cursor.fetchall()
            return result
        finally:
            conn.close()

    def search_data(self, table_name, user_name):
        user_name = "'" + user_name + "'"
        conn = self.db_connect()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM {0} WHERE name={1};".format(
                    table_name, user_name
                )
                cursor.execute(sql)
                result = cursor.fetchall()
            return result
        finally:
            conn.close()

    def delete_data(self, table_name,  user_name):
        user_name = "'" + user_name + "'"
        conn = self.db_connect()
        try:
            with conn.cursor() as cursor:
                sql = "delete from {0} where name={1}".format(table_name,
                                                            user_name)
                print(sql)
                cursor.execute(sql)
                conn.commit()
        finally:
            conn.close()

    def delete(self, table_name,  user_id):
        user_id = "'" + user_id + "'"
        conn = self.db_connect()
        try:
            with conn.cursor() as cursor:
                sql = "delete from {0} where id={1}".format(table_name,
                                                            user_id)
                print(sql)
                cursor.execute(sql)
                conn.commit()
        finally:
            conn.close()


    def update_data(self, table_name, column_key, new_value, user_name):
        new_value = "'" + new_value + "'"
        user_name = "'" + user_name + "'"
        conn = self.db_connect()
        try:
            with conn.cursor() as cursor:
                sql = "update {0} set {1} = {2} where name = {3}".format(
                    table_name, column_key, new_value, user_name)
                cursor.execute(sql)
                conn.commit()
        finally:
            conn.close()
