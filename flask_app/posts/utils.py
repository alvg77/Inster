from PIL import Image
import secrets
import os
from flask import current_app

def save_post_pic(image):
    random_hex = secrets.token_hex(8)
    _, extention = os.path.splitext(image.filename)
    filename = random_hex + extention
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', filename)

    image = Image.open(image)
    image.save(picture_path)    
    
    return filename