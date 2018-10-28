from flask import Flask, render_template, redirect, url_for, request, session
from util import storyreturn, storyedit
from util import usrctrl 
import os

#TODO add flashing for failed login
#TODO session checking

app = Flask(__name__);

# temporary hard coded user
usr = ''
pw = ''
# generate secret key
app.secret_key = os.urandom(32)


@app.route("/")
def root():
    '''redirect to welcome page if user logged in, otherwise to landing page'''
    if usr in session:
        return redirect(url_for("welcome"))
    return redirect(url_for("landing"))


@app.route("/login", methods=["POST"])
def auth():
    '''logs in the user'''
    usr = request.form["user"]
    pw = request.form["pass"]

    if usr == '' or pw == '':
        return redirect(url_for("landing"))
    # returns boolean value for success of login
    if not usrctrl.login_check(usr, pw):
        return redirect(url_for('landing'))

    #logs in the user, redirect to welcome page
    session['username'] = usr
    session['password'] = pw
    return redirect(url_for('welcome'))


@app.route("/create")
def new():
    '''Creates new user in database'''
    print("CREATE NEW USEREKLJRELKRJELKRJWELKJ")
    return render_template("newUser.html") 


@app.route("/logout", methods=["POST"])
def logout():
    '''ends session, redirect back to landing page'''
    print(session)
    session.pop('username')
    session.pop('password')
    return redirect(url_for("landing"))


@app.route("/splash")
def landing():
    '''renders splash (landing) page'''
    return render_template("splash.html")


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


@app.route("/add", methods=["GET", "POST"])
def add():
    if "addition" in request.form.keys() and "title" in request.form.keys():
        if request.form["addition"] == "" or request.form["title"] == "":
            return render_template("addstory.html")
        else:
            storyedit.add(request.form["addition"], request.form["title"])
            return render_template("library.html", stories=storyreturn.all_stories())
    else:
        return render_template("addstory.html")


app.debug = True
app.run()
