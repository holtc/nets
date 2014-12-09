import MySQLdb

class Database:

    def __init__(self, host, user, pwd, db_name):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db_name = db_name

    def execute(self, query):
        conn = MySQLdb.connect(self.host, self.user, self.pwd, self.db_name)
        cursor = conn.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except MySQLdb.IntegrityError, e:
            print "Error: " + str(e)
        cursor.close()
        conn.close()
        return result
