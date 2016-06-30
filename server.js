var fs = require('fs-extra');
var path = require('path');
var express = require('express');
var bodyParser = require('body-parser');
var request = require('request');
var app = express();
var util = require('util');
var formidable = require('formidable');
var http = require('http');
var PythonShell = require('python-shell');




app.set('port', (process.env.PORT || 3000));

app.use('/', express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

// Additional middleware which will set headers that we need on each request.
app.use(function(req, res, next) {
    // Set permissive CORS header - this allows this server to be used only as
    // an API server in conjunction with something like webpack-dev-server.
    res.setHeader('Access-Control-Allow-Origin', '*');

    // Disable caching so we'll always get the latest comments.
    res.setHeader('Cache-Control', 'no-cache');
    next();
});

app.post('/process', function(req, resp) {

    var form = new formidable.IncomingForm();
    form.parse(req, function (err, fields, files) {
        if (err) {
            console.error(err.message);
            return;
        }
        var data = "Hello from the Node writeFile method!";

        console.log(files['file']);

        resp.writeHead(200, {'content-type': 'text/plain'});
        resp.write('received upload:\n\n');
        resp.end(util.inspect({fields: fields, files: files}));
    });


    form.on('end', function(fields, files) {
       /* Temporary location of our uploaded file */
       var temp_path = this.openedFiles[0].path;
       /* The file name of the uploaded file */
       var file_name = this.openedFiles[0].name;
       /* Location where we want to copy the uploaded file */
       var new_location = './uploaded/';

       fs.copy(temp_path, new_location + file_name, function(err) {
           if (err) {
               console.error(err);
           } else {
               console.log("success!");
               var options = {
                 args: [new_location+file_name]
               };
               PythonShell.run('test.py', options, function (err) {
                 if (err) throw err;
                 console.log('finished');
               });
           }
       });
     });

    return;
});




app.listen(app.get('port'), function() {
  console.log('Server started: http://localhost:' + app.get('port') + '/');
});
