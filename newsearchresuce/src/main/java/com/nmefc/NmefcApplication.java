package com.nmefc;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class NmefcApplication {

    public static void main(String[] args) {
        SpringApplication.run(NmefcApplication.class, args);
    }

}
