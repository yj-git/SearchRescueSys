package com.nmefc.service;

import com.nmefc.entity.OilSpillingEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: evase
 * \* Date: 2020/1/2
 * \* Time: 20:08
 * \* To change this template use File | Settings | File Templates.
 * \* Description:
 * \
 */
@Service
public class OilSpillingService {

    @Autowired
    private MongoTemplate mongoTemplate;

    /**
     * @Author : evaseemefly
     * @Description : 根据code找到对应code的 oil list
     * @params :
     * @Date : 2019/12/30 19:58
     * @return :
     */
    public List<OilSpillingEntity> findByCode(String code, Date dt){
        Query query=new Query(Criteria.where("code").is(code).and("time").is(dt));
        return mongoTemplate.find(query,OilSpillingEntity.class);
    }
}
