const amqp = require("amqplib/callback_api");

module.exports = class Sender {

    static send(messageInfo) {
        /*
        amqp.connect('amqp://findadoc:Findadoc!@172.26.169.103', (error, connection) => {
            /*
            if (error) {
                throw error;
            }
            connection.createChannel((channelError, channel) => {
                if (channelError) {
                    throw channelError
                }

                let exchangeName = "rabbitmqFanout";

                /*
                channel.assertExchange(exchangeName, 'direct', {
                    durable: false
                });


                // channel.sendToQueue('nodejsTOc#backend', Buffer.from("Testing sending a message"));
                channel.publish(exchangeName, 'feTObeRK', Buffer.from(messageInfo));
                console.log("Message is sent to receiver");
            })
        */
        amqp.connect('amqp://findadoc:Findadoc!@172.26.169.103', (error, connection) => {
            if (error) {
                throw error;
            }
            connection.createChannel((channelError, channel) => {
                if (channelError) {
                    throw channelError
                }
                // channel.sendToQueue('nodejsTOc#backend', Buffer.from("Testing sending a message"));
                channel.sendToQueue('feTObe', Buffer.from(messageInfo));
                console.log("Message is sent to receiver");
            })
        })
    }
}