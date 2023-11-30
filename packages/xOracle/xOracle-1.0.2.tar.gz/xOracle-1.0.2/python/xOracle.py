import cx_Oracle

class Config:
    def __init__(self, host,dsn,user,password):

        # Set up the connection details
        cx_Oracle.makedsn(host=host, port=dsn, service_name=dsn)

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

  