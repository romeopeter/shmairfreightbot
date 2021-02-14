from psycopg2 import connect
from psycopg2 import DatabaseError

from decouple import config


class Connection:
    """
    Database connetion object.
    Initializes the conection to postgresql database
    """

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def _connect(self):
        """Connect to postgre sql database"""

        conn = None

        for attempt in range(0, 10):
            try:
                # Connect to postgreSQL server
                print("Connecting to postgresql server")
                conn = connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                )

                # Connection successful. break loop
                break
            except (Exception, DatabaseError) as error:
                print(f"Attempt: {attempt}, got error: {error}")

                # Connection not successful. Continue loop
                continue

        # Return the 'connection' object
        return conn

    def execute_stmt(self, statement: str):
        """Execute SQL statements"""

        conn = self._connect()

        # Check if connection object is returned
        if conn is not None:

            # Create cursor
            cursor = conn.cursor()

            # Execute statement
            print("PostgreSQL database version:")
            cursor.execute(statement)

            # display the PostgreSQL database server version
            DB_version = cursor.fetchone()

            print(DB_version)

            # Close communication with postgre server
            cursor.close()
            conn.close()

            return True, cursor

        return False


if __name__ == "__main__":
    connect_db = Connection(
        host=config("HOST", cast=str),
        database=config("DATABASE", cast=str),
        user=config("USER", cast=str),
        password=config("PASSWORD", cast=str),
    )

    connect_db.execute_stmt("SELECT  version()")
