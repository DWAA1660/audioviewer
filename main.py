from flask import Flask, render_template, send_file, request, Response, jsonify
import os
import math
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("KEY")
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB limit
ITEMS_PER_PAGE = 50  # Number of items to display per page

@app.route("/path")
def path():
    pathurl = request.args.get("path")
    page = request.args.get("page", 1, type=int)
    
    try:
        # Get all items in directory
        all_items = os.listdir(pathurl)
        total_items = len(all_items)
        total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
        
        # Calculate pagination indices
        start_idx = (page - 1) * ITEMS_PER_PAGE
        end_idx = min(start_idx + ITEMS_PER_PAGE, total_items)
        
        # Get paginated items
        paginated_items = all_items[start_idx:end_idx]
        
        files = []
        folders = []
        
        for item in paginated_items:
            fullitem = os.path.join(pathurl, item)
            if os.path.isfile(fullitem):
                files.append(fullitem)
            else:
                folders.append(fullitem)
                
        prefix_length = len("static/sources") + 1
        return render_template("index.html", 
                              files=files, 
                              folders=folders, 
                              prefix_length=prefix_length,
                              current_page=page,
                              total_pages=total_pages,
                              total_items=total_items,
                              path=pathurl)
    except Exception as e:
        return f"Error accessing directory: {str(e)}"

@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    
    try:
        # Get all items in directory
        all_items = os.listdir("static/sources")
        total_items = len(all_items)
        total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
        
        # Calculate pagination indices
        start_idx = (page - 1) * ITEMS_PER_PAGE
        end_idx = min(start_idx + ITEMS_PER_PAGE, total_items)
        
        # Get paginated items
        paginated_items = all_items[start_idx:end_idx]
        
        files = []
        folders = []
        
        for item in paginated_items:
            fullitem = os.path.join("static/sources", item)
            if os.path.isfile(fullitem):
                files.append(fullitem)
            else:
                folders.append(fullitem)
                
        prefix_length = len("static/sources") + 1
        return render_template("index.html", 
                              files=files, 
                              folders=folders, 
                              prefix_length=prefix_length,
                              current_page=page,
                              total_pages=total_pages,
                              total_items=total_items,
                              path="static/sources")
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/file/")
def file():
    name = request.args.get('file')
    return send_file(f"{name}")

@app.route("/checkfile/")
def checkfile():
    name = request.args.get('name')
    name = name.replace("\\", "/")
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
        name = name.replace("\\", "/")
        last_slash_index = name.rfind('/')
        if last_slash_index != -1:
            result = name[:last_slash_index]
        else:
            result = name


        file = request.files['file']
        print(result, 0.5)
        if not os.path.exists('static/sources/' + result) and ".mp3" not in result and ".mp2" not in result:
            print(1)
            os.makedirs('static/sources/' + result)
        if file:
            if ".mp3" not in result and ".mp2" not in result:
                print(2)
                file.save('static/sources/' + result +"/" + file.filename)
            else:
                print(3)
                file.save('static/sources/' + file.filename)
            return 'File uploaded successfully'
    return 'No file selected'



@app.route('/api/directory_contents')
def get_directory_contents():
    """API endpoint to get directory contents with pagination"""
    path = request.args.get('path', 'static/sources')
    page = request.args.get('page', 1, type=int)
    
    try:
        # Get all items in directory
        all_items = os.listdir(path)
        total_items = len(all_items)
        total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
        
        # Calculate pagination indices
        start_idx = (page - 1) * ITEMS_PER_PAGE
        end_idx = min(start_idx + ITEMS_PER_PAGE, total_items)
        
        # Get paginated items
        paginated_items = all_items[start_idx:end_idx]
        
        files = []
        folders = []
        
        for item in paginated_items:
            fullitem = os.path.join(path, item)
            if os.path.isfile(fullitem):
                files.append(fullitem)
            else:
                folders.append(fullitem)
        
        return jsonify({
            'files': files,
            'folders': folders,
            'current_page': page,
            'total_pages': total_pages,
            'total_items': total_items
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)