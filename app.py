import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

with mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database= os.getenv("DB_NAME"),
) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM delitos")
        print(cursor.fetchone())

query = "SELECT * FROM delitos WHERE entidad like  'Ciudad %';"
