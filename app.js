var express = require('express');
var app = express();
var dataInterface = require('./DataInterface.js');


// set the view engine to ejs
app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

// use res.render to load up an ejs view file

// index page
app.get('/', function(req, res) {
  res.render('pages/index');
});

// about page
app.get('/NoiseChart', function(req, res) {
  var now = Date.now();
    dataInterface.VolumesBetweenDates(now - 60*60*1000,now, function(data){
    res.render('pages/NoiseChart', {data: data});
    });
});

app.get('/NoiseChart/Day', function(req, res) {
  var now = Date.now();
  dataInterface.VolumesBetweenDates(now - 24*60*60*1000,now, function(data){
  res.render('pages/NoiseChart', {data: data});
  });
});

app.listen(80);
console.log('Server is listening on port 80');
