from flask import Flask, render_template, redirect, url_for

app = Flask(__name__);

@app.route("/")
def root():
	return redirect(url_for("landing"))

@app.route("/splash")
def landing():
	return render_template("splash.html")

@app.route("/login", methods=["POST"])
def redir():
    return redirect(url_for("welcome"))

@app.route("/welcome")
def welcome():
    return render_template("welcome.html", name='bni')

@app.route("/logout", methods=["POST"])
def logout():
	return redirect(url_for("landing"))

@app.route("/browse")
def library():
	return render_template("library.html", stories=[])

@app.route("/edit")
def edit():
	return render_template("storybase.html", title="", content="")

app.debug = True
app.run()
