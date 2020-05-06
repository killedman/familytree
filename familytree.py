#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, abort, redirect, url_for, render_template, request
from dbutils import DbUtils
from constant import HOST, USER, PASSWORD, DB, TABLE_NAME


app = Flask(__name__)

my_dbutils = DbUtils(HOST, USER, PASSWORD, DB)

@app.route("/")
def index():
    results = my_dbutils.search_all_data(TABLE_NAME)
    return render_template("index.html", results=results)

@app.route("/search", methods=["POST", "GET"])
def show():
    if request.method == "POST":
        username = request.form["name"]
        if username:
            results = my_dbutils.search_data(TABLE_NAME, username)
            return render_template("search.html", results=results)
    return render_template("search.html")

@app.route("/detail")
def detail():
    user_id = request.args.get('id')
    results = my_dbutils.search_by_user_id(TABLE_NAME, user_id)
    return render_template("detail.html", results=results)

@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        username = request.form["name"]
        sex = request.form["sex"]
        birthday = request.form["birthday"]
        hometown = request.form["hometown"]
        isMarried = request.form["isMarried"]
        new_data = {"name": username,
                    "sex": sex,
                    "birthday": birthday,
                    "hometown": hometown,
                    "isMarried": isMarried}
        my_dbutils.insert_data(TABLE_NAME, new_data)
        return redirect("/")

    return render_template("add.html")

@app.route("/delete")
def delete():
    user_id = request.args.get('id')
    print("user_id is %s" % user_id)
    my_dbutils.delete(TABLE_NAME, user_id)
    return redirect("/")

@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        user_id = request.form["id"]
        username = request.form["name"]
        sex = request.form["sex"]
        birthday = request.form["birthday"]
        hometown = request.form["hometown"]
        isMarried = request.form["isMarried"]
        new_data = {"name": username,
                    "sex": sex,
                    "birthday": birthday,
                    "hometown": hometown,
                    "isMarried": isMarried}
        my_dbutils.update_data(TABLE_NAME, new_data, user_id)
        return redirect("/")

    elif request.method == "GET":
        user_id = request.args.get('id')
        results = my_dbutils.search_by_user_id(TABLE_NAME, user_id)
        print(user_id, results)
        return render_template("update.html", results=results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)