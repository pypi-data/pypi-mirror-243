import cx_Oracle

class Config:
    def __init__(self, dsn,user,password):

        # Establish a connection
        self.connection = cx_Oracle.connect(
            user=user,
            password=password,
            dsn=dsn
        )
        self.cursor = self.connection.cursor()

    def fetchall(self, query):
        try:
            self.cursor.execute(query)
            data = list(self.cursor)
            return data
        except Exception as error:
            print("Oracle Error:", error)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
  