from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Unicode, Integer, TIMESTAMP, String
from sqlalchemy.orm import relationship, backref, validates, synonym
import sqlalchemy

Base = declarative_base()


class Agency(Base):

    __tablename__ = "agency"
    __plural_name__ = "agencies"

    id = Column(Integer, primary_key=True)
    agency_id = Column(Integer, index=True)
    agency_name = Column(Unicode(255))
    agency_url = Column(Unicode(255))
    agency_timezone = Column(String(50))


class Route(Base):

    __tablename__ = "route"
    __plural_name__ = "routes"

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, index=True)
    agency_id = Column(Integer)
    route_short_name = Column(Unicode(150), index=True)
    route_long_name = Column(Unicode(255), index=True)
    route_type = Column(Integer)


class StopTime(Base):

    __tablename__ = "stop_time"
    __plural_name__ = "stop_times"

    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, index=True)
    arrival_time = Column(String(8))
    departure_time = Column(String(8))
    stop_id = Column(Integer)
    stop_sequence = Column(Integer)
    pickup_type = Column(Integer)


class Stop(Base):

    __tablename__ = "stop"
    __plural_name__ = "stops"

    id = Column(Integer, primary_key=True)
    stop_id = Column(Integer, index=True)
    stop_name = Column(Unicode(255), index=True)
    stop_desc = Column(Unicode(255))
    stop_lat = Column(String(50))
    stop_lon = Column(String(50))


class Trip(Base):

    __tablename__ = "trip"
    __plural_name__ = "trips"

    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, index=True)
    route_id = Column(Integer)
    service_id = Column(Integer)
    trip_headsign = Column(String(255), index=True)
    direction_id = Column(Integer)
    block_id = Column(Integer)


def init(db_uri, echo=False):
    print(db_uri)
    db_engine = sqlalchemy.create_engine(db_uri, echo=echo)
    Base.metadata.create_all(db_engine)
    SessionMaker = sqlalchemy.orm.sessionmaker(bind=db_engine)
    return SessionMaker


if __name__ == "__main__":
    init('sqlite:///data/app.sqlite')
