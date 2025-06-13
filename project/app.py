from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image, ImageOps
import math
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'static/processed_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def process_image(image_path):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    scaling_factor = math.sqrt(2500 / (width * height))
    image = image.resize((round(scaling_factor * width), round(scaling_factor * height)))
    width, height = image.size

    quantized = image.quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    grayscale = ImageOps.grayscale(quantized)

    quant_path = os.path.join(PROCESSED_FOLDER, "quantized.png")
    gray_path = os.path.join(PROCESSED_FOLDER, "grayscale.png")
    quantized.save(quant_path)
    grayscale.save(gray_path)
    
    image_rgb = quantized.convert("RGB")
    color_id = {}
    id_counter = 1
    pixel_ids = []

    for y in range(height):
        row = []
        for x in range(width):
            color = image_rgb.getpixel((x, y))
            if color not in color_id:
                color_id[color] = id_counter
                id_counter += 1
            row.append({
                "id": color_id[color],
                "rgb": color
            })
        pixel_ids.append(row)

    return width, height, pixel_ids

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            width, height, pixel_data = process_image(filepath)
            with open("static/pixels.json", "w") as f:
                json.dump(pixel_data, f)

            return redirect(url_for('result'))
    return render_template("index.html")

@app.route("/result")
def result():
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)
