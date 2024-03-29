import unittest
import psycopg2

from dbprime import MockPostgresRecord


class TestPostgres(unittest.TestCase):
    def setUp(self):
        self.dbargs = {
            "user": "postgres",
            "password": "",
            "database": "postgres",
            "host": "localhost",
        }
        self.dbcon = psycopg2.connect(**self.dbargs)
        self.dbcur = self.dbcon.cursor()

    def tearDown(self):
        self.dbcon.close()

    def test_postgres_insert(self):
        test_obj = MockPostgresRecord(
            psycopg2,
            self.dbargs,
            table_name="test_table",
            primary_key_column="test_tableid",
            num_val=123,
        )
        self.dbcur.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM test_table
                WHERE test_tableid = {}
            );
            """.format(
                test_obj.test_tableid
            )
        )

        record_exists = self.dbcur.fetchone()[0]
        self.assertTrue(record_exists)

    def test_postgres_update(self):
        test_obj = MockPostgresRecord(
            psycopg2,
            self.dbargs,
            table_name="test_table",
            primary_key_column="test_tableid",
            num_val=123,
        )

        self.dbcur.execute(
            """
            UPDATE test_table SET num_val = 456 WHERE test_tableid = {};
            """.format(
                test_obj.test_tableid
            )
        )

        self.dbcur.execute(
            """
            SELECT num_val = 456 FROM test_table WHERE test_tableid = {};
            """.format(
                test_obj.test_tableid
            )
        )

        self.dbcon.commit()
        update_succeeded = self.dbcur.fetchone()[0]
        self.assertTrue(update_succeeded)

    def test_postgres_delete(self):
        test_obj = MockPostgresRecord(
            psycopg2,
            self.dbargs,
            table_name="test_table",
            primary_key_column="test_tableid",
            num_val=123,
        )
        test_tableid = test_obj.test_tableid
        del test_obj

        self.dbcur.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM test_table
                WHERE test_tableid = {}
            );
            """.format(
                test_tableid
            )
        )

        record_exists = self.dbcur.fetchone()[0]
        self.assertFalse(record_exists)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
