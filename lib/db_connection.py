import psycopg2


class DatabaseConnection:
    DEV_DATABASE_NAME = "journal_app"
    TEST_DATABASE_NAME = "journal_app_test"

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.connect()

    def connect(self):
        try:
            # self.connection = psycopg2.connect(
            #     f"postgresql://localhost/{self._database_name()}"
            # )
            self.connection = psycopg2.connect(
                dbname="journal_app",
                user="benhurst",
                password="",
                port=5432,
                host="localhost",
            )
            # self.connection = psycopg2.connect(
            #     f"dbname={self._database_name()} host=localhost user=postgres password=  port=5432"
            # )
        except psycopg2.OperationalError:
            raise Exception(f"Could not connect to {self._database_name()}")

    def execute(self, query, params=[]):
        with self.connection.cursor() as cur:
            cur.execute(query, params)
            if cur.description is not None:
                result = cur.fetchall()
            else:
                result = None
            self.connection.commit()
            return result

    def _database_name(self):
        if self.test_mode == True:
            return self.TEST_DATABASE_NAME
        return self.DEV_DATABASE_NAME
