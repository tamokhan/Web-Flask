from app import app 

from flask import Flask, render_template, request, redirect, send_from_directory, session, flash, url_for
from werkzeug.utils import secure_filename
import os
from werkzeug.exceptions import RequestEntityTooLarge
import sys

# The app folder selection
sys_dir = sys.path[0]
# The upload folder specification
# Bellow is for Windows:
# app.config['PHOTO_UPLOAD'] = f'{sys_dir}\\photoupload\\'
# app.config['NOTICE_FOLDER'] = f'{sys_dir}\\app\\static\\notice\\'
# Bellow is for Linux:
app.config['PHOTO_UPLOAD'] = f'{sys_dir}/photoupload/'
app.config['NOTICE_FOLDER'] = f'{sys_dir}/app/static/notice/'
# Max Upload file size
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['ALLOW_EXTENTION_NOTICE'] = ['.pdf']
app.config['ALLOW_EXTENTION_PAGEFILE'] = ['.txt']
app.secret_key = "jsdljaljdlfjkslkgjioerhiofjkvnkrig"

@app.route('/login', methods=["POST","GET"])
def login():
	if request.method == "POST":
		userid = request.form["user"]
		userpass = request.form["password"]
		# print(type(userid))
		if userid !="":
			if (userid=='kamrul@telnet.com.bd' and userpass=='kamrul321'):
				session["userid"] = userid
				print(f"Login: {userid}")
				return redirect(url_for("admin_dashboard"))
			else:
				msg = "Wrong: User-ID or Password"
				flash(f"{msg}","info")
				return redirect("/login")
		else:
			msg = "Ener blank User-ID"
			flash(f"{msg}")
			return redirect("/admin/login.html")

	else:
		return render_template("/admin/login.html")

# Admin Dash Board Main Page    
@app.route('/admin/dashboard')
@app.route('/admin/panel')
def admin_dashboard():
    if "userid" in session:
        userid = session["userid"]  
        # Notice File List
        noticefiles = os.listdir(app.config['NOTICE_FOLDER'])
        notices = []
        for noticefile in noticefiles:
            extention = os.path.splitext(noticefile)[1]
            if extention in app.config['ALLOW_EXTENTION_NOTICE']:
                notices.append(noticefile)
        # Notice shored by date of modificaion
        notices.sort(key=lambda x: os.path.getmtime('{}{}'.format(app.config['NOTICE_FOLDER'],x)), reverse=True)
        return render_template("/admin/dashboard.html", notices=notices, userid=userid)
    else:
        return redirect("/login")

# Notice File Upload
@app.route('/admin/uploadnoticefile', methods=['POST'])
def uploadnoticefile():
    if "userid" in session:  
        try:
            nfile = request.files["nfile"]
            # splittext the file name by . in list data
            extention = os.path.splitext(nfile.filename)[1]
            # print(extention)
            # If any file select then only execute
            if nfile:
                if extention not in app.config['ALLOW_EXTENTION_NOTICE']:
                    return 'This is not proper extention file'
                # secure_filename upload file (file name not allow space)\
                # For windows after folder \\ & in linux afterfolder / use
                # file.save(f'noticeupload\\{secure_filename(file.filename)}')
                else:
                    nfile.save(os.path.join(app.config['NOTICE_FOLDER'], secure_filename(nfile.filename)))
        except RequestEntityTooLarge:
            return 'The file is over 10 MB file'
        return redirect('/admin/dashboard')
    else:
        return redirect("/login")

# Delete Notice File
@app.route('/admin/deletenoticefile/<filename>', methods=['GET'])
def deletenoticefile(filename):
    if "userid" in session:
        files = os.listdir(app.config['NOTICE_FOLDER'])
        for file in files:
            if file == filename:
                print(file)
                path = os.path.join(app.config['NOTICE_FOLDER'], filename)
                os.remove(path)
        return redirect('/admin/dashboard')
    else:
        return redirect("/login")

# Pages File Upload
@app.route('/admin/pagefile', methods=['POST'])
def pagefileupload():
    if "userid" in session:
        try:
            pagefile = request.files["pagefile"]
            # splittext the file name by . in list data
            extention = os.path.splitext(pagefile.filename)[1]
            # print(extention)
            # If any file select then only execute
            if pagefile:
                pagefilename = os.path.splitext(pagefile.filename)[0]
                if(pagefilename=='history' or pagefilename=='introduction' or pagefilename=='objective'):
                    if extention not in app.config['ALLOW_EXTENTION_PAGEFILE']:
                        return 'This is not proper extention file'
                    # secure_filename upload file (file name not allow space)\
                    # For windows after folder \\ & in linux afterfolder / use
                    # file.save(f'noticeupload\\{secure_filename(file.filename)}')
                    else:
                        pagefile.save(os.path.join(app.config['NOTICE_FOLDER'], secure_filename(pagefile.filename)))
                else:
                    return 'Upload file name did not math with Page file name.'
        except RequestEntityTooLarge:
            return 'The file is over 10 MB file'
        return redirect('/admin/dashboard')
    else:
        return redirect("/login")

# Logout Sytem
@app.route('/logout')
def logout():
	if "userid" in session:
		userid = session["userid"]
		session.pop('userid',None)
		flash(f"Log-out: {userid}","info")
		return redirect("/login")
	else:
		return redirect("/login")

