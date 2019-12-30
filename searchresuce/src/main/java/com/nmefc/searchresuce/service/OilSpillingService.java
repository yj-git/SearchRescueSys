package com.nmefc.searchresuce.service;

//import com.nmefc.searchresuce.entity.OilSpillingModel;
import com.nmefc.searchresuce.entity.OilSpillingEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: evase
 * \* Date: 2019/12/30
 * \* Time: 19:55
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
    public List<OilSpillingEntity> findByCode(String code){

        Query query=new Query(Criteria.where("code").is(code));
        return mongoTemplate.find(query,OilSpillingEntity.class);
    }
}
