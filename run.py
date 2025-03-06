from flask import render_template
from app import create_app

app=create_app()

@app.route("/")
def hello_world():
    return render_template('index.html')

app.run(debug=True)

