package com.hydra.main.services;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.MessageProperties;
import jakarta.annotation.PreDestroy;
import org.springframework.beans.factory.annotation.Value;
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

    @Value("${main.rabbitmq_host}")
    private String rabbiMQ_Host;

    public MessageSenderService()
    {
        factory = new ConnectionFactory();

        try
        {
            connect(rabbiMQ_Host, 5672);
        }
        catch (RuntimeException e)
        {
            System.out.println(e.getMessage());
        }
    }

    public void connect(String host, int port)
    {
        factory.setHost(host);
        factory.setPort(port);

        try
        {
            System.out.println("Connecting to " + host + ":" + port + "...");
            connection = factory.newConnection();
            channel = connection.createChannel();

            //create new queue or do nothing if it exists
            boolean durable = true;//the queue(and messages inside) will survive a RabbitMQ restart
            channel.queueDeclare(QUEUE_NAME, durable, false, false, null);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (TimeoutException e) {
            throw new RuntimeException(e);
        }
    }

    @PreDestroy
    public void closeConnection() throws IOException, TimeoutException {
        System.out.println("Checking connection...");
        if(channel == null) return;

        System.out.println("Closing connection...");
        connection.close();
        channel.close();
    }

    public boolean sendMessage(String message) throws IOException {
        if(channel == null)
        {
            try
            {
                connect(rabbiMQ_Host, 5672);
            }
            catch (RuntimeException e)
            {
                System.out.println(e.getMessage());
                return false;
            }
        }

        //MessageProperties.PERSISTENT_TEXT_PLAIN - mark messages as persistent
        channel.basicPublish("", QUEUE_NAME,
                MessageProperties.PERSISTENT_TEXT_PLAIN, // our message now will be persistent
                message.getBytes(StandardCharsets.UTF_8));
        System.out.println(" [x] Sent '" + message + "'");

        return true;
    }
}
