import asyncpg

connect = asyncpg.connect
create_pool = asyncpg.create_pool
connection = asyncpg.connection
pool = asyncpg.pool

ConnectionAsyncpg = connection.Connection
PoolAsyncpg = pool.Pool
Record = asyncpg.Record
