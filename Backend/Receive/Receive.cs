using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System;
using System.Text;

class Receive
{
    public static void Main()
    {
        var factory = new ConnectionFactory() { HostName = "172.26.169.103", UserName = "admin", Password = "Luftwaffe1"};
        //var factory = GetConnection("172.26.169.103", "admin", "Luftwaffe1");
        using (var connection = factory.CreateConnection())
        using (var channel = connection.CreateModel())
        {
            //channel.QueueDeclare(queue: "nodejsTOc#backend", durable: false, exclusive: false, autoDelete: false, arguments: null);

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