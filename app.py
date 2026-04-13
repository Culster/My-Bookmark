from flask import Flask, render_template, request
from operator import itemgetter
import datetime, json, markdown, os

app = Flask(__name__)

notescontent = "contents/notes/"
bookmarkscontent = "contents/bookmarks/"

@app.route("/savenotes", methods=['GET', 'POST'])
def savingnotes():
    idofnotes = request.form["idofnotes"]
    titleofnotes = request.form["titleofnotes"]
    contentofnotes = request.form["contentofnotes"].replace("\r\n\r\n", "\n\n")
    contentofnotes = contentofnotes.replace("\r\n", "<br>")
    tagsofnotes = request.form["tagsofnotes"].split()

    if idofnotes!="null":
        filename = idofnotes
    else:
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d%H%M%S")
    
    with open(notescontent+filename+".json", "w") as f:
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
    listdir = os.listdir(notescontent)
    lenlistdir = len(listdir)

    listofnoteslist = []

    for i in listdir:
        with open(notescontent+i) as f:
            content = json.loads(f.read())
        listofnoteslist.append({"id": i[:-5], "title": content["title"]})
    
    listofnoteslist = sorted(listofnoteslist, key=itemgetter("title"))
    listofnotes = ""
    
    for i in listofnoteslist:
        ilink = "notes/"+i["id"]
        listofnotes+="- [%s](%s)" %(i["title"], ilink)
        listofnotes+="\r\n"
    
    listofnotes = markdown.markdown(listofnotes)
    
    return render_template("notes.html", lennoteslist=lenlistdir, unorderednoteslist=listofnotes)

@app.route("/notes/<notesname>")
def readingnotes(notesname):
    with open(notescontent+notesname+".json", "r") as f:
        content = json.loads(f.read())

    contentmd = markdown.markdown(content["content"])

    tagsofnotes = ""
    
    for i in content["tags"]:
        tagsofnotes+=i
        if i==content["tags"][len(content["tags"])-1]:
            pass
        else:
            tagsofnotes+=" "

    return render_template("readingnotes.html", content=content, idofnotes=notesname, markdownpart=contentmd, tagsofnotes=tagsofnotes)

@app.route("/input")
def inputmenu():
    return render_template("inputmenu.html")

@app.route("/input/<whichinput>")
def inputpages(whichinput, idofnotes=None, idofbookmarks=None):
    if whichinput=="notes":
        # open using idofnotes if not None.
        idofnotes = request.args.get("idofnotes")

        if idofnotes:
            with open(notescontent+str(idofnotes)+".json", "r") as f:
                content = json.loads(f.read())
            titleofnotes = content["title"]
            contentofnotes = content["content"].replace("<br>", "\n")
            tagsofnotes = content["tags"]
            tagslist = ""
            for i in tagsofnotes:
                tagslist+=i
                if i==tagslist[len(tagslist)-1]:
                    pass
                else:
                    tagslist+=" "
        else:
            titleofnotes = ""
            contentofnotes = ""
            tagslist = ""

        return render_template("inputnotes.html", titleofnotes=titleofnotes, contentofnotes=contentofnotes, tagsofnotes=tagslist)
    elif whichinput=="bookmarks":
        return render_template("inputbookmarks.html")
