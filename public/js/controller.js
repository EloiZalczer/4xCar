var mousedown = false;
var canvas, ctx;
var height, width;
var command = {direction: 0, speed: 0};
var periodicSend;
var socket;
var connected = false;
var running = false;
var recording = false;

window.onload = function(){

	canvas = document.getElementById('controller');
	height = canvas.height;
	width = canvas.width;

	ctx = canvas.getContext('2d');

	initBall();
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
			prev_direction = command.direction;
			prev_speed = command.speed;
			command.direction = - Math.round(coord.x*(60/width) - 30);
			command.speed = Math.round(30 - coord.y*(30/height));
			displayBall(coord);
			if(running && (prev_direction != command.direction || prev_speed != command.speed)){
				sendData();
			}
		}
	}

	// Support for mobile devices

	canvas.addEventListener('touchstart', function(evt){
		evt.preventDefault()
		mousedown = true;
	})

	document.body.addEventListener('touchend', function(evt){
		evt.preventDefault()
		mousedown = false;
		resetBall();
	})

	canvas.addEventListener('touchmove', function(evt){
		if(mousedown){
			var touches = evt.changedTouches;
			coord = getTouchPos(evt)
			console.log(coord)
			prev_direction = command.direction;
			prev_speed = command.speed;
			command.direction = - Math.round(coord.x*(60/width) - 30);
			command.speed = Math.round(30 - coord.y*(30/height));
			displayBall(coord);
			if(running && (prev_direction != command.direction || prev_speed != command.speed)){
				sendData();
			}
		}
	})
}

function connect(){
	socket = io.connect("http://192.168.43.45:3000/");
	socket.on("connect_failed", () => {alert("Connection failed");})
	socket.on("connect", function(){ 
		connected = true;
	});
}

function setRunButtonTextAndColor(value, color){
	var button = document.getElementById("stopstart")
	button.style.background = color;
	var text = button.firstChild;
	text.data = value;
}

function setRecordButtonTextAndColor(value, color){
	var button = document.getElementById("stopstart_record")
	button.style.background = color;
	var text = button.firstChild;
	text.data = value;
}

function displayCurrentSpeedAndDirection(speed, direction){
	document.getElementById("speed_value").innerHTML = speed;
	document.getElementById("direction_value").innerHTML = direction;
} 

function stopstart(){
	if(running){
		sendStop();
		setRunButtonTextAndColor("Start", '#1CB841');
		running = false;
	}
	else{
		sendStart();
		setRunButtonTextAndColor("Stop", '#CA3C3C');
		running = true;
	}
}

function stopstart_record(){
	if(recording){
		sendStopRecording();
		setRecordButtonTextAndColor("Start recording", '#1CB841');
		recording = false;
	}
	else{
		sendStartRecording();
		setRecordButtonTextAndColor("Stop recording", '#CA3C3C');
		recording = true;
	}
}

function sendStartRecording(){
	if(connected){
		console.log("Sending start recording command");
		socket.emit('start_record');
	}
}

function sendStopRecording(){
	if(connected){
		console.log("Sending stop recording command");
		socket.emit('stop_record');
	}
}

function sendStart(){
	if(connected){
		console.log("Sending start command");
		socket.emit('start');
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
	socket.emit('command', command);
}

function resetBall(){
	command.direction = 0;
	command.speed = 0;
	sendData();
	displayBall({x: width/2, y: height});
}

function initBall(){
	command.direction = 0;
	command.speed = 0;
	displayBall({x: width/2, y: height});
}

function displayBall(coord){
	ctx.fillStyle = "#B0B0B0"
	ctx.fillRect(0, 0, width, height)
	ctx.fillStyle = "#808080"
	ctx.beginPath();
	ctx.arc(coord.x, coord.y, 50, 0, 2*Math.PI);
	ctx.fill();
	ctx.stroke();
	displayCurrentSpeedAndDirection(command.speed, command.direction);
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

function getTouchPos(evt){

	touches = evt.changedTouches

	var rect = canvas.getBoundingClientRect(), // abs. size of element
	  scaleX = canvas.width / rect.width,    // relationship bitmap vs. element for X
	  scaleY = canvas.height / rect.height;  // relationship bitmap vs. element for Y

	  return {
	    x: (touches[0].pageX - rect.left) * scaleX,   // scale mouse coordinates after they have
	    y: (touches[0].pageY - rect.top) * scaleY     // been adjusted to be relative to element
	  }
}