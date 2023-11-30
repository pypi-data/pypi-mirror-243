import cx_Oracle

class Config:
    def __init__(self, dsn,host,user,password):

        # Establish a connection
        self.connection = cx_Oracle.connect(
            user=user,
            password=password,
            dsn=dsn
        )
        self.cursor = self.connection.cursor()

    
    def fetchall(self, query):
        self.cursor.execute(query)
        data = list(self.cursor)
        if self.connection:
            self.connection.close()
            self.cursor.close()

        return data

  