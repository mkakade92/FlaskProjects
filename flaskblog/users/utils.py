import os
import  secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def remove_orig(filename):
    path = os.path.join(current_app.root_path,'static/profile_pics/',filename)
    print(path)
    if os.path.exists(path):
        os.remove(path)
    else:
        print("Cannot Delete as it does not exist")
    return

def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    remove_orig(current_user.image_file)
    picture_fn = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path,'static/profile_pics/',picture_fn)

    output_size = (125,125)
    img =Image.open(form_pic)
    img.thumbnail(output_size)
    img.save(pic_path)
    
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        'Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email]  
    )
    msg.body = f'''To reset your password , visit the following link:
{url_for('users.reset_token',token=token,_external=True)}

If you did not make this request then ignore.
'''
    mail.send(msg)