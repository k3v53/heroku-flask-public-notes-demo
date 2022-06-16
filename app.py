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

if conn:
    @app.route('/sql_create')
    def sql_create():
        with conn.cursor() as cursor:
            cursor.execute("""--sql
        DROP TABLE IF EXISTS public.note;
        CREATE TABLE public.note (
        note_id SERIAL PRIMARY KEY,
        created_at timestamp without time zone NOT NULL DEFAULT NOW(),
        note_text text NULL
    );""")
        return "Created 'note' table"
    @app.route('/sql_insert', methods=["GET"])
    def sql_insert():
        note = request.args.get('note')
        with conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO public.note(note_text) VALUES (\'{note}\')")
        return f'Inserted {note}'
    @app.route('/sql_select')
    def sql_select():
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM note")
            return cursor.fetchall()
if __name__ == '__main__': app.run(debug=True)
