import os
import secrets
from PIL import Image
from flask import current_app



def save_picture(form_picture):
    # Resizing Picture and Creation of a New Name to make sure we don't have 2 images with same name.
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # _ is a value that we don't need.
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)
    # Os is a module that have multiple methods to help us with files.
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename
