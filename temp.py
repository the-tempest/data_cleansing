from flask import Flask, request, render_template, url_for, jsonify, send_file, Response, make_response, send_from_directory, session, safe_join
from flask.sessions import SessionInterface
import os, subprocess
from datetime import datetime
import main

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploaded/'
app.config['OUTPUT_FOLDER'] = 'output/'
app.config['COOKIE LIST'] = {};

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
            now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            noExt, ext = os.path.splitext(f.filename);
            filename = os.path.join(app.config['UPLOAD_FOLDER'], noExt+now+ext)
            f.save(filename)
            main.execute(filename)
            outputFile = noExt+now+".txt"
            r = make_response(send_file(app.config['OUTPUT_FOLDER'] + outputFile), 200, {"file": outputFile} );
            #k = os.urandom(24);
            #app.config['COOKIE LIST'][]
            #r.set_cookie('username', k)
            return r;


    return "No files were uploaded";



@app.route('/download', methods=['GET'])
def download():
    filename = request.args['fn'];
    return send_from_directory(app.config['OUTPUT_FOLDER'],filename, as_attachment=True, attachment_filename="results.txt");


if __name__ == '__main__':
    app.run(debug=True)
