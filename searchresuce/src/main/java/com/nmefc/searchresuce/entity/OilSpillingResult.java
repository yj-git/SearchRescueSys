package com.nmefc.searchresuce.entity;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.Collections;
import java.util.List;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: evase
 * \* Date: 2019/12/30
 * \* Time: 21:54
 * \* To change this template use File | Settings | File Templates.
 * \* Description:
 * \
 */
@Setter
@Getter
@ToString
public class OilSpillingResult {
    private List<OilSpillingEntity> oils= Collections.emptyList();
}
