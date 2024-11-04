package com.hydra.main.services;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.MessageProperties;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeoutException;

@Service
public class MessageSenderService {
    private final static String QUEUE_NAME = "main";// main queue

    private ConnectionFactory factory;
    private Connection connection;
    private Channel channel;

    public MessageSenderService()
    {
        factory = new ConnectionFactory();

        try
        {
            connect("localhost", 5672);
        }
        catch (RuntimeException e)
        {
            System.out.println("Error connection...");
        }
    }

    public void connect(String host, int port)
    {
        factory.setHost(host);
        factory.setPort(port);

        try
        {
            connection = factory.newConnection();
            channel = connection.createChannel();
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (TimeoutException e) {
            throw new RuntimeException(e);
        }
    }

    public boolean sendMessage(String message) throws IOException {
        if(channel == null)
        {
            try
            {
                System.out.println("Connecting to 172.18.0.2:5672");
//                connect("172.18.0.2", 5672);
                connect("localhost", 5672);
            }
            catch (RuntimeException e)
            {
                System.out.println("Error connection...");
                System.out.println(e.getMessage());
                return false;
            }
        }
        boolean durable = true;//the queue will survive a RabbitMQ node restart
        channel.queueDeclare(QUEUE_NAME, durable, false, false, null);

        //MessageProperties.PERSISTENT_TEXT_PLAIN - mark messages as persistent
        channel.basicPublish("", QUEUE_NAME,
                MessageProperties.PERSISTENT_TEXT_PLAIN,
                message.getBytes(StandardCharsets.UTF_8));
        System.out.println(" [x] Sent '" + message + "'");

        return true;
    }
}
