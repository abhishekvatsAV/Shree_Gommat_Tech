var express = require("express");  
var app = express();  

app.use(express.static("public"));

app.get("/", function(req, res){
	res.sendFile(__dirname + "/public/html/index.html");
})

app.get("/index2", function(req, res){
	res.sendFile(__dirname + "/public/html/index2.html");
})

app.get("/index3", function(req, res){
	res.sendFile(__dirname + "/public/html/index3.html");
})

app.get("/index", function(req, res){
	res.sendFile(__dirname + "/public/html/index.html");
})



app.listen(8080);