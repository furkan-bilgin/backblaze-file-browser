from wtforms import *

class UploadFileForm(Form):
    file = FileField()
    directory = FileField()
