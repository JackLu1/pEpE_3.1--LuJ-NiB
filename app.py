from flask import Flask, render_template, redirect, url_for

app = Flask(__name__);

@app.route("/")
def root():
	return redirect(url_for("landing"))

@app.route("/splash")
def landing():
	return render_template("base.html")

app.run()