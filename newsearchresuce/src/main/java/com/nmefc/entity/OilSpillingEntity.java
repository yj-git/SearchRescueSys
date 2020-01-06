package com.nmefc.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.GeoSpatialIndexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.Date;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: evase
 * \* Date: 2020/1/2
 * \* Time: 20:07
 * \* To change this template use File | Settings | File Templates.
 * \* Description:
 * \
 */
@Document(collection = "oil_spilling_model")
@Setter
@Getter
@ToString
public class OilSpillingEntity {
    @Id
    @JsonIgnore
    private String _id;

    /**
     * 编号
     */
    private String code;

    private int status;

    private Date time;

    private WindModel wind;
//    @GeoSpatialIndexed
//    private Double[] point;

//    /**
////     * 海温
////     */
////    private float wt;
////
////    /**
////     * 水含量
////     */
////    private float water_fraction;
}