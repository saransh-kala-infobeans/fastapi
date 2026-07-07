from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select

# #creating database URL to connect to the database.
# DATABASE_URL= "postgresql://postgres:[YOUR_PASSWORD_HERE]@db.kljwkuyifmdkmgkubezk.supabase.co:5432/postgres"

# #creating an engine object.
# engine= create_engine(DATABASE_URL) #this doesn't start any connections, only create an engine object.

#MetaData object initialization
metadata= MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("age", Integer),
    Column("email", String, unique=True)
)

accounts= Table(
    "accounts",
    metadata,
    Column("account_id", Integer, nullable=False, unique=True),
    Column("personal_id", Integer),
    Column("balance", Integer),
    Column("password", String, nullable=False)
)

#tell metadata which all tables to create.
#metadata.create_all(engine, tables=[users])

#creating a statement object, remember, this is just an object, no query from now. SQLAlchemy compiles a statement whenever compilation is needed LIKE during execution(conn.execute(stmt)), when we explicitly call stmt.compile(...), or when you print a statement (sqlalchemy complies it for display)
stmt= select(users).where(users.c.age > 18) 

# users.c.age > 18  -> this feels like this should be returning a boolean answer, just like 5 > 18 or 34 > 17 would give, but,
# users.c.age isn't an integer to compare, users.c.age is a COLUMN OBJECT.
# so what does "users.c.age > 18" do?? CREATE ANOTHER ANOTHER OBJECT.
# The EXPRESSION OBJECT.

#stmt (Statement object)--> Dialect --> Compiled Statement (SQL + Parameter bindings.)

# with engine.connect() as conn:
#     #The result object represents an ITERABLE view over the database rasult set.
#     result= conn.execute(stmt)
#     #Why doesn't sqlalchemy return a list as result of a query, why OBJECT?!
#     # STREAMING,  see, say the query is executed and it returns some 20 million rows. if you'll use list, it'll fillup your complete ram even before you'd know. Hence we use STREAMING, SQLAlchemy can fetch rows gradually (or in batches, depending on the driver and configuration).

#     for row in result:
#         print(row.name)

#print(type(stmt))

#stop
from sqlalchemy.dialects import postgresql
print(
    stmt.compile(dialect= postgresql.dialect()).params
)