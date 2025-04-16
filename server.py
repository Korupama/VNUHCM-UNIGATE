from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
from dotenv import load_dotenv
import json

def connect_db():
    load_dotenv()
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRESQL_DB'),
        user=os.getenv('POSTGRESQL_USER'),
        password=os.getenv('POSTGRESQL_PASSWORD'),
        host=os.getenv('POSTGRESQL_HOST'),
        port=os.getenv('POSTGRESQL_PORT'),
        sslmode='require'
    )
    return conn

conn = connect_db()

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Định nghĩa API route
@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI"}

@app.get("/api/get-posts")
def get_posts():
    with open('./nosqlDB/forum.json', 'r') as f:
        data = json.load(f)
    return data

# @app.post('/api/add-post')
# @app.post('/api/update-post')

@app.get("/api/authenticate-user")
def authenticate_user(cccd: str, password: str):
    print("Username:", cccd)
    print("Password:", password)
    with conn.cursor() as cur:
        cur.execute("select check_password(%s,%s)", (cccd, password))
        user = cur.fetchone()
    if user:
        return {"message": "User authenticated successfully", "user": cccd}
    else:
        return {"message": "Invalid username or password"}
    