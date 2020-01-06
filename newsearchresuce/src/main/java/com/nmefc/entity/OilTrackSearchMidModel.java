package com.nmefc.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import org.springframework.format.annotation.DateTimeFormat;

import java.util.Date;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: evase
 * \* Date: 2020/1/2
 * \* Time: 20:36
 * \* To change this template use File | Settings | File Templates.
 * \* Description:
 * \
 */
public class OilTrackSearchMidModel {
    private String code;

//    @DateTimeFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSZ")
//    @JsonFormat(timezone = "GTM+8", pattern = "yyyy-MM-dd HH:mm:ss")
    // TODO:[*] 20-01-02 注意此处使用JsonFormat记得在pom中加入jackson的相关依赖
    @DateTimeFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSZ")
    @JsonFormat(timezone = "GTM+8", pattern = "yyyy-MM-dd HH:mm:ss")
    private Date dt;

    public String getCode(){return code;}

    public Date getDt(){return dt;}

    public void setCode(String code){
        this.code=code;
    }

    public void setDt(Date dt){
        this.dt=dt;
    }

}
