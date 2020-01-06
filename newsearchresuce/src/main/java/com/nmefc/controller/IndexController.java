package com.nmefc.controller;

import com.nmefc.entity.OilSpillingResult;
import com.nmefc.entity.OilTrackSearchMidModel;
import com.nmefc.service.OilSpillingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.Date;


@Controller
@CrossOrigin(origins = "*", allowedHeaders = "*")
@RequestMapping("/oil")
public class IndexController {

    @Autowired
    OilSpillingService oilSpillingService;

    //    private final static Logger logger = LoggerFactory.getLogger(IndexController.class);
    @ResponseBody
    @GetMapping(value="/track")
//    @RequestMapping("/track")
    public Object oilTrack(OilTrackSearchMidModel model) {

//        String code=new String();
        String code = model.getCode();
        Date dt = model.getDt();
        OilSpillingResult oilSpillingResult = new OilSpillingResult();
        oilSpillingResult.setOils(oilSpillingService.findByCode(code, dt));
        return oilSpillingResult;
    }
}