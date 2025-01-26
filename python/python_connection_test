import cx_Oracle

# Connection details
username = "CAROL"
password = "CAROL"
dsn = "ol7-dba.localdomain:1521/orclpdb.localdomain"

try:
    # Connect to the Oracle database
    connection = cx_Oracle.connect(f"{username}/{password}@{dsn}")
    print(f"Connected to {username}")

    # Perform database operations here if needed

except cx_Oracle.DatabaseError as e:
    # Handle database connection errors
    print(f"Database connection error: {e}")

finally:
    # Ensure the connection is closed
    if 'connection' in locals() and connection:
        connection.close()
        print("Database connection closed")
