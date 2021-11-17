const amqp = require("amqplib/callback_api");

amqp.connect('amqp://findadoc:Findadoc!@172.26.83.6',  (error, connection) => {

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
        })
    })
})
