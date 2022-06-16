import psycopg2
import os
from flask import Flask, render_template
from module.postg import convert_postgres_url_to_dict
DATABASE_URL = os.environ.get('DATABASE_URL')

settings = convert_postgres_url_to_dict(DATABASE_URL)
print(settings)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
conn = psycopg2.connect(DATABASE_URL)
@app.route('/')
def index():
    return render_template('index.html')
@app.route("/testsql")
def testsql():
    sql_query_result=""
    with conn.cursor() as cursor:
        cursor.execute('SELECT note_text FROM note LIMIT 1;')
        sql_query_result = cursor.fetchone()[0]
        print("Query result", sql_query_result)
        return str(sql_query_result)

if __name__ == '__main__': app.run(debug=True)
