import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import contextlib
from core import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataBase:
    _pool = None

    def __init__(self):
        self._initialize_pool()

    def _initialize_pool(self):
        if DataBase._pool is None:
            try:
                DataBase._pool = psycopg2.pool.ThreadedConnectionPool(
                    1, 20,
                    host=settings.DB_HOST,
                    database=settings.DB_NAME,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    port=settings.DB_PORT
                )
                logger.info("Database connection pool initialized.")
            except Exception as e:
                logger.error(f"Error initializing connection pool: {e}")
                raise

    def get_conn(self):
        return DataBase._pool.getconn()

    def put_conn(self, conn):
        DataBase._pool.putconn(conn)

    @contextlib.contextmanager
    def transaction(self):
        conn = self.get_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                yield cursor
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Error in transaction, rolling back: {e}")
            raise
        finally:
            self.put_conn(conn)

    def execute(self, sql, params=None, many=True):
        conn = self.get_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql, params)
                if cursor.description:
                    result = cursor.fetchall() if many else cursor.fetchone()
                else:
                    result = None
                return result
        except Exception as e:
            logger.error(f"Error executing SELECT: {e}")
            raise
        finally:
            self.put_conn(conn)

    def commit(self, sql, params=None):
        conn = self.get_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchone() if cursor.description else None
                conn.commit()
                return result
        except Exception as e:
            conn.rollback()
            logger.error(f"Error executing COMMIT: {e}")
            raise
        finally:
            self.put_conn(conn)

    def execute_non_query(self, query, params=None):
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                affected = cursor.rowcount
                return affected
        except Exception as e:
            conn.rollback()
            logger.error(f"Error executing NON-QUERY: {e}")
            raise
        finally:
            self.put_conn(conn)

    def commit_many(self, sql, parameters):
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.executemany(sql, parameters)
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            conn.rollback()
            logger.error(f"Error executing COMMIT MANY: {e}")
            raise
        finally:
            self.put_conn(conn)