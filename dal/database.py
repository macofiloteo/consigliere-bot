from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///consigliere.db")
session_maker = sessionmaker(engine)

def create_session():
    session = session_maker()
    return session


