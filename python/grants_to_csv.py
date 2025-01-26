import cx_Oracle
import csv

# Oracle Database Connection Details
host = "ol7-dba.localdomain"  # e.g., "localhost" or "192.168.1.100"
port = "1521"             # Default Oracle port
service_name = "orclpdb.localdomain"  # e.g., "orclpdb.localdomain"
username = "CAROL"  # e.g., "SYS"
password = "CAROL"  # e.g., "your_password"

# SQL Query
query = """
SELECT 
    a.GRANTEE,
    a.OWNER,
    a.TABLE_NAME,
    a.PRIVILEGE,
    a.TYPE,
    b.INSTANCE_NAME
FROM 
    DBA_TAB_PRIVS a
CROSS JOIN 
    V$INSTANCE b
WHERE 
    a.GRANTEE = 'TESTE'
"""

# Output CSV file
output_file = "TESTE_grants.csv"

try:
    # Create a Data Source Name (DSN)
    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
    
    # Connect to the Oracle database
    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
    print("Connected to Oracle Database")

    # Create a cursor to execute the query
    cursor = connection.cursor()
    cursor.execute(query)

    # Fetch all rows from the query result
    rows = cursor.fetchall()

    # Get column names from the cursor description
    column_names = [col[0] for col in cursor.description]

    # Write the results to a CSV file using csv.writer
    with open(output_file, mode="w", newline="") as file:
        csv_writer = csv.writer(file)
        
        # Write the header (column names)
        csv_writer.writerow(column_names)
        
        # Write the data rows
        csv_writer.writerows(rows)
    
    print(f"Query results saved to {output_file}")

except cx_Oracle.DatabaseError as e:
    # Handle database connection errors
    print(f"Database connection error: {e}")

finally:
    # Ensure the database connection is closed
    if 'connection' in locals() and connection:
        connection.close()
        print("Database connection closed")
