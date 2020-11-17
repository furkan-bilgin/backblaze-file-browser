from main import db
from models import *
from werkzeug.utils import secure_filename
from flask import g

backblaze = g.backblaze


def upload_file(file, directory=None):
    filename = secure_filename(file.filename).lower() 
    directory_obj = None

    if directory is not None and len(directory) > 0:
        directory_obj = get_folder(secure_filename(directory), create_new=True)

    
    file_obj = UploadedFile(filename=filename, folder_id=None if directory_obj is None else directory_obj.id)

    db.session.add(file_obj)
    db.session.commit()

    #Update file id
    file_id = backblaze.upload_file(file_obj.get_full_name(), file.read())
    file_obj.file_id = file_id

    db.session.commit()

    return file_obj


def delete_file(file):
    backblaze.delete_file(file.file_id, file.filename)

    db.session.delete(file)
    db.session.commit()

    return True


def get_all_files():
    return UploadedFile.query.filter(UploadedFile.folder_id == None).all()


def get_folders():
    return Folder.query.all()


def get_file(id):
    return UploadedFile.query.filter(UploadedFile.id == id).first()


def get_folder(name, create_new=False):
    folder = Folder.query.filter(Folder.name == name).first()
    if create_new and folder is None:
        return add_folder(name)

    return folder

def add_folder(name):
    folder = Folder(name=name)
    db.session.add(folder)
    db.session.commit()

    return folder
