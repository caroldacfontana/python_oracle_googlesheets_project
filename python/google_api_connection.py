import cx_Oracle
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Oracle Database Connection Details
host = "ol7-dba.localdomain"
port = "1521"
service_name = "orclpdb.localdomain"
username = "CAROL"
password = "CAROL"

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

# Google Sheets details
google_sheet_name = "Oracle Grants Report"  # Name of the new Google Sheet

try:
    # Step 1: Connect to Oracle Database
    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
    print("Connected to Oracle Database")

    # Execute the query
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Get column names
    column_names = [col[0] for col in cursor.description]

    # Step 2: Authenticate with Google Sheets API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/home/carol/python_oracle/XXXXXXXX.json", scope)
    client = gspread.authorize(creds)

    # Step 3: Create a New Google Sheet
    spreadsheet = client.create(google_sheet_name)  # Create a new Google Sheet
    spreadsheet.share('carolXXXXXXX@gmail.com', perm_type='user', role='writer') 
    sheet = spreadsheet.sheet1  # Access the first sheet
    print(f"Google Sheet '{google_sheet_name}' created successfully.")

    # Step 4: Write Data to the New Sheet
    # Write the header (column names)
    sheet.append_row(column_names)

    # Write the rows of data
    for row in rows:
        sheet.append_row(row)

    print(f"Query results successfully written to the Google Sheet: {google_sheet_name}")

except cx_Oracle.DatabaseError as e:
    print(f"Database connection error: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'connection' in locals() and connection:
        connection.close()
        print("Database connection closed")
