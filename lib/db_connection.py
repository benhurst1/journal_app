import psycopg2


class DatabaseConnection:
    DATABASE_NAME = "journal_app"

    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        try:
            return psycopg2.connect(
                f"postgresql://localhost/journal_app"
            )
        except psycopg2.OperationalError:
            raise Exception(f"Could not connect to {self.DATABASE_NAME}")

    def execute(self, query, params):
        with self.connection.cursor() as cur:
            cur.execute(query, params)
            self.connection.commit()
