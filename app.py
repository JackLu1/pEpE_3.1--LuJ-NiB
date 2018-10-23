from flask import Flask, render_template, redirect, url_for, request
from util import storyreturn, storyedit

app = Flask(__name__);

@app.route("/")
def root():
    '''If user not logged in, redirect to landing page. Otherwise redirect to welcome page'''
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
    return render_template("welcome.html")

@app.route("/logout", methods=["POST"])
def logout():
    '''ends session, redirect back to landing page'''
    return redirect(url_for("landing"))

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
        return redirect(url_for("welcome"))


@app.route("/search")
def search():
	'''search results page'''
	return render_template("library.html", stories=storyreturn.search(request.args["search"]))

app.debug = True
app.run()
