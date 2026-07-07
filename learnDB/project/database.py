from sqlalchemy import (
    create_engine, #is create_engine a class? NO, it's a function, that returns an engine object.   
    MetaData, 
    Table, 
    Column, 
    Integer,
    String,
    select, 
    insert )

#environment variables, to stores sensitive information like DATABASE_URL, passwords, etc.

#learn about, do all variables come from python's process variable. like do the windows env variables get into python's process variables or what?

from dotenv import load_dotenv, dotenv_values
import os
from pathlib import Path

# env_path = Path("project")/ "information.env"

# loaded = load_dotenv(env_path)

# DEBUGGING.
# print(env_path)
# print(env_pa  th.resolve())
# print(env_path.exists())
# print(os.getenv("hello"))

# print(dotenv_values(env_path))
# print(repr(open(env_path).read()))

# loaded = load_dotenv('project/information.env')

# print(loaded)

# print(os.getenv("DATABASE_URL"))

##Now starting to write actual codes.

#load the .env file so you can access the database url information.
load_dotenv('project/information.env')

#get database url from .env file (in this case, information.env file)
db_url = os.getenv("DATABASE_URL")

if db_url is None:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set."   
    )

engine= create_engine(
    db_url, 
    echo= True  #this tells SQLAlchemy, print ALL the SQL statements you execute.
)
#create_engine is a factory function.
#Factory functions : Functions which create and configure objects for you.

"""
Internally, create_engine():
Parses the URL.
Chooses the correct Dialect.
Loads the correct Driver.
Creates a Connection Pool.
Creates the Engine.
Then returns one fully configured Engine object."""

metadata = MetaData()

users = Table(
    "users",
    metadata,

    Column(
        "id",
        Integer,
        primary_key=True,
    ),

    Column(
        "name",
        String(100),
        nullable=False,
    ),

    Column(
        "email",
        String(255),
        unique=True,
        nullable=False,
    ),
)

metadata.create_all(engine)