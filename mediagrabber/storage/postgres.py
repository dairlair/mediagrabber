import numpy as np
import psycopg2
from typing import List, Optional
from psycopg2.extensions import register_adapter, AsIs
from psycopg2.extras import RealDictCursor

def addapt_numpy_array(numpy_array):
    return AsIs(list(numpy_array))

class PostgreSQLStorage():
    def __init__(self, dsn: str):
        register_adapter(np.ndarray, addapt_numpy_array)
        self.dsn = dsn
        self.conn = None

    def get_url_id(self, url: str) -> Optional[int]:
        cur = self.get_connection().cursor()
        cur.execute("SELECT id FROM urls WHERE url = %s ", (url.lower(),))
        row = cur.fetchone()
        return str(row['id']) if row else None

    def get_url_id_or_create(self, url: str) -> int:
        try:
            cur = self.get_connection().cursor()
            sql = "INSERT INTO urls (url) VALUES (%s) RETURNING id"
            cur.execute(sql, (url.lower(),))
            row = cur.fetchone()
            self.get_connection().commit()
            return row['id']
        except psycopg2.errors.UniqueViolation:
            self.get_connection().rollback()
            # We anyway will return the ID of URL
            return self.get_url_id(url)
        finally:
            cur.close()

    def get_connection(self) -> psycopg2.extensions.connection:
        if self.conn is None:
            self.conn = self.connect()

        return self.conn

    def connect(self) -> psycopg2.extensions.connection:
        return psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)