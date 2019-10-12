
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
app.config["DEBUG"] = True

comments = []

@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'GET':
        return render_template("main_page.html", comments=comments)

    else:
        comments.append(request.form["contents"])
        return redirect(url_for('index'))

