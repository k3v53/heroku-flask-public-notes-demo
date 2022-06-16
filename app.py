import psycopg2
import os
from flask import Flask, render_template, request
DATABASE_URL = os.environ.get('DATABASE_URL')
app = Flask(__name__)
conn = None
if DATABASE_URL:
    conn = psycopg2.connect(DATABASE_URL)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sql_create')
def sql_create():
    with conn.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS public.note (
    created_at timestamp without time zone NOT NULL,
    note_text text NULL,
    note_id integer NOT NULL
);
ALTER TABLE
    public.note
ADD
    CONSTRAINT note_pkey PRIMARY KEY (note_id);
    """)
    return True
@app.route('/sql_insert', methods=["GET"])
def sql_insert():
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO note VALUES ({request.args.get('note')})")
    return True
@app.route('/sql_select')
def sql_select():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM note")
    return cursor.fetchall()
if __name__ == '__main__': app.run(debug=True)
