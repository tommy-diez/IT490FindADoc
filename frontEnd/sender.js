const amqp = require("amqplib/callback_api");

module.exports = class Sender {

    static send(messageInfo) {
        amqp.connect('amqp://findadoc:Findadoc!@172.26.99.35', (error, connection) => {
            if (error) {
                throw error;
            }
            connection.createChannel((channelError, channel) => {
                if (channelError) {
                    throw channelError
                }
                channel.sendToQueue('feTObe', Buffer.from(messageInfo));
                console.log("Message is sent to receiver");
            })
        })
    }
}