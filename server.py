import os
from flask import Flask, send_file, jsonify, abort, request
import secrets
from dotenv import load_dotenv
load_dotenv()
byte_count = os.getenv("BYTE_COUNT")
domain = os.getenv("DOMAIN")
image_dir = os.getenv("IMAGE_DIR")  # no slash
KEY = os.getenv("PRIVATE_KEY")
port = os.getenv("PORT")
app = Flask("SimpyleUpload")
@app.route("/<img>")
def serveImage(img):
    if os.path.isfile("{}/{}.png".format(image_dir, img)):
        image = img
    else:
        abort(404)
    return send_file("{}/{}.png".format(image_dir, image))
@app.route("/upload", methods=['POST'])
def upload():
    key = request.args.get('key', 'invalid', type=str)
    if key != KEY:
        abort(403)
    f = request.files.get('file')
    filename = secrets.token_urlsafe(int(byte_count))
    f.save(f"{image_dir}/{filename}.png")
    print("New image posted! Name: " + filename)
    return jsonify({"status": 200, "url": f"https://{domain}/{filename}"})
app.run(host="0.0.0.0", port=port)