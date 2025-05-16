"""
Main application to demonstrate CRUD operations for the ERD-based system.
Edit the connection string for your MS SQL Server.
"""
from models import Base, Client, Worker, Specialities, Location, Task, SubTask, Request, AvailableSlot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Edit this connection string for your MS SQL Server
# Example: 'mssql+pyodbc://username:password@dsn_name'
engine = create_engine('sqlite:///test.db')  # For demo/testing, uses SQLite
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables (run once)
Base.metadata.create_all(engine)

def create_sample_data():
    # Create a client
    client = Client(name='John Doe', phone='123456789', address='123 Main St', payment_info='VISA')
    session.add(client)
    # Create a worker
    worker = Worker(name='Alice')
    session.add(worker)
    # Create a speciality
    speciality = Specialities(speciality_name='Plumbing')
    session.add(speciality)
    # Create a location
    location = Location(location_name='Downtown')
    session.add(location)
    # Create a slot
    slot = AvailableSlot(start_time='09:00', end_time='12:00')
    session.add(slot)
    # Create a task
    task = Task(task_name='Fix Sink', avg_fee=50.0, avg_time_to_finish=2.0)
    session.add(task)
    # Create a subtask
    subtask = SubTask(name='Turn off water', status='Pending', task=task)
    session.add(subtask)
    # Create a request
    request = Request(request_address='123 Main St', client=client, slot=slot)
    request.tasks.append(task)
    session.add(request)
    # Set relationships
    worker.specialities.append(speciality)
    worker.locations.append(location)
    worker.slots.append(slot)
    client.locations.append(location)
    task.specialities.append(speciality)
    session.commit()
    print('Sample data created.')

def list_clients():
    print('Clients:')
    for client in session.query(Client).all():
        print(f'- {client.client_id}: {client.name}, {client.phone}, {client.address}')

def update_client(client_id, new_name):
    client = session.query(Client).filter_by(client_id=client_id).first()
    if client:
        client.name = new_name
        session.commit()
        print(f'Client {client_id} updated.')
    else:
        print('Client not found.')

def delete_client(client_id):
    client = session.query(Client).filter_by(client_id=client_id).first()
    if client:
        session.delete(client)
        session.commit()
        print(f'Client {client_id} deleted.')
    else:
        print('Client not found.')

if __name__ == '__main__':
    create_sample_data()
    list_clients()
    update_client(1, 'Jane Doe')
    list_clients()
    delete_client(1)
    list_clients()
