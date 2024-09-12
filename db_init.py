from sqlalchemy import create_engine, Column, Integer, Text, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

# Create SQL engine and session
engine = create_engine('sqlite:///db/flightstats.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

# Define the Flight model for the database
class Flight(Base):
    __tablename__ = 'FLIGHTS'
    id = Column(Integer, primary_key=True)
    airline_code = Column(Text, nullable=False)
    airline_number = Column(Integer, nullable=False)
    departure_date = Column(Text, nullable=False)
    flight_data = Column(JSON, nullable=False)

# Create the tables in the database
Base.metadata.create_all(engine)
