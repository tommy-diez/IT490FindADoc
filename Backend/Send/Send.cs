using System;
using RabbitMQ.Client;
using System.Text;

using Newtonsoft.Json;
using System.Collections.Generic;
using RabbitMQ.Client.Events;

class Send
{
    public static void Main()
    {
        // Test case will send "Hello World!" to postgres
        Test();
        
        /*
        var factory = new ConnectionFactory() { HostName = "172.26.169.103", UserName = "admin", Password = "Luftwaffe1" };
        //var factory = GetConnection("172.26.169.103", "admin", "Luftwaffe1");
        using(var connection = factory.CreateConnection())
        using(var channel = connection.CreateModel())
        {
            var registerInfo = ReceiveFromFrontend(channel);
            string email = registerInfo.TryGetValue("email", out value);
            string message = "SELECT * FROM `users` WHERE email=`" + email + "`";
            //string message = "SHOW max_connections;";
            var body = Encoding.UTF8.GetBytes(message);

            channel.BasicPublish(exchange: "", routingKey: "c#backendTOpostgresql", basicProperties: null, body: body);
            Console.WriteLine(" [x] Sent {0}", message);
        
            Console.WriteLine(" [*] Waiting for messages.");

            var consumer = new EventingBasicConsumer(channel);
            consumer.Received += (model, ea) =>
            {
                var body = ea.Body.ToArray();
                var message = Encoding.UTF8.GetString(body);
                Console.WriteLine(" [x] Received {0}", message);
            };
            channel.BasicConsume(queue: "postgresqlTOc#backend", autoAck: true, consumer: consumer);

            Console.WriteLine(" Press [enter] to exit.");
            Console.ReadLine();
        }
        Console.WriteLine(" Press [enter] to exit.");
        Console.ReadLine();
        */
    }

    public static IConnection GetConnection(string hostName, string userName, string password)
    {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.HostName = hostName;
        connectionFactory.UserName = userName;
        connectionFactory.Password = password;
        return connectionFactory.CreateConnection();
    }

    public static void Test()
    {
        var factory = new ConnectionFactory() { HostName = "172.26.169.103", UserName = "admin", Password = "Luftwaffe1" };
        //var factory = GetConnection("172.26.169.103", "admin", "Luftwaffe1");
        using(var connection = factory.CreateConnection())
        using(var channel = connection.CreateModel())
        {
            //channel.QueueDeclare(queue: "c#backendTOpostgresql", durable: true, exclusive: false, autoDelete: false, arguments: null);

            string message = "SHOW max_connections";
            var body = Encoding.UTF8.GetBytes(message);

            channel.BasicPublish(exchange: "", routingKey: "c#backendTOpostgresql", basicProperties: null, body: body);
            Console.WriteLine(" [x] Sent {0}", message);
        }

        Console.WriteLine(" Press [enter] to exit.");
        Console.ReadLine();
    }

    public static Dictionary<string, string> ReceiveFromFrontend(IModel channel)
    {
        var values = new Dictionary<string, string>();
        Console.WriteLine(" [*] Waiting for messages.");

        var consumer = new EventingBasicConsumer(channel);
        consumer.Received += (model, ea) =>
        {
            var body = ea.Body.ToArray();
            var message = Encoding.UTF8.GetString(body);
            Console.WriteLine(" [x] Received {0}", message);
            values = JsonConvert.DeserializeObject<Dictionary<string,string>>(message);
        };
        channel.BasicConsume(queue: "nodejsTOc#backend", autoAck: true, consumer: consumer);
        
        return values;        
    }

    public static void Register() 
    {
        // receive info from frontend
        //string queryString = "SELECT version()";
        //string queryString = "SELECT * FROM `users` WHERE email=`" + email + "`";
        // send query with frontend info to database queue
        // check if user already exists
        // if doesn't exist:
        //string insertQuery = "INSERT INTO `account` (email, password) VALUES('" + email + "', '" + password + "')";
        // if query worked, record successful. if not, give error message
    }

    public static void Login(string email, string password) 
    {
        //string query = "SELECT * FROM `account` WHERE email='" + email + "' AND password='" + password + "'";
        // send to database queue
        // check with database
        // if login successful, let frontend know
        // if login not successful, tell frontend "Wrong username or password, please try again."
    }
}