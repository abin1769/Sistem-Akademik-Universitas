import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="siak"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print("Gagal koneksi ke database:", e)
        return None
