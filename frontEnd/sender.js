const amqp = require("amqplib/callback_api");

module.exports = class Sender {

    static send(messageInfo) {
        amqp.connect('amqp://admin:Luftwaffe1@172.26.169.103', (error, connection) => {
            if (error) {
                throw error;
            }
            connection.createChannel((channelError, channel) => {
                if (channelError) {
                    throw channelError
                }
               // channel.sendToQueue('nodejsTOc#backend', Buffer.from("Testing sending a message"));
                channel.sendToQueue('nodejsTOc#backend', Buffer.from(messageInfo));
                console.log("Message is sent to receiver");
            })
        })
    }
}