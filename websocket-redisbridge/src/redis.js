//redis sub channels :
var redis = require('redis');
const redis_host = "redis"
var host = "redis://" + redis_host + ":6379";
var redisclient = redis.createClient(host);
redisclient.select(5);
var redis_sub = redis.createClient(host)




let previousConversions = redisclient.get('conversion.*')
console.log(previousConversions)
//SOCKETIO

var io = require('socket.io')(3001);

io.on('connection', function (socket) {
  io.emit('this', { will: 'be received by everyone' });

  redis_sub.on("message", function (channel, message) {
    console.log("pdf update recieved" + channel + ": " + message);
    redisclient.hmget(channel) //stored key is the same name as the channel
    io.emit('message', { message })
    
  
  })
  socket.on('message', function (from, msg) {
    //console.log('I received a private message by ', from);
    var tbl = from.split(":")
    redis_sub.subscribe(`conversion.${pdfname}`)

    
  });


  
  socket.on('disconnect', function () {
    io.emit('user disconnected');
  });

  

});

