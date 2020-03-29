from flask import Flask, render_template, request
import app2 as mapa
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/stayAtHome')
def forma():
    return render_template("forma.html")

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        name = request.form["firstName"]
        rolls = request.form["rolls"]
        soc = request.form["socOpt"]
        rolls = int(rolls)
        if name.capitalize() in ("Nedim", "Armen", "Harun", "Alen", "Adis", "Amir", "Ibrahim", "Mugdim", "Ahmed", "Ekrem", "Ibro", "Anes", "Dzenan"):
            perc = name.capitalize() + "e ti si jedan veliki covIDIOT heheh salim se\n btw kupi jos toalet papira. Selam"
        elif rolls > 30 and soc == "socNo":
            perc = "You are definitely a covIDIOT."
        elif rolls <= 30 and soc == "socYes":
            perc = "Good job, you are not a covIDIOT"
        else:
            perc = "You are almost a covIDIOT, let's say you're halfway there"

        return render_template("result.html", firstname = name.capitalize(), perc = perc)

 
@app.route('/map/')
def map():
    return mapa.map._repr_html_()

if __name__ == "__main__":
    app.run(debug=True)