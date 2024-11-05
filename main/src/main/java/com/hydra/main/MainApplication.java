package com.hydra.main;

import com.hydra.main.services.MessageSenderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MainApplication {

	@Autowired
	private MessageSenderService messageSenderService;

	public static void main(String[] args) {
		SpringApplication.run(MainApplication.class, args);
	}

}
