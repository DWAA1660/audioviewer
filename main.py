from flask import Flask, render_template, request, Response
import os
import flask
from pathlib import Path

app = Flask(__name__)

@app.route("/")
def index():
    files = os.listdir("static/sources")
    return render_template("index.html", files=files)

@app.route("/file/<file>")
def file(file):
    return flask.send_from_directory((p := Path(f"static/sources/{file}")).parent, p.name)

@app.route("/checkfile/<file>")
def file(file):
    exists = os.path.exists(f"static/sources/{file}")
    if exists:
        return Response(status=200)
    else:
        return Response(status=201)
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save('uploads/' + file.filename)
            return 'File uploaded successfully'
    return 'No file selected'



app.run("0.0.0.0", port=5000)
