from pymysql import *
import pymysql.cursors

class Login():
    def __init__(self, parent = None):
        self.conn = pymysql.connect(
            host = 'localhost',
            user = 'dreamlocker',
            password = '123',
            db = 'DT_DB',
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor
            )

    def login(self, username, passwd):
        result = self.getPasswd(username)
        if username == "" or passwd == "":
            return "Miss"
        elif result == None:
            return "None"
        elif passwd == result.get('pwd'):
            return "Success"
        else:
            return "WrongPwd"

    def sign_up(self, username, passwd):
        if username != "" and passwd != "":
            self.insert_sql(username, passwd)
            return "Success"
        else:
            return "Miss"

    def insert_sql(self, username, passwd):
        try:
            with self.conn.cursor() as cursor:
                sql = "insert into userinfo (name, pwd) values (%s, %s)"
                cursor.execute(sql, (username, passwd))
                self.conn.commit()
        except Exception as e:
            print(e)


    def getPasswd(self, username):
        try:
            with self.conn.cursor() as cursor:
                sql = "select `pwd`, `name` from userinfo where name = %s"
                cursor.execute(sql, (username))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(e)
        # finally:
            # self.conn.close()

