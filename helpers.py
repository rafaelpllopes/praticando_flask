from jogoteca import app
import os

def remover_arquivo(img):
    upload_path = app.config['UPLOAD_PATH']
    os.remove(f'{upload_path}/{img}.jpg')