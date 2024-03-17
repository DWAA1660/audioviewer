from flask import Flask, render_template, send_file, request, Response
import os

app = Flask(__name__)

@app.route("/")
def index():
    files = os.listdir("static/sources")
    return render_template("index.html", files=files)

@app.route("/file/<file>")
def file(file):
    return send_file(f"static/sources/{file}")

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