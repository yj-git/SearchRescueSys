package com.nmefc.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;


@Controller
@CrossOrigin(origins = "*",allowedHeaders ="*" )
//@RequestMapping("/oil")
public class IndexController {

//    private final static Logger logger = LoggerFactory.getLogger(IndexController.class);
    @ResponseBody
//    @GetMapping("/track")
    @RequestMapping("/")
    public String oilTrack() {
        String code=new String();
//        return oilSpillingResult;
        return "test";
    }
}