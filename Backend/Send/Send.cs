using System;
using RabbitMQ.Client;
using System.Text;

class Send
{
    public static void Main()
    {
        var factory = new ConnectionFactory() { HostName = "172.26.169.103", UserName = "admin", Password = "Luftwaffe1" };
        //var factory = GetConnection("172.26.169.103", "admin", "Luftwaffe1");
        using(var connection = factory.CreateConnection())
        using(var channel = connection.CreateModel())
        {
            //channel.QueueDeclare(queue: "c#backendTOpostgresql", durable: true, exclusive: false, autoDelete: false, arguments: null);

            string message = "Hello World!";
            var body = Encoding.UTF8.GetBytes(message);

            channel.BasicPublish(exchange: "", routingKey: "c#backendTOpostgresql", basicProperties: null, body: body);
            Console.WriteLine(" [x] Sent {0}", message);
        }

        Console.WriteLine(" Press [enter] to exit.");
        Console.ReadLine();
    }

    public static IConnection GetConnection(string hostName, string userName, string password)
    {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.HostName = hostName;
        connectionFactory.UserName = userName;
        connectionFactory.Password = password;
        return connectionFactory.CreateConnection();
    }
}