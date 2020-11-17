from flask import current_app as app
from main import db
from datetime import datetime
import os


class Folder(db.Model):
    __tablename__ = "folders"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    files = db.relationship("UploadedFile", primaryjoin="UploadedFile.folder_id == Folder.id")


class UploadedFile(db.Model):
    __tablename__ = "uploaded_files"

    id = db.Column(db.BigInteger, primary_key=True)
    filename = db.Column(db.String(100))
    file_id = db.Column(db.String(600))

    folder_id = db.Column(db.BigInteger, db.ForeignKey("folders.id"))
    
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    folder = db.relationship("Folder", primaryjoin="UploadedFile.folder_id == Folder.id", uselist=False)

    def get_full_name(self):
        folder_name = ""
        
        if self.folder is not None:
            folder_name = self.folder.name + "/"

        return folder_name + self.filename

    def get_full_url(self):
        return os.environ["cdn_url"] + "/" + self.get_full_name()


class DeleteSchedule(db.Model):
    __tablename__ = "delete_schedules"
    id = db.Column(db.BigInteger, primary_key=True)
    uploaded_file_id = db.Column(db.BigInteger, db.ForeignKey("uploaded_files.id"))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    remove_timestamp = db.Column(db.Integer)

