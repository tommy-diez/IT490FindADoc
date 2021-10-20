#!/usr/bin/env node

const express = require('express'); 
const sender = require('./sender');
const bodyParser = require('body-parser');
const handlebars = require('express-handlebars');
const app = express();
const consumer = require('./consumer');

app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'hbs');

app.engine('hbs', handlebars({
	layoutsDir: __dirname + "/html/views/layouts",
	extname: 'hbs',
	partialsDir: __dirname + "/html/views/partials"
}));

app.use(express.static('css'));

app.listen(5000, function() {
	console.log("Server is configured on port 5000"); 
});

app.get("/", function(req, res) {
	res.render( __dirname + '/html/views/main', {layout: 'index'});
});

app.get("/register", function(req, res) {
	res.render( __dirname + '/html/views/register', {layout: 'index'});
})

app.get("/login", function(req, res) {
	res.render( __dirname + '/html/views/main', {layout: 'index'});
})

app.post("/", function(req, res) {

	if (req.body.postType === "register") {

		let firstName = req.body.firstName;
		let lastName = req.body.lastName;
		let email = req.body.email;
		let password = req.body.password;
		let confirmPassword = req.body.confirmPassword;
		let insuranceId = req.body.insuranceId;

		if(confirmPassword !== password) {
			console.log("passwords do not match");
			res.render(__dirname + '/html/views/register', {layout: 'index', didntMatch: true});

		} else {

			let newUser = {
				firstName: firstName,
				lastName: lastName,
				email: email,
				password: password,
				insuranceId: insuranceId
			}

			const payloadAsString = JSON.stringify(newUser);
			sender.send(payloadAsString);
			if(consumer.consume()) {
				res.send("Account created");
			}
		}
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
})

