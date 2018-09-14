var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var bodyParser = require('body-parser');
var cors = require('cors');

app.use(cors())
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/', express.static(__dirname + '/'));
var port = process.env.PORT || 3000;

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});

app.post('/', function (req, res) {
  io.emit('chat message', req.body.Giroscopio);
  res.end();
});

io.on('connection', function (socket) {
  socket.on('chat message', function (msg) {
    io.emit('chat message', msg);
  });
});

//chamar esse metodo para classicar o movimento, passando os parametros conforme exemplo abaixo.
setInterval(
function () {

  //parametros para demostração  
  var params = "-15196,-0.913818359375,-548,-0.060791015625,1620,0.096923828125,-266,-266,49,0,-3049,-24,-5.70035711339,81.2437656066"
  
  var exec = require('child_process').exec;
  var child = exec('java -jar classificador\\Cownex\\dist\\Cownex.jar ' + params,
    function (error, stdout, stderr) {
      // res.send(stdout);
      io.emit('teste',stdout);
      if (error !== null) {
        console.log(error);
      }
    });
}, 3000);

http.listen(port, function () {
  console.log('listening on *:' + port);
});