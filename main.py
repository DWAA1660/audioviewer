from flask import Flask, render_template, request, Response
import os
from dotenv import load_dotenv
import flask
from pathlib import Path

load_dotenv()
KEY = os.getenv("KEY")
print(KEY, 1)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB limit

@app.route("/path")
def path():
    pathurl = request.args.get("path")
    files = []
    folders = []
    items = os.listdir(f"{pathurl}")
    for item in items:
        fullitem = os.path.join(f"{pathurl}", item)
        if os.path.isfile(fullitem):
            files.append(fullitem)
        else:
            folders.append(fullitem)
    print(folders,files)
    prefix_length = len("static/sources") + 1
    return render_template("index.html", files=files, folders=folders, prefix_length=prefix_length)

@app.route("/")
def index():
    
    files = []
    folders = []
    items = os.listdir(f"static/sources")
    for item in items:
        fullitem = os.path.join("static/sources", item)
        if os.path.isfile(fullitem):
            files.append(fullitem)
        else:
            folders.append(fullitem)
    print(folders,files)
    prefix_length = len("static/sources") + 1
    return render_template("index.html", files=files, folders=folders, prefix_length=prefix_length)

@app.route("/file/")
def file():
    name = request.args.get('file')
    return flask.send_from_directory((p := Path(f"{name}")).parent, p.name)

@app.route("/checkfile/")
def checkfile():
    name = request.args.get('name')
    size = request.args.get('size') # size of file in bytes
    
    exists = os.path.exists(f"static/sources/{name}")
    
    if exists and os.stat(f"static/sources/{name}").st_size == int(size):
        #file exists and is same size
        return Response(status=201)
    else:
        #file does not exist or is different size
        return Response(status=202)
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if request.headers['key'] != KEY:
            print("bad guy")
            return Response(status=401)
        name = request.form.get('name')
        last_slash_index = name.rfind('/')
        if last_slash_index != -1:
            result = name[:last_slash_index]
        else:
            result = name


        file = request.files['file']
        print(result, 0.5)
        if not os.path.exists('static/sources/' + result) and ".mp3" not in result:
            print(1)
            os.makedirs('static/sources/' + result)
        if file:
            if not ".mp3" in result:
                print(2)
                file.save('static/sources/' + result +"/" + file.filename)
            else:
                print(3)
                file.save('static/sources/' + file.filename)
            return 'File uploaded successfully'
    return 'No file selected'



app.run("0.0.0.0", port=5000)
