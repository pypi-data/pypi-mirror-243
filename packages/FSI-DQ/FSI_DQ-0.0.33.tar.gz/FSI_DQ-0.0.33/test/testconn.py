import os
import pyodbc, struct
from azure import identity



def get_conn(connection_string):
    credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string)#, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn


def main(connection_string):
    try:
        conn = get_conn(connection_string)
        cursor = conn.cursor()

        # Table should be created ahead of time in production app.
        cursor.execute("""
            SELECT  * from db_act.Channel
        """)
        row = cursor.fetchall()
        print(row)
    except Exception as e:
        # Table may already exist
        print(e)


#connection_string = 'Server=tcp:fsideveusrkasql01.database.windows.net,1433;Initial Catalog=fsideveusrkafwkdb02;Persist Security Info=False;User ID=SQLAdmin;Password=EHUXW54V3MJCE-139b25f6-bb0c-4af7-94ef-20d7a3c5480d;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;'
connection_string='Driver={ODBC Driver 17 for SQL Server};Server=tcp:fsideveusrkasql01.database.windows.net,1433;Database=fsideveusrkafwkdb02;Uid=SQLAdmin;Pwd=EHUXW54V3MJCE-139b25f6-bb0c-4af7-94ef-20d7a3c5480d;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

main(connection_string)