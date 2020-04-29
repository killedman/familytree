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

    return render_template("add.html")

@app.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        username = request.form["name"]
        my_dbutils.delete_data(TABLE_NAME, username)
    return render_template("delete.html")


@app.route("/update", methods=["POST", "GET"])
def update():
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
        if username:
            results = my_dbutils.search_data(TABLE_NAME, username)
            if results:
                my_dbutils.update_data(TABLE_NAME, "isMarried",
                                       isMarried, username)
            else:
                my_dbutils.insert_data(TABLE_NAME, new_data)
    return render_template("update.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)