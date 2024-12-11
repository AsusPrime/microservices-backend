package com.hydra.main.controllers;

import com.hydra.main.services.MessageSenderService;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestBody;

import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.MessageProperties;

import java.io.IOException;
import java.util.Map;

@Controller
@RequestMapping(value = "/test")
public class MainController {
    private final MessageSenderService messageSenderService;

    public MainController(MessageSenderService messageSenderService)
    {
        this.messageSenderService = messageSenderService;
    }

    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<Map<String, String>> test(@RequestBody(required = false) Map<String, Object> data)
    {
        if(data.isEmpty())
        {
            return ResponseEntity.status(HttpStatus.UNSUPPORTED_MEDIA_TYPE)
                    .body(Map.of("status", "unsupported media type", "message", "content type must be application/json"));
        }

        String email = (String) data.get("email");
        String image = (String) data.get("link");

        if(email == null || image == null)
        {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(Map.of("status", "bad request", "message", "missing email or link"));
        }

        JSONObject message = new JSONObject();
        message.put("email", email);
        message.put("image", image);

        //send data into process function
        //TODO:
        //* if unable send message don't add photo to the DB
        // make this function 'transactional'!!!
        try {
            if(!messageSenderService.sendMessage(message)){
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                        .body(Map.of("status", "server error", "message", "Unable to send message! Try again later"));
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return ResponseEntity.status(HttpStatus.OK)
                .body(Map.of("status", "success", "message", "Photo successfully processed!"));
    }
}
