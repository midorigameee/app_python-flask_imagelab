from flask import Flask, render_template, request, url_for, redirect
import os
import sys
import datetime


app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = "images"


@app.route('/')
def index():
    return render_template(
        "index.html"
        )


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # URLでhttp://127.0.0.1:5000/uploadを指定したときはGETリクエストとなるのでこっち
    if request.method == 'GET':
        return render_template('upload.html')
    # formでsubmitボタンが押されるとPOSTリクエストとなるのでこっち
    elif request.method == 'POST':
        file = request.files['example']
        file.save(os.path.join('static', 'images', file.filename))
        return redirect(url_for('uploaded_file', filename=file.filename))


@app.route('/uploaded_file/<string:filename>')
def uploaded_file(filename):
    filepath = createImgPath(filename)

    print("[UPLOAD]filename : {}".format(filename))
    print("[UPLOAD]filepath : {}".format(filepath))

    return render_template(
        'uploaded_file.html',
        filename=filename,
        filepath=filepath
        )


@app.route('/view', methods=['GET'])
def view():
    # static/images以下のデータを全て取得する
    filename_list = checkImgExtension(os.listdir(os.path.join("static", app.config["UPLOAD_FOLDER"])))
    filepath_list = []
    for fname in filename_list:
        fpath = createImgPath(fname)
        filepath_list.append(fpath)

    print("[VIEW]filename_list : {}".format(filename_list))
    print("[VIEW]filepath_list : {}".format(filepath_list))

    return render_template(
        'view.html',
        list_len=len(filename_list),
        filename_list=filename_list,
        filepath_list=filepath_list
        )


@app.route('/detail', methods=['GET'])
def detail():
    filename = request.args["filename"]
    filepath = createImgPath(filename)

    print("[DETAIL]filename : " + filename)
    print("[DETAIL]filepath : " + filepath)

    path_for_info = os.path.join("static", filepath)
    updated_time = getFileUpdatedTime(path_for_info)
    created_time = getFileCreatedTime(path_for_info)

    print("[DETAIL]updated_time : {}".format(updated_time))
    print("[DETAIL]created_time : {}".format(created_time))

    return render_template(
        "detail.html",
        filename=filename,
        filepath=filepath,
        updated_time=updated_time,
        created_time=created_time
        )


@app.route('/delete', methods=['GET'])
def delete():
    filename = request.args["filename"]
    filepath_for_py = os.path.join("static", app.config["UPLOAD_FOLDER"], filename)
    print("[DELETE]filename : {}".format(filename))
    print("[DELETE]filepath_for_py : {}".format(filepath_for_py))

    os.remove(filepath_for_py)

    if os.path.exists(filepath_for_py) is None:
        print("Delete completed [{}]".format(filepath_for_py))

    return render_template(
        "index.html"
        )


# ./image/filenameのパスを生成するメソッド
def createImgPath(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.name == "nt":
        filepath = converUrlForHtml(filepath)

    return filepath


# Windows環境でos.path.joinを使ってURL作成するとスラッシュがバックスラッシュになってしまうので修正するメソッド
def converUrlForHtml(url):
    return url.replace("\\", "/")


def getFileUpdatedTime(filename):
    # 参考 https://www.mathpython.com/file-date
    t = os.path.getmtime(filename)  # この時点ではUNIX時間
    d = datetime.datetime.fromtimestamp(t)  # 一般の時間に変換

    return d


def getFileCreatedTime(filename):
    if os.name == "nt": # Win用
        t = os.path.getctime(filename)
        d = datetime.datetime.fromtimestamp(t)
        return d
    else:   # Win以外
        try:
            t = os.stat(filename).st_birthtime
            d = datetime.datetime.fromtimestamp(t)
            return d
        except AttributeError:
            return "None"



def checkImgExtension(img_list):
    checked_list = []
    extension_list = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

    for i, img in enumerate(img_list):
        if (os.path.splitext(img)[1] in extension_list):
            checked_list.append(img)

    return checked_list


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "debug":
        app.run(host="0.0.0.0", debug=True)
    else:
        app.run(host="0.0.0.0", debug=False)
