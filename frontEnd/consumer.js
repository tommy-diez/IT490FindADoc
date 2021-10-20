const amqp = require("amqplib/callback_api");

module.exports = class Consumer {

    static consume() {
        amqp.connect('amqp://admin:Luftwaffe1@172.26.169.103', (error, connection) => {
            if (error) {
                throw error;
            }

            //create channel connection
            connection.createChannel((channelError, channel) => {
                if (channelError) {
                    throw channelError
                }

                const QUEUE = "c#backendTOnodejs";
                channel.assertQueue(QUEUE);

                channel.consume(QUEUE, (msg) => {
                    console.log(msg.content.toString());
                })
            })
        })
        return true;
    }
}




