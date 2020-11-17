from flask import *
from flask import current_app as app
from forms import *
from main import db
import file


@app.route("/")
def homepage():
    return render_template("index.html", files=file.get_all_files(), folders=file.get_folders())


@app.route("/folder/<name>")
def show_folder(name):
    folder = file.get_folder(name)
    if folder is None:
        abort(404)

    return render_template("folder.html", files=folder.files, folder_name=name)


@app.route("/upload", methods=["POST"])
def upload_file():
    form = UploadFileForm(request.form)
    
    if not form.validate():
        abort(400)
    else:
        file.upload_file(request.files["file"], directory=form.directory.data)

    return "ok"


@app.route("/delete/<id>")
def delete_file(id):
    f = file.get_file(id)

    if f is None:
        return render_template("404.html")

    file.delete_file(f)

    return render_template("success.html")