
var mousedown = false;
var canvas, ctx;
var height, width;
var command = {direction: 0, speed: 0};
var periodicSend;
var socket;
var connected=false;

window.onload = function(){

	canvas = document.getElementById('controller');
	height = canvas.height;
	width = canvas.width;

	ctx = canvas.getContext('2d');

	resetBall();
	connect();

	canvas.onmousedown = function(){
		mousedown = true;
	}

	document.onmouseup = function(){
		mousedown = false;
		resetBall();
	}

	canvas.onmousemove = function(evt){
		if(mousedown){
			coord = getMousePos(evt);
			command.direction = coord.x*(60/width) - 30
			command.speed = 30 - coord.y*(30/height)
			displayBall(coord);
		}
	}
}

function connect(){
	socket = io.connect("http://localhost:3000/");
	socket.on("connect_failed", () => {alert("Connection failed");})
	socket.on("connect", function(){
		connected = true;
		periodicSend = setInterval(sendData, 20);
	});
}

function sendData(){
	console.log("Sending data : "+command);
	socket.emit('command', command);
}

function resetBall(){
	displayBall({x: width/2, y: height});
	command.direction = 0;
	command.speed = 0;
}

function displayBall(coord){
	ctx.fillStyle = "#808080"
	ctx.fillRect(0, 0, width, height)
	ctx.beginPath();
	ctx.arc(coord.x, coord.y, 50, 0, 2*Math.PI);
	ctx.stroke();
}

function  getMousePos(evt) {
  var rect = canvas.getBoundingClientRect(), // abs. size of element
      scaleX = canvas.width / rect.width,    // relationship bitmap vs. element for X
      scaleY = canvas.height / rect.height;  // relationship bitmap vs. element for Y

  return {
    x: (evt.clientX - rect.left) * scaleX,   // scale mouse coordinates after they have
    y: (evt.clientY - rect.top) * scaleY     // been adjusted to be relative to element
  }
}