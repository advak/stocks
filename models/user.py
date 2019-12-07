from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('sqlite:///data.db',  echo=True)
meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('email', String),
    Column('password', String),
    Column('first_name', String),
    Column('last_name', String),
)
meta.create_all(engine)


def insert_to_table(email, password, first_name, last_name):
    ins = users.insert().values(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name)
    conn = engine.connect()
    conn.execute(ins)
