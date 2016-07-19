from flask import Flask, request, render_template, url_for, jsonify, send_file, Response, make_response
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
            noExt, ext = os.path.splitext(f.filename);
            filename = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(filename)
            main.execute(filename)
            return "output/"+noExt+"_c.txt";


    return "No files were uploaded";




@app.route('/download', methods=['GET'])
def download():
    filename = request.args['fn'];
    return send_file(filename, as_attachment=True);

if __name__ == '__main__':
    app.run(debug=True)
