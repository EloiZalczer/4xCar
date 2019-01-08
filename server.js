var express=require('express'),
    app = express(),
    port = process.env.PORT || 3000;

var bodyParser = require('body-parser')

app.set('views', __dirname + '/public');
app.engine('html', require('ejs').renderFile);
app.use(express.static(__dirname + '/public'));

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }));
 
// parse application/json
app.use(bodyParser.json());

app.get('/', function(req, res){
  res.render('views/main.html')
});

app.use(function(req, res) {
    res.status(404).send({url: req.originalUrl +  ' not found'})
});

  // Which port to listen on
app.set('port', process.env.PORT || 3000);

// Start listening for HTTP requests
var server = app.listen(app.get('port'), function() {
  var host = server.address().address;
  var port = server.address().port;

  console.log('Listening at http://%s:%s', host, port);
});

var io = require('socket.io').listen(server);

io.sockets.on('connection', function(socket){
  console.log("Client connected");

  socket.on('command', function(command){
    socket.broadcast.emit('command', command);
  });
});