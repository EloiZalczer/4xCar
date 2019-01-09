
var mousedown = false;
var canvas, ctx;
var height, width;
var command = {direction: 0, speed: 0};
var periodicSend;
var socket;
var connected = false;
var running = false;

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
	});
}

function setButtonTextAndColor(value, color){
	var button = document.getElementById("stopstart")
	button.style.background = color;
	var text = button.firstChild;
	text.data = value;
}

function displayCurrentSpeedAndDirection(speed, direction){
	document.getElementById("speed_value").innerHTML = speed.toPrecision(5);
	document.getElementById("direction_value").innerHTML = direction.toPrecision(5);
} 

function stopstart(){
	if(running){
		sendStop();
		setButtonTextAndColor("Start", '#1CB841');
		running = false;
	}
	else{
		sendStart();
		setButtonTextAndColor("Stop", '#CA3C3C');
		running = true;
	}
}

function sendStart(){
	if(connected){
		console.log("Sending start command");
		socket.emit('start');
		periodicSend = setInterval(sendData, 20);
	}
}

function sendStop(){
	if(connected){
		console.log("Sending stop command");
		socket.emit('stop');
		clearInterval(periodicSend);
	}
}

function sendMaxSpeed(){
	max_speed = document.getElementById('max_speed').value;
	console.log("Setting max speed : "+max_speed);
	socket.emit('max_speed', max_speed);
}

function sendData(){
	console.log("Sending data : "+command);
	displayCurrentSpeedAndDirection(command.speed, command.direction);
	socket.emit('command', command);
}

function resetBall(){
	displayBall({x: width/2, y: height});
	command.direction = 0;
	command.speed = 0;
}

function displayBall(coord){
	ctx.fillStyle = "#B0B0B0"
	ctx.fillRect(0, 0, width, height)
	ctx.fillStyle = "#808080"
	ctx.beginPath();
	ctx.arc(coord.x, coord.y, 50, 0, 2*Math.PI);
	ctx.fill();
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