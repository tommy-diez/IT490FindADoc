const amqp = require("amqplib/callback_api");
const https = require('https');
module.exports =

    class Consumer {

    async consume() {
        let data;
        amqp.connect('amqp://findadoc:Findadoc!@172.26.169.103', (error, connection) => {

            if (error) {
                throw error;
            }

            //create channel connection
            connection.createChannel((channelError, channel) => {
                if (channelError) {
                    throw channelError
                }

                const QUEUE = "beTOfe";

                channel.consume(QUEUE, (msg) => {
                    console.log(msg.content.toString());
                    data = msg.content;
                })
            })
        })
        return data;
    }
}










