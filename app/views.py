from app import app 

from flask import Flask, render_template
from fp import *

# Variable Declear for files that can be change files are dump in notice folder
historyFile = "history.txt"
introductionFile = "introduction.txt"
objectiveFile = "objective.txt"


@app.route('/')
@app.route('/index')
def index():
    return render_template("public/index.html")



@app.route('/contact')
def contact():
    return render_template("public/contact.html")


@app.route('/about')
def about():
    content = introduction(introductionFile)
    return render_template("public/about.html", content=content)

@app.route('/objective')
def objective():
    content = introduction(objectiveFile)
    return render_template("public/objective.html", content=content)



@app.route('/notice')
def notice():
    pdflist=noticefile()
    return render_template("public/notice.html", pdflist=pdflist)


@app.route('/info')
def info():
    content = introduction(historyFile)
    return render_template("public/info.html", content=content)


@app.route('/test')
def test():
    return render_template("public/test.html")
