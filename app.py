# coding=utf-8
import os
import sys
import re
import ast
import json
import time
import random
import numpy as np
import textwrap
from datetime import timedelta
from functools import reduce
from pathlib import Path
from bson import json_util
import asyncio


# 檔案類型檢查
import magic

# 讀取.env檔
from dotenv import load_dotenv, find_dotenv

# 輸出詳細錯誤信息
import traceback

# MongoDB CRUD模組
# from db import Mongodb, connect, disconnect, run, pp
# connect()  # 連線Mongodb

# Flask
from flask import (
    Flask,
    request,
    Response,
    make_response,
    abort,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify,
    session,
    send_from_directory,
)

# 異常處理
from werkzeug import exceptions

# 檔名安全處理
from werkzeug.utils import secure_filename

# Bootstrap-Flask (https://github.com/helloflask/bootstrap-flask)
from flask_bootstrap import Bootstrap5

# 自訂模組
from modules.utils import (
    search_path,  # search_path: 搜尋檔案或資料夾
)

# 辨識羊隻ID、活動量
from modules.test_img import identify_id
from modules.test_video import identify_activity

# 從.env載入環境變數
env_path = find_dotenv(raise_error_if_not_found=True)
load_dotenv(env_path)


app = Flask(__name__)
# Flask flash需要Session，因此需使用密鑰，防止CSRF。
app.secret_key = os.getenv("SECRET_KEY") or None
# 設置session有效期限
app.permanent_session_lifetime = timedelta(days=365)

# 上傳文件存放處
app.config["UPLOAD_FOLDER"] = Path("static").joinpath("uploads")

# Bootstrap-Flask(Bootstrap5 CSS框架包裝Flask)
bootstrap = Bootstrap5(app)


# 開發者登入密碼
Developer_Pwd = os.getenv("DEV_PASSWORD") or None

if Developer_Pwd is None:
    raise ValueError(".env檔尚未設置密碼!")

# 開發模式
is_dev = False

# 當開發模式啟用時，啟用開發者登入授權
if is_dev:
    # 檢查登入狀態
    @app.before_request
    async def is_login():
        if request.path == "/dev_login":
            return

        if session.get("is_login") != True:
            return redirect(url_for("dev_login"))
        else:
            return

    # = = = 授權(開發者登入頁面) = = =
    @app.route("/dev_login", methods=["GET", "POST"])
    async def dev_login():
        if session.get("is_login") == True:
            return redirect("/")

        if request.method == "POST":
            password = request.form.get("password")
            if password == Developer_Pwd:
                session.permanent = True
                session["is_login"] = True
                return redirect("/")
            else:
                flash("登入失敗!")
                return redirect("/dev_login")
        else:
            return render_template("./Auth/dev_login.html")


# 🌟🌟🌟 首頁 🌟🌟🌟
@app.route("/", methods=["GET", "POST"])
async def home(file=None):
    if "file" in request.args:
        args = request.args.to_dict()
        file = json.loads(args.get('file'))
        print(type(file))
    return render_template("home.html", file_info=file)


# 上傳檔案
@app.route("/upload_file", methods=["POST"])
async def upload_file():
    # 處理上傳的檔案
    file = None
    if request.method == "POST":
        # 檢查上傳的是否為檔案
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        # 取得檔案
        file = request.files["file"]

        # 當使用者沒有選擇檔案
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        # 檢查檔案並儲存至存放區
        file_info = {"path": "", "type": ""}
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file_path = app.config["UPLOAD_FOLDER"].joinpath(file_name)
            file.save(file_path)
            redirect(url_for("download_file", name=file_name))

            # 檔案路徑
            file_path = file_path.as_posix()
            # 取得檔案類型: image/video
            file_type = magic.from_file(str(file_path), mime=True).split("/")[0]
            # 檔案資訊
            file_info = {"path": file_path, "type": file_type}

        return redirect(url_for("home", file=json.dumps(file_info)))


# 檢查檔案格式是否為圖片或影片
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "webm", "avi", "wmv"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# 下載檔案
@app.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name, as_attachment=True)


# 訓練頁面
@app.route("/train", methods=["GET", "POST"])
async def train():
    return render_template("train.html")


# 預測頁面(測試頁面)
@app.route("/predict", methods=["GET", "POST"])
async def predict():
    return redirect(url_for("home"))
    # return render_template("predict.html")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

    # Flask熱重載功能
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
