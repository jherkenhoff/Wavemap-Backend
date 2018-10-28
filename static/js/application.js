
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('device_info', function(msg){
        console.log("Got device info: " + msg);
    });

    socket.emit("get_device_info");
});
