from dotenv import load_dotenv
import os
import json
from sqlalchemy import Column, String, Integer, Numeric, text, func, create_engine
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

Base = declarative_base()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASS")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")

engine = create_engine(
    "mysql://{}:{}@{}/{}".format(MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_DB))


class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    rco2_units = Column('rco2_units', String(16))
    rco2_span = Column('rco2_span', Integer)
    rco2_value = Column('rco2_value', Numeric)
    rco2_timestamp = Column('rco2_timestamp', TIMESTAMP)
    rhumid_units = Column('rhumid_units', String(16))
    rhumid_span = Column('rhumid_span', Integer)
    rhumid_value = Column('rhumid_value', Numeric)
    rhumid_timestamp = Column('rhumid_timestamp', TIMESTAMP)
    rpm10c_units = Column('rpm10c_units', String(16))
    rpm10c_span = Column('rpm10c_span', Integer)
    rpm10c_value = Column('rpm10c_value', Numeric)
    rpm10c_timestamp = Column('rpm10c_timestamp', TIMESTAMP)
    rpm25c_units = Column('rpm25c_units', String(16))
    rpm25c_span = Column('rpm25c_span', Integer)
    rpm25c_value = Column('rpm25c_value', Numeric)
    rpm25c_timestamp = Column('rpm25c_timestamp', TIMESTAMP)
    rtemp_units = Column('rtemp_units', String(16))
    rtemp_span = Column('rtemp_span', Integer)
    rtemp_value = Column('rtemp_value', Numeric)
    rtemp_timestamp = Column('rtemp_timestamp', TIMESTAMP)
    created_time = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_time = Column(TIMESTAMP, nullable=False, server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


print('Running transform')

Base.metadata.create_all(engine, tables=[Log.__table__])

log = Log()

with open('./data/extract/devices.json') as json_file:
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()

    data = json.load(json_file)
    for p in data['data']:
        if p['param'] == 'rc02':
            log.rco2_units = p['units']
            log.rco2_span = p['span']
            log.rco2_value = p['points'][0]['value']
            log.rco2_timestamp = p['points'][0]['ts']
        elif p['param'] == 'rhumid':
            log.rhumid_units = p['units']
            log.rhumid_span = p['span']
            log.rhumid_value = p['points'][0]['value']
            log.rhumid_timestamp = p['points'][0]['ts']
        elif p['param'] == 'rpm10c':
            log.rpm10c_units = p['units']
            log.rpm10c_span = p['span']
            log.rpm10c_value = p['points'][0]['value']
            log.rpm10c_timestamp = p['points'][0]['ts']
        elif p['param'] == 'rpm25c':
            log.rpm25c_units = p['units']
            log.rpm25c_span = p['span']
            log.rpm25c_value = p['points'][0]['value']
            log.rpm25c_timestamp = p['points'][0]['ts']
        elif p['param'] == 'rtemp':
            log.rtemp_units = p['units']
            log.rtemp_span = p['span']
            log.rtemp_value = p['points'][0]['value']
            log.rtemp_timestamp = p['points'][0]['ts']
    session.add(log)
    session.commit()
    session.close()
