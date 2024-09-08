from db_init import Base
from sqlalchemy import Column, Integer, Text, JSON

# define the Flight model for db
class Flight(Base):
    __tablename__ = 'FLIGHTS'
    id = Column(Integer, primary_key=True)
    airline_code = Column(Text, nullable=False)
    airline_number = Column(Integer, nullable=False)
    departure_date = Column(Text, nullable=False)
    flight_data = Column(JSON, nullable=False)