#!/usr/bin/env node

const express = require('express'); 
const sender = require('./sender');
const bodyParser = require('body-parser');
const handlebars = require('express-handlebars');
const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'hbs');

app.engine('hbs', handlebars({
	layoutsDir: __dirname + "/html/views/layouts",
	extname: 'hbs'
}));

app.use(express.static('css'));

app.listen(5000, function() {
	console.log("Server is configured on port 5000"); 
});

app.get("/", function(req, res) {
	res.sendFile(__dirname + "/html/login.html");
});

app.get("/register", function(req, res) {
	res.sendFile(__dirname + "/html/register.html");
})

app.get("/login", function(req, res) {
	res.sendFile(__dirname + "/html/login.html");
})

app.post("/", function(req, res) {

	if (req.body.postType === "register") {

		let firstName = req.body.firstName;
		let lastName = req.body.lastName;
		let email = req.body.email;
		let password = req.body.password;

		let newUser = {
			firstName: firstName,
			lastName: lastName,
			email: email,
			password: password,
		}

		const payloadAsString = JSON.stringify(newUser);
		sender.send(payloadAsString);

	}

	if(req.body.postType === "login") {

		let email = req.body.email;
		let password = req.body.password;

		let login = {
			email: email,
			password: password
		}

		const payloadAsString = JSON.stringify(login);
		sender.send(payloadAsString);

	}

});

