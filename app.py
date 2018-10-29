from flask import Flask, render_template, redirect, url_for, request, session, flash
from util import storyreturn, storyedit
from util import usrctrl 
import os

#TODO add flashing for failed login
#TODO check stories for prev edit

app = Flask(__name__);

# generate secret key
app.secret_key = os.urandom(32)

userid = None

@app.route("/")
def root():
    '''redirect to welcome page if user logged in, otherwise to landing page'''
    if 'user' in session:
        return redirect(url_for("welcome"))
    return redirect(url_for("landing"))


@app.route("/login", methods=["POST"])
def auth():
    '''logs in the user'''
    usr = request.form["user"]
    pw = request.form["pass"]

    if usr == '' or pw == '':
        flash('Unsuccessful login, try again')
        return redirect(url_for("landing"))
    # returns boolean value for success of login
    if not usrctrl.login_check(usr, pw):
        flash('Unsuccessful login, try again')
        return redirect(url_for('landing'))

    #logs in the user, redirect to welcome page
    session['user'] = usr
    session['pass'] = pw
    global userid
    userid = usrctrl.getID(usr)
    return redirect(url_for('welcome'))


@app.route("/create")
def new():
    '''redirects from splash if creating new user'''
    return render_template("newUser.html") 

@app.route("/make_account", methods=["POST"])
def make_user():
    '''Creates new user in database'''
    usr = request.form["user"]
    pw = request.form["pass"]
    check = request.form["confirm"]
    if pw != check:
        flash('Passwords do not match.')
        return redirect(url_for('new'))
    usrctrl.new_user(usr, pw) 
    return redirect(url_for('landing'))

@app.route("/logout", methods=["POST"])
def logout():
    '''ends session, redirect back to landing page'''
    session.pop('user')
    session.pop('pass')
    return redirect(url_for("landing"))


@app.route("/splash")
def landing():
    '''renders splash (landing) page'''
    return render_template("splash.html")


@app.route("/welcome")
def welcome():
    '''welcomes user'''
    if 'user' not in session:
        return redirect(url_for('landing'))
    return render_template("welcome.html", name=session['user'])


@app.route("/browse")
def library():
    '''renders a list of stories'''
    if 'user' not in session:
        return redirect(url_for('landing'))
    a = storyreturn.all_stories()
    return render_template("library.html", name=session['user'], stories=storyreturn.all_stories())

@app.route("/edit", methods=["GET", "POST"])
def edit():
    '''edit page for story'''
    if 'user' not in session:
        return redirect(url_for('landing'))
    sID = int(request.args["storylink"])
    
    # If user has already edited, display full story
    if usrctrl.check_edited(userid, sID):
        return redirect(url_for('show', sID=sID))

    story = storyreturn.get(sID)
    return render_template("storybase.html", title=story[1], name=session['user'], content=story[2], storyID=story[0])

@app.route('/insert', methods=["GET", "POST"])
def insert_story():
    storyedit.edit(int(request.form['submit']), request.form["addition"], userid)
    return render_template("library.html", name=session['user'], stories=storyreturn.all_stories())


@app.route("/search")
def search():
    '''search results page'''
    if 'user' not in session:
        return redirect(url_for('landing'))
    s = storyreturn.search(request.args["search"])
    if len(s) == 0:
        return render_template("search.html", name=session['user'], e=True, stories=[])
    else:
        return render_template("search.html", name=session['user'], e=False, stories=storyreturn.search(request.args["search"]))

@app.route("/display")
def show():
    '''Displays full story'''
    if 'user' not in session:
        return redirect(url_for('landing'))
    sID = request.args['sID']
    info = storyreturn.whole_story(sID)
    title = info.pop(0)
    return render_template("show.html", story_title=title, name=session["user"], content=info)

@app.route("/add", methods=["GET", "POST"])
def add():
    if 'user' not in session:
        return redirect(url_for('landing'))
    if "addition" in request.form.keys() and "title" in request.form.keys():
        if request.form["addition"] == "" or request.form["title"] == "":
            flash("Please fill in all fields")
            return render_template("addstory.html", name=session['user'])
        else:
            storyedit.add(request.form["addition"], request.form["title"], userid)
            return render_template("library.html", name=session['user'], stories=storyreturn.all_stories())
    else:
        return render_template("addstory.html", name=session['user'])


app.debug = True
app.run()
