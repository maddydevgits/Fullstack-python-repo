from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/home")
def home1():
    return render_template("index1.html")


if __name__ == '__main__':
	app.run(debug=True)
