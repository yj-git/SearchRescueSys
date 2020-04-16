/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80017
 Source Host           : localhost:3306
 Source Schema         : searchrescue

 Target Server Type    : MySQL
 Target Server Version : 80017
 File Encoding         : 65001

 Date: 14/04/2020 14:39:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dict_base
-- ----------------------------
DROP TABLE IF EXISTS `dict_base`;
CREATE TABLE `dict_base`  (
  `code` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `type_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `desc` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `val` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dict_base
-- ----------------------------
INSERT INTO `dict_base` VALUES (400, 0, 'COVERAGE_TYPE', 'COVERAGE_TYPE', '栅格数据种类', 'COVERAGE_TYPE');
INSERT INTO `dict_base` VALUES (401, 400, 'CURRENT', 'CURRENT', '海流', 'current');
INSERT INTO `dict_base` VALUES (402, 400, 'WIND', 'WIND', '风', 'wind');
INSERT INTO `dict_base` VALUES (500, 0, 'COVERAGE_AREA', 'COVERAGE_AREA', '删格数据区域', 'COVERAGE_AREA');
INSERT INTO `dict_base` VALUES (501, 500, 'bhs', 'bhs', '印度洋', 'bhs');
INSERT INTO `dict_base` VALUES (502, 500, 'ecs', 'ecs', '东中国海', 'ecs');
INSERT INTO `dict_base` VALUES (503, 500, 'scs', 'scs', '南海', 'scs');
INSERT INTO `dict_base` VALUES (504, 500, 'nwp', 'nwp', '西北太', 'nwp');

SET FOREIGN_KEY_CHECKS = 1;
