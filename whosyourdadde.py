from flask import *
from flask import render_template
from whosyourdad import whosyourdad
from waitress import serve

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/', methods= ["GET", "POST"])
def getdad():
    if request.method == 'POST':
        person = request.form.get('name')
        if person:
            dad = whosyourdad(person)
            return jsonify({'html':dad})
        else:
            return jsonify('')

    return render_template('index.html')

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80)