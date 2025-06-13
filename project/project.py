from PIL import Image, ImageOps
import math
import os

def process_image(image_path, output_dir="processed_images"):
    os.makedirs(output_dir, exist_ok=True)

    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    scaling_factor = math.sqrt(2500 / (width * height))
    new_size = (round(scaling_factor * width), round(scaling_factor * height))
    image = image.resize(new_size)
    width, height = image.size  # Update after resizing

    image = image.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    quantized_image_path = os.path.join(output_dir, "quantized.png")
    image.save(quantized_image_path)


    grayscale_image = ImageOps.grayscale(image)
    grayscale_image_path = os.path.join(output_dir, "grayscale.png")
    grayscale_image.save(grayscale_image_path)


    image_rgb = image.convert("RGB")
    color_id = {}
    id_place = 1
    pixel_ids = []

    for i in range(height):
        row = []
        for j in range(width):
            color = image_rgb.getpixel((j, i))
            if color not in color_id:
                color_id[color] = id_place
                id_place += 1
            row.append(color_id[color])
        pixel_ids.append(row)

    return {
        "quantized_path": quantized_image_path,
        "grayscale_path": grayscale_image_path,
        "color_map": color_id,
        "pixel_ids": pixel_ids,
        "size": (width, height)
    }

