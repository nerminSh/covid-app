from flask import Flask, render_template
import app2 as mapa
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/map/')
def map():
    return mapa.map._repr_html_()

if __name__ == "__main__":
    app.run(debug=True)