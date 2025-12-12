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

---

# ERDApp

This project supports both:
- **Console testing on Linux (with SQLite, no GUI)**
- **Full Windows GUI (WinForms, with SQL Server)**

---

## Console Test (Linux, SQLite)

1. **Install .NET SDK:**
   - [Official Microsoft instructions](https://learn.microsoft.com/en-us/dotnet/core/install/linux)
   - Or on Ubuntu:
     ```bash
     sudo apt-get update
     sudo apt-get install -y dotnet-sdk-6.0
     ```

2. **Run the console test:**
   ```bash
   dotnet new console -n TestApp
   mv FakeDatabaseTest.cs TestApp/Program.cs
   cd TestApp
   dotnet add package System.Data.SQLite
   dotnet run
   ```
   - This will show add, update, and delete operations for the `Client` entity using an in-memory SQLite database.

---

## Windows GUI (WinForms, SQL Server)

1. **Open the solution in Visual Studio on Windows.**
2. **Ensure these files are included:**
   - `MainForm.cs`
   - `MainForm.Designer.cs`
   - `Database.cs`
   - `Program.cs`
3. **Update the connection string in `Database.cs`** to point to your SQL Server instance.
4. **Build and run the project.**
   - The GUI will appear for managing clients.

---

## Files
- `models.py`: SQLAlchemy models for all entities and relationships.
- `app.py`: Main application with CRUD operations and sample data.
- `requirements.txt`: Python dependencies.
- `FakeDatabaseTest.cs` — Console test for Linux (SQLite, no GUI)
- `MainForm.cs`, `MainForm.Designer.cs`, `Database.cs`, `Program.cs` — Windows GUI (WinForms, SQL Server)

---

## Collaboration
- Linux users: Use the console test to validate logic.
- Windows users: Use the GUI for full functionality.

---

## Notes
- The code demonstrates basic CRUD for the `Client` entity. You can extend it for other entities similarly.
- For production, use MS SQL Server and update the connection string accordingly.
- **For any issues, make sure the .NET SDK is installed and the connection string is correct for your environment.**
