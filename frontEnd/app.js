const express = require('express'); 
const sender = require('./sender');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

app.listen(5000, function() {
	console.log("Server is configured on port 5000"); 
});

app.get("/", function(req, res) {
	res.send("Hello World" + "\n");
});

app.get("/register", function(req, res) {
	res.sendFile(__dirname + "/html/register.html");
})

app.post("/", function(req, res) {
//	sender.send()
	if (req.body.postType === "register") {
		let firstName = req.body.firstName;
		let lastName = req.body.lastName;
		let email = req.body.email;
		let password = req.body.password;
		console.log("Hi " + firstName + " " + lastName+ " your email is " + email);
		console.log(req.body);
	} else {
		console.log("Registration failed");
	}
});

