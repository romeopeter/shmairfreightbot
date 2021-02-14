from psycopg2 import connect
from psycopg2 import DatabaseError

from decouple import config


class Connection:
    """
    Database connetion object.
    Initializes the conection to postgresql database
    """

    def __init__(self, host: str, database: str, user: str, password: str) -> None:
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

    def create(self, statement: str) -> bool:
        """Create data in database"""

        conn = self._connect()

        if conn is not None:
            try:
                # Create cursor
                cursor = conn.cursor()

                # Execute SQL statements
                print("PostgreSQL database version:")
                cursor.execute(statement)

                return True
            except Exception as error:
                print(error)
            finally:
                # Committing tell the driver to send the command to the database
                conn.close()

        return False

    def read(self, statement: str):
        """Read database data"""

        conn = self._connect()

        # Check if connection object is returned
        if conn is not None:

            try:
                # Create cursor
                cursor = conn.cursor()

                # Execute SQL statements
                print("PostgreSQL database version:")
                cursor.execute(statement)

                # display the PostgreSQL database server version
                DB_version = cursor.fetchone()

                print(DB_version)

                # Return 'True' for succes and cursor object for further processing
                return True, cursor
            except Exception as error:
                print(error)
            finally:
                # Close communication with postgre server
                conn.close()

        return False

    def update(self, statement: str) -> bool:
        """Update databse data"""
        conn = self._connect()

        if conn is not None:
            try:
                # Create cursor
                cursor = conn.cursor()

                # Execute SQL statements
                cursor.execute(statement)
                cursor.commit()

                print("Total updated row:", cursor.rowcount)
                return True
            except Exception as error:
                print(error)
            finally:
                print("Database updated successfully")
                conn.close()
        return False


if __name__ == "__main__":
    connect_db = Connection(
        host=config("HOST", cast=str),
        database=config("DATABASE", cast=str),
        user=config("USER", cast=str),
        password=config("PASSWORD", cast=str),
    )

    connect_db.execute_stmt("SELECT  version()")
