import os
from flask import Flask, send_file, jsonify, abort, request
import secrets
from dotenv import load_dotenv
import filetype
from extensions import ext_list
load_dotenv()
domain = os.getenv("DOMAIN")
file_dir = os.getenv("FILE_DIR")  # no slash
KEY = os.getenv("PRIVATE_KEY")
port = os.getenv("PORT")
app = Flask("SimpyleUpload")
@app.route("/<file>")
def serveFile(file):
    for ext in ext_list:
        if os.path.isfile("{}/{}.{}".format(file_dir, file, ext)):
            return send_file("{}/{}.{}".format(file_dir, file, ext))
    return "Sorry, we don't support that yet! Try making an issue on GitHub.", 422      
@app.route("/upload", methods=['POST'])
def uploadFile():
    if request.args.get('key', 'invalid', type=str) != KEY:
        abort(403)
    filename = secrets.token_urlsafe(3)
    exte = filetype.guess(request.files.get('file'))
    if exte == None:
        ext = "txt"
    ext = exte.extension
    if ext not in ext_list:
        print(ext)   
    request.files.get('file').save(f"{file_dir}/{filename}.{ext.lower()}")
    print("New file posted! Name: " + filename)
    return jsonify({"status": 200, "url": f"https://{domain}/{filename}"})
app.run(host="0.0.0.0", port=port)