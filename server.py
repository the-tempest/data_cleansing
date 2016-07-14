from flask import Flask, request, render_template, url_for, jsonify
from datetime import datetime
import os, subprocess
import main

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded/'

@app.route('/')
def index():
    return app.send_static_file('index.html')


#@app.route('/profile/<name>')
#def profile(name):
#    return render_template("profile.html", namePassed=name); # passes name as arg to html template

@app.route('/process', methods=['POST'])
def process():
    for i in range(len(request.files)):
        f = request.files['file'+str(i)]
        if f:
            now = datetime.now()
            filename = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(filename)
            print filename
            main.execute(filename)

    return jsonify({"success":True})

#@app.p

if __name__ == '__main__':
    app.run(debug=True)
