from flask import Flask, render_template, redirect, url_for, request, session
from util import storyreturn, storyedit
from util import usrctrl as User
import os

#TODO add flashing for failed login

app = Flask(__name__);

# temporary hard coded user
usr = 'jlu'
pw = '123'
# generate secret key
app.secret_key = os.urandom(32)

@app.route("/")
def root():
    '''If user not logged in, redirect to landing page. Otherwise redirect to welcome page'''
    if usr in session:
        return redirect(url_for("welcome"))
    return redirect(url_for("landing"))

@app.route("/login", methods=["POST"])
def auth():
    '''logs in the user'''
    check_usr = request.form["user"]
    check_pw = request.form["pass"]

    # checks correct password
    if check_pw != pw or check_usr != usr:
        return redirect(url_for('root'))

    #logs in the user, redirect to welcome page
    session[usr] = pw
    return redirect(url_for('welcome'))

@app.route("/logout", methods=["POST"])
def logout():
    '''ends session, redirect back to landing page'''
    session.pop(usr)
    return redirect(url_for("landing"))

@app.route("/splash")
def landing():
    '''renders splash (landing) page'''
    return render_template("splash.html")

@app.route("/login", methods=["POST"])
def redir():
    '''redirect to welcome page when login successful'''
    return redirect(url_for("welcome"))

@app.route("/welcome")
def welcome():
    '''welcomes user'''
    return render_template("welcome.html", name=usr)


@app.route("/browse")
def library():
    '''renders a list of stories'''
    return render_template("library.html", stories=storyreturn.all_stories())

@app.route("/edit", methods=["GET", "POST"])
def edit():
    '''edit page for story'''
    if "addition" not in list(request.form.keys()):
        sID = int(request.args["storylink"])
        story = storyreturn.get(sID)
        return render_template("storybase.html", title=story[1], content=story[2], storyID=sID)
    else:
        storyedit.edit(int(request.form["storylink"]), request.form["addition"])
        return render_template("library.html", stories=storyreturn.all_stories())


@app.route("/search")
def search():
    '''search results page'''
    s = storyreturn.search(request.args["search"])
    if len(s) == 0:
        return render_template("search.html", e=True, stories=[])
    else:
        return render_template("search.html", e=False, stories=storyreturn.search(request.args["search"]))

@app.route("/add")
def add():
    if "addition" in request.form.keys() and "title" in request.form.keys():
        if request.form["addition"] == "" || request.form["title"] == "":
            return render_template("addstory.html")
        else:
            storyedit.add(request.form["addition"], request.form["title"])
            return render_template("library.html", stories=storyreturn.all_stories())
    else:
        return render_template("addstory.html")

app.debug = True
app.run()
