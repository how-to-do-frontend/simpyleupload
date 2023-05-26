import os
from flask import Flask, send_file, jsonify, abort, request
import secrets
from dotenv import load_dotenv
import imghdr
import mimetypes
load_dotenv()
domain = os.getenv("DOMAIN")
file_dir = os.getenv("FILE_DIR")  # no slash
KEY = os.getenv("PRIVATE_KEY")
port = os.getenv("PORT")
app = Flask("SimpyleUpload")
@app.route("/<file>")
def serveFile(file):
    ext = mimetypes.guess_extension(mimetypes.guess_type(f"{file_dir}/{file}")[0])
    if os.path.isfile("{}/{}.{}".format(file_dir, file, ext)):
        filename = file
    else:
        abort(404)
    return send_file("{}/{}*".format(file_dir, filename))
@app.route("/upload", methods=['POST'])
def uploadFile():
    key = request.args.get('key', 'invalid', type=str)
    if key != KEY:
        abort(403)
    f = request.files.get('file')
    filename = secrets.token_urlsafe(3)
    ext = imghdr.what(f)
    f.save(f"{file_dir}/{filename}.{ext}")
    print("New file posted! Name: " + filename)
    return jsonify({"status": 200, "url": f"https://{domain}/{filename}"})
app.run(host="0.0.0.0", port=port)