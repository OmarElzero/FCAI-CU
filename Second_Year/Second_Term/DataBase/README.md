# Software Application for ERD-based System

## Requirements
- Python 3.x
- SQLAlchemy
- pyodbc (for MS SQL Server)

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Edit the connection string in `app.py` and `models.py` to match your MS SQL Server setup.
   - Example: `mssql+pyodbc://username:password@dsn_name`
   - For demo/testing, SQLite is used by default.
3. Run the application:
   ```bash
   python app.py
   ```

## Files
- `models.py`: SQLAlchemy models for all entities and relationships.
- `app.py`: Main application with CRUD operations and sample data.
- `requirements.txt`: Python dependencies.

## Notes
- The code demonstrates basic CRUD for the `Client` entity. You can extend it for other entities similarly.
- For production, use MS SQL Server and update the connection string accordingly.
