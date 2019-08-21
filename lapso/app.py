from flask import Flask, render_template, request
from flask import redirect, g, flash, send_from_directory
import sqlite3
import datetime
import os
from helpers import upload_file_to_s3, allowed_file
from helpers import random_string, delete_file_from_s3
from images import get_image_properties

app = Flask(__name__)
app.config.from_object("config")

DATABASE = '/app/db/lapso.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    cur = get_db().execute(
        """select id, object, dt, bytessize, width, height
           from photos
           order by dt desc"""
    )
    photos = [dict(id=row[0],
              object=row[1],
              dt=datetime.datetime.strptime(
                    row[2],
                    '%Y-%m-%d %H:%M:%S'
                 ).strftime("%d-%m-%Y %H:%M"),
              d=datetime.datetime.strptime(
                    row[2],
                    '%Y-%m-%d %H:%M:%S'
                ).strftime("%d-%m-%Y"),
              bytessize=("{0:.3f}".format(int(row[3]) / (1024 * 1024))),
              width=row[4],
              height=row[5])
              for row in cur.fetchall()]
    cur.close()
    return render_template("index.html", photos=photos)


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_photo():

    try:
        file = request.files["user_file"]
    except KeyError:
        flash("No file sent.")
        return redirect(request.url)

    extension = os.path.splitext(file.filename)[1]

    if not allowed_file(file.filename):
        flash("The extension of this file (%s) is not allowed." % extension)
        return redirect("/")

    if not file.filename:
        flash("Please select a file.")
        return redirect("/")

    file.filename = random_string(16) + extension
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'] + "/" + file.filename)
    bytessize, width, height, exif = get_image_properties(file_path)

    datetime_original = exif.get('DateTimeOriginal', None)
    if datetime_original:
        datetime_original = datetime.datetime.strptime(
            datetime_original, '%Y:%m:%d %H:%M:%S'
        )
        datetime_original = datetime_original.strftime("%Y-%m-%d %H:%M:%S")

    url = upload_file_to_s3(file_path, file.filename,
                            file.content_type, app.config["S3_BUCKET"])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur = get_db().execute("""
        insert into photos
        (object, dt_uploaded, dt,original_name, bytessize, width, height)
        values
        (?,?,?,?,?,?,?)""", (url, now, datetime_original or now, file.filename,
                             bytessize, width, height,))
    g._database.commit()
    cur.close()
    os.remove(file_path)
    return redirect("/")


@app.route("/delete/<id_image>", methods=["GET"])
def delete_photo(id_image):
    # GET IMAGE DATA
    cur = get_db().execute(
        "select id, object from photos where id=?", (id_image,)
    )
    row = cur.fetchone()

    if not row:
        return "not found", 404

    im = {
        "id": row[0],
        "object": row[1]
    }
    cur.close()

    delete_file_from_s3(
        app.config["S3_BUCKET"],
        im.get('object').replace(
            app.config.get('S3_LOCATION'), ''
        )
    )
    cur = get_db().execute("delete from photos where id=?", (id_image,))
    g._database.commit()
    cur.close()

    flash("Photo has been deleted.")
    return redirect("/")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


if __name__ == "__main__":
    app.run()
