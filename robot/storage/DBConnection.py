from psycopg2 import connect
from psycopg2 import DatabaseError

from decouple import config

from typing import Tuple
from typing import Any


class Connection:
    """
    Database connetion object.
    Initializes the conection to postgresql database
    """

    def __init__(self, host: str, database: str, user: str, password: str) -> None:
        """
        Parameters
        ----------
        host: str -- Database host.

        datanse: str -- Name of database to use, for example postgreSQL.

        user: str -- Database username. username can be superuser.

        password: str -- Password to access database.

        Return
        ------
        None -- Nothing is returned
        """

        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def _connect(self) -> None:
        """
        NOTE: private method.
        Makes a connection to the postgreSQL database.

        Returns
        ------
        None -- Nothing is returned.
        """

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
        """
        Create data in database.

        Parameter
        ---------
        statement: str -- The 'CREATE' command to execute

        Return
        ------
        bool -- Return 'True' if successful or 'False' if not sucessful.
        """

        # Call method to connect to database
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

    def read(self, statement: str) -> Tuple[bool, Any]:
        """
        Read database data

        Parameter
        ---------
        statemtemt: str -- The 'READ' command to execute

        Return
        ------
        Tuple[bool, Any] -- Return 'True' and 'cursor' object if successful or 'False' and 'None' if not sucessful.
        """

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

        return False, None

    def update(self, statement: str) -> bool:
        """
        Update databse data.

        Parameter
        ---------
        statemtemt: str -- The 'UPDATE' command to execute

        Return
        ------
        bool -- Return 'True' if successful or 'False' if not sucessful.
        """
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
