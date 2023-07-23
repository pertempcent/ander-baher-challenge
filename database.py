import sqlite3
import requests

def fetch_data():
    api_url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                website TEXT NOT NULL
            )
        """)

        for user in data:
            cursor.execute("""
                INSERT INTO users (name, username, email, phone, website) 
                VALUES (?, ?, ?, ?, ?)
            """, (user["name"], user["username"], user["email"], user["phone"], user["website"]))

        conn.commit()
        conn.close()

        return data
    else:
        return None

def create_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            website TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def insert_data(data):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    for user in data:
        cursor.execute("""
            INSERT INTO users (name, username, email, phone, website) 
            VALUES (?, ?, ?, ?, ?)
        """, (user["name"], user["username"], user["email"], user["phone"], user["website"]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    data = fetch_data()
    if data:
        create_table()
        insert_data(data)
        print("Data inserted successfully.")
    else:
        print("Failed to fetch data from the API.")
