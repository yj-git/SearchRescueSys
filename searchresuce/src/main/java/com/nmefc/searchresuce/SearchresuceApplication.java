package com.nmefc.searchresuce;
//package com.nmefc.searchresuce.controller;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class SearchresuceApplication {

    public static void main(String[] args) {
//        System.setProperty("app.key", "nmefc-searchresuce");
        SpringApplication.run(SearchresuceApplication.class, args);
    }

}
