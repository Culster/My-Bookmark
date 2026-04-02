from flask import Flask, render_template, request
import json, markdown

app = Flask(__name__)

notescontent = "contents/notes/"
bookmarkscontent = "contents/bookmarks/"

@app.route("/savenotes", methods=['GET', 'POST'])
def savingnotes():
    titleofnotes = request.form["titleofnotes"]
    contentofnotes = request.form["contentofnotes"].replace("\r\n", "\n")
    tagsofnotes = request.form["tagsofnotes"].split()
    with open(notescontent+request.form["titleofnotes"]+".json", "w") as f:
        f.write(json.dumps({
            "title": titleofnotes,
            "content": contentofnotes,
            "tags": tagsofnotes
        }))

    return request.form

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/bookmarks")
def bookmarks():
    return render_template("bookmarks.html")

@app.route("/notes")
def notes():
    return render_template("notes.html")

@app.route("/notes/<notesname>")
def readingnotes(notesname):
    with open(notescontent+notesname+".json", "r") as f:
        content = json.loads(f.read())
    
    contentmd = markdown.markdown(content["content"])

    return render_template("readingnotes.html", content=content, markdownpart=contentmd)

@app.route("/input")
def inputpage():
    return render_template("inputnotes.html")