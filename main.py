from flask import Flask, render_template

app = Flask(__name__)
menu = ["Download", "First app", "Contact us"]


@app.route('/')
def index():
    return render_template("index.html", title='Home')


@app.route('/about')
def about():
    return render_template("about.html", title="About", menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
