#!/usr/bin/env node

const express = require('express'); 
const sender = require('./sender');
const bodyParser = require('body-parser');
const handlebars = require('express-handlebars');
const app = express();
const amqp = require("amqplib");
let connection, channel, data;

app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'hbs');

app.engine('hbs', handlebars({
	layoutsDir: __dirname + "/html/views/layouts",
	extname: 'hbs',
	partialsDir: __dirname + "/html/views/partials"
}));

app.use(express.static('css'));

async function connect() {
	try {
		const server = "amqp://findadoc:Findadoc!@172.26.169.103";
		connection = await amqp.connect(server);
		channel = await connection.createChannel()
		const QUEUE = "beTOfe";
		//await channel.assertQueue(QUEUE);
		channel.consume(QUEUE, (msg) => {
			console.log(msg.content.toString());
			data = msg.content;
			//channel.ack(msg);
		}, {
			noAck: true
		});
	} catch (err) {
		console.log(err.toString());
	}
	return data;
}

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

app.get("/landing", function(req, res) {
	connect().then((data)=> {
		res.render(__dirname + "/html/views/landing", {layout: 'index'});
	})
})

app.post("/", function(req, res) {

	if (req.body.postType === "register") {

		let firstName = req.body.firstName;
		let lastName = req.body.lastName;
		let email = req.body.email;
		let password = req.body.password;
		let confirmPassword = req.body.confirmPassword;
		let policy = req.body.policy;
		let process = 1;

		if(confirmPassword !== password) {
			console.log("Passwords do not match");
			res.render(__dirname + '/html/views/register', {layout: 'index', didntMatch: true});

		} else {

			let newUser = {
				firstName: firstName,
				lastName: lastName,
				email: email,
				password: password,
				insuranceId: policy,
				case: process
			}

			const payloadAsString = JSON.stringify(newUser);
			sender.send(payloadAsString);
			connect().then(() => {
				res.render(__dirname + "/html/views/main", {layout: 'index'});
			})
		}
	}

	if(req.body.postType === "login") {

		let email = req.body.email;
		let password = req.body.password;
		let process = 2;

		let login = {
			email: email,
			password: password,
			case: process
		}

		const payloadAsString = JSON.stringify(login);
		sender.send(payloadAsString);
		//res.render(__dirname + "/html/views/landing", {layout: 'index'});
		connect().then(()=> {
            /*
			let landing = {
				case: 3
			}
			let payloadAsString = JSON.stringify(landing);
			sender.send(payloadAsString);

             */
			res.render(__dirname + "/html/views/landing", {layout: 'index'});

		})
	}

	if(req.body.postType === "case3") {

		let specialization = req.body.specialization;
		let insuranceId = 1;

		let doctors = {
			specialty: specialization,
			case: 3,
			insuranceId: insuranceId
		}

		let payloadAsString = JSON.stringify(doctors);
		sender.send(payloadAsString);
		connect().then( (data) => {
			console.log(data);
	})

	}

});

