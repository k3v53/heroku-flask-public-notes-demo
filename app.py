import psycopg2
import os
from flask import Flask, redirect, render_template, request
def heroku_get_DATABASE_URL():
	ret = os.popen('heroku config:get DATABASE_URL --app {}'.format(os.environ.get("HEROKU_APP")))
	return ret.read().strip()


DATABASE_URL = os.environ.get('DATABASE_URL') or heroku_get_DATABASE_URL()
app = Flask(__name__)
conn = None
if DATABASE_URL:
	conn = psycopg2.connect(DATABASE_URL, sslmode=os.environ.get("SSLMODE"))
@app.route('/')
def index():
	return render_template('index.html')

if conn:
	@app.route('/sql_create', methods=["GET"])
	def sql_create():
		if request.args.get('passwd') == os.environ.get("ClearDB_Key"):
			with conn.cursor() as cursor:
				cursor.execute("""--sql
                DROP TABLE IF EXISTS public.note;
                CREATE TABLE public.note (
                note_id SERIAL PRIMARY KEY,
                created_at timestamp without time zone NOT NULL DEFAULT NOW(),
                note_text text NULL
                );
                commit;""")
			return "Dropped and Created 'public.note' table"
		return "Need password"
	@app.route('/sql_insert', methods=["GET","POST"])
	def sql_insert():
		note = request.form.get('note')
		if(note):
			with conn.cursor() as cursor:
				cursor.execute(f"INSERT INTO public.note(note_text) VALUES (\'{note}\');commit;")
				return redirect(f"/sql_select")
		else:
			return render_template("sql_insert.html")
	@app.route('/sql_select', methods=["GET"])
	def sql_select():
		sql_query = "SELECT note_id, note_text, created_at FROM public.note ORDER BY note_id DESC LIMIT 1000"
		note_id = request.args.get('note_id')
		if note_id:
			sql_query+=f" WHERE note_id={note_id};"
		with conn.cursor() as cursor:
			cursor.execute(sql_query)
			return render_template("sql_select.html",notes=cursor.fetchall())
if __name__ == '__main__': app.run(debug=True)
