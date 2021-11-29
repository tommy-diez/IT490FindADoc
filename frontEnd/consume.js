const amqp = require("amqplib/callback_api");

amqp.connect('amqp://findadoc:Findadoc!@172.26.169.103',  (error, connection) => {

    if (error) {
        throw error;
    }

    //create channel connection
    connection.createChannel((channelError, channel) => {
        if (channelError) {
            throw channelError
        }

        const QUEUE = "beTOfe";
        //channel.assertQueue(QUEUE);

        // channel.bindQueue(QUEUE, exchangeName, '');
        channel.consume(QUEUE, (msg) => {
            console.log(msg.content.toString());
        })
    })
})


    /*
    static checkIP() {

        let node;

        let nodes = ['172.26.169.103', '172.26.30.225', '172.26.83.6'];

        for (let address of nodes) {
            ping.sys.probe(address, (isAlive) => {
                if (isAlive) {
                    node = address;
                }
            })
        }

        return node;
        */









