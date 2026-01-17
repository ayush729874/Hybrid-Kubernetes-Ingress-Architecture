from fastapi import FastAPI, Request
import mysql.connector
import os

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )

@app.post("/submit")
async def submit_data(request: Request):
    data = await request.json()
    name = data.get("name")

    if not name:
        return {"error": "name is required"}

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()

    return {"status": "inserted", "name": name}
