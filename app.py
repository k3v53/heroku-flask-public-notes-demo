import os
from flask import Flask, render_template
DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__': app.run(debug=True)
