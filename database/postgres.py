import logging
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

logger = logging.getLogger(__name__)


class Database:

    def __init__(self, config):
        self.pool: Union[Pool, None] = None
        self._db_user = config.user
        self._db_password = config.password
        self._db_host = config.host
        self._db_database = config.database
        self._db_port = config.port


    async def execute(self, command, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False,
                      execute: bool = False):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(user=self._db_user,
                                                  password=self._db_password,
                                                  host=self._db_host,
                                                  database=self._db_database,
                                                  port=self._db_port
                                                  )
            logger.info(f'Создано подключение к БД')
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_tables(self):
        sql = "CREATE TABLE IF NOT EXISTS payments (" \
              "payment_id INTEGER NOT NULL UNIQUE," \
              "date_time VARCHAR(19) NOT NULL," \
              "order_id INTEGER NOT NULL," \
              "customer_id INTEGER NOT NULL," \
              "customer_name VARCHAR(100) NOT NULL," \
              "payment_method_id INTEGER NOT NULL," \
              "payment_method_name VARCHAR(255) NOT NULL," \
              "amount NUMERIC(8, 2) NOT NULL);"
        return await self.execute(sql, execute=True)

    async def add_payment(self, payment_id, date_time, order_id, customer_id, customer_name, payment_method_id,
                          payment_method_name, amount):
        sql = "INSERT INTO payments " \
              "(payment_id, date_time, order_id, customer_id," \
              " customer_name, payment_method_id, payment_method_name, amount)" \
              " VALUES ($1, $2, $3, $4, $5, $6, $7, $8)"
        return await self.execute(sql, payment_id, date_time, order_id, customer_id, customer_name, payment_method_id,
                                  payment_method_name, amount, execute=True)

    async def select_payment(self, payment_id):
        sql = "SELECT payment_id FROM payments WHERE payment_id = $1"
        return await self.execute(sql, payment_id, fetchval=True)
