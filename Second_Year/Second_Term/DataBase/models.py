"""
SQLAlchemy models for the ERD-based system.
Edit the connection string as needed for your MS SQL Server.
"""

from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Float, Table, DateTime
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

# Association tables for many-to-many relationships
client_location = Table(
    'client_location', Base.metadata,
    Column('client_id', Integer, ForeignKey('client.client_id')),
    Column('location_id', Integer, ForeignKey('location.location_id'))
)

worker_speciality = Table(
    'worker_speciality', Base.metadata,
    Column('worker_id', Integer, ForeignKey('worker.worker_id')),
    Column('speciality_id', Integer, ForeignKey('specialities.speciality_id'))
)

worker_location = Table(
    'worker_location', Base.metadata,
    Column('worker_id', Integer, ForeignKey('worker.worker_id')),
    Column('location_id', Integer, ForeignKey('location.location_id'))
)

worker_slot = Table(
    'worker_slot', Base.metadata,
    Column('worker_id', Integer, ForeignKey('worker.worker_id')),
    Column('slot_id', Integer, ForeignKey('availableslot.slot_id'))
)

task_speciality = Table(
    'task_speciality', Base.metadata,
    Column('task_id', Integer, ForeignKey('task.task_id')),
    Column('speciality_id', Integer, ForeignKey('specialities.speciality_id'))
)

request_task = Table(
    'request_task', Base.metadata,
    Column('request_id', Integer, ForeignKey('request.request_id')),
    Column('task_id', Integer, ForeignKey('task.task_id'))
)

class Client(Base):
    __tablename__ = 'client'
    client_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    address = Column(String)
    payment_info = Column(String)
    requests = relationship('Request', back_populates='client')
    locations = relationship('Location', secondary=client_location, back_populates='clients')

class Worker(Base):
    __tablename__ = 'worker'
    worker_id = Column(Integer, primary_key=True)
    name = Column(String)
    specialities = relationship('Specialities', secondary=worker_speciality, back_populates='workers')
    locations = relationship('Location', secondary=worker_location, back_populates='workers')
    slots = relationship('AvailableSlot', secondary=worker_slot, back_populates='workers')

class AvailableSlot(Base):
    __tablename__ = 'availableslot'
    slot_id = Column(Integer, primary_key=True)
    start_time = Column(String)  # Use DateTime if you want
    end_time = Column(String)
    workers = relationship('Worker', secondary=worker_slot, back_populates='slots')
    requests = relationship('Request', back_populates='slot')

class Specialities(Base):
    __tablename__ = 'specialities'
    speciality_id = Column(Integer, primary_key=True)
    speciality_name = Column(String)
    workers = relationship('Worker', secondary=worker_speciality, back_populates='specialities')
    tasks = relationship('Task', secondary=task_speciality, back_populates='specialities')

class Location(Base):
    __tablename__ = 'location'
    location_id = Column(Integer, primary_key=True)
    location_name = Column(String)
    workers = relationship('Worker', secondary=worker_location, back_populates='locations')
    clients = relationship('Client', secondary=client_location, back_populates='locations')

class Task(Base):
    __tablename__ = 'task'
    task_id = Column(Integer, primary_key=True)
    task_name = Column(String)
    avg_fee = Column(Float)
    avg_time_to_finish = Column(Float)
    specialities = relationship('Specialities', secondary=task_speciality, back_populates='tasks')
    requests = relationship('Request', secondary=request_task, back_populates='tasks')
    subtasks = relationship('SubTask', back_populates='task')

class SubTask(Base):
    __tablename__ = 'subtask'
    name = Column(String, primary_key=True)
    status = Column(String)
    task_id = Column(Integer, ForeignKey('task.task_id'))
    task = relationship('Task', back_populates='subtasks')

class Request(Base):
    __tablename__ = 'request'
    request_id = Column(Integer, primary_key=True)
    request_address = Column(String)
    client_id = Column(Integer, ForeignKey('client.client_id'))
    slot_id = Column(Integer, ForeignKey('availableslot.slot_id'))
    client = relationship('Client', back_populates='requests')
    slot = relationship('AvailableSlot', back_populates='requests')
    tasks = relationship('Task', secondary=request_task, back_populates='requests')

# Example engine (edit for your MS SQL Server)
# engine = create_engine('mssql+pyodbc://username:password@dsn_name')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
