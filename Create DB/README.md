To create an SQL database and a table for storing data from sensors such as temperature and humidity, you can use the following Python program. This example utilizes SQLite, which is a lightweight database that doesn't require a separate server. If you're using another SQL database (like MySQL or PostgreSQL), the SQL commands will remain largely the same, but you'll need to modify the connection setup.

### Python Program to Create an SQL Database and Table

```python
import sqlite3

# Define the database name
db_name = 'sensor_data.db'

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_name)

# Create a cursor object
cursor = conn.cursor()

# SQL command to create a new table
create_table_query = '''
CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL
);
'''

# Execute the SQL command
cursor.execute(create_table_query)

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Database and table created successfully!")
```

### Explanation of the Code

1. **Import sqlite3**: The SQLite library is imported to manage the database operations.

2. **Database Connection**: The program connects to a database file named `sensor_data.db`. If the file does not exist, SQLite will create it.

3. **Create Cursor**: A cursor object is created, which is used to execute SQL commands.

4. **Create Table Query**: The SQL command defines a table named `sensor_readings` with the following columns:
   - `id`: An auto-incrementing primary key.
   - `timestamp`: A datetime column that defaults to the current timestamp when a record is inserted.
   - `temperature`: A column to store temperature readings (real number).
   - `humidity`: A column to store humidity readings (real number).

5. **Execute the Command**: The SQL command is executed to create the table if it doesn’t already exist.

6. **Commit Changes**: Changes are committed to the database.

7. **Close Connection**: The connection to the database is closed.

8. **Print Confirmation**: A success message is printed to indicate that the database and table have been created successfully.

### How to Run the Program

1. Ensure you have Python installed on your machine.
2. Save the code above to a file, for example, `create_sensor_db.py`.
3. Run the script using the command:
   ```bash
   python create_sensor_db.py
   ```

### Additional Considerations

- If you're using a different SQL database system (like MySQL or PostgreSQL), you will need to adjust the connection method accordingly and ensure the respective database driver (like `mysql-connector-python` or `psycopg2`) is installed.
- This example creates a simple structure for storing sensor data. You may want to expand upon this by adding indexes, foreign keys, or more complex relationships depending on your application's needs.
