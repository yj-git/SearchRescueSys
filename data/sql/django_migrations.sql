/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 80017
 Source Host           : localhost:3306
 Source Schema         : searchrescue

 Target Server Type    : MySQL
 Target Server Version : 80017
 File Encoding         : 65001

 Date: 23/04/2020 07:05:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `applied` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 52 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2020-01-07 12:33:58.208875');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2020-01-07 12:33:58.367876');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2020-01-07 12:33:58.765876');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2020-01-07 12:33:58.861875');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2020-01-07 12:33:58.869875');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2020-01-07 12:33:58.957874');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2020-01-07 12:33:59.010876');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2020-01-07 12:33:59.066875');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2020-01-07 12:33:59.074875');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2020-01-07 12:33:59.126881');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2020-01-07 12:33:59.130876');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2020-01-07 12:33:59.141878');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2020-01-07 12:33:59.194875');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2020-01-07 12:33:59.237875');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2020-01-07 12:33:59.287905');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2020-01-07 12:33:59.294874');
INSERT INTO `django_migrations` VALUES (17, 'sessions', '0001_initial', '2020-01-07 12:33:59.322877');
INSERT INTO `django_migrations` VALUES (18, 'authtoken', '0001_initial', '2020-01-08 12:04:24.433448');
INSERT INTO `django_migrations` VALUES (19, 'authtoken', '0002_auto_20160226_1747', '2020-01-08 12:04:24.547480');
INSERT INTO `django_migrations` VALUES (20, 'user', '0001_initial', '2020-01-16 12:44:33.801752');
INSERT INTO `django_migrations` VALUES (21, 'user', '0002_auto_20200204_1450', '2020-02-04 06:51:05.302541');
INSERT INTO `django_migrations` VALUES (23, 'users', '0001_initial', '2020-02-12 02:57:29.306367');
INSERT INTO `django_migrations` VALUES (24, 'users', '0002_jobinfo_type', '2020-02-12 02:57:29.640332');
INSERT INTO `django_migrations` VALUES (25, 'users', '0003_auto_20200212_1059', '2020-02-12 02:59:08.015985');
INSERT INTO `django_migrations` VALUES (26, 'users', '0004_auto_20200212_1440', '2020-02-12 06:40:45.716596');
INSERT INTO `django_migrations` VALUES (27, 'users', '0005_auto_20200212_1444', '2020-02-12 06:49:58.392972');
INSERT INTO `django_migrations` VALUES (28, 'users', '0006_auto_20200212_1516', '2020-02-12 07:17:01.716800');
INSERT INTO `django_migrations` VALUES (29, 'users', '0007_remove_jobinfo_cid', '2020-02-13 02:50:57.222014');
INSERT INTO `django_migrations` VALUES (31, 'users', '0008_auto_20200215_2036', '2020-02-15 12:36:31.129531');
INSERT INTO `django_migrations` VALUES (32, 'common', '0002_auto_20200219_1448', '2020-02-19 06:48:34.675484');
INSERT INTO `django_migrations` VALUES (33, 'users', '0009_auto_20200219_1448', '2020-02-19 06:48:34.791487');
INSERT INTO `django_migrations` VALUES (34, 'geo', '0001_initial', '2020-04-03 03:12:33.407896');
INSERT INTO `django_migrations` VALUES (35, 'geo', '0002_auto_20200407_1458', '2020-04-07 06:58:45.932736');
INSERT INTO `django_migrations` VALUES (36, 'users', '0002_auto_20200407_1458', '2020-04-07 06:58:46.255660');
INSERT INTO `django_migrations` VALUES (37, 'common', '0001_initial', '2020-04-12 07:10:00.023606');
INSERT INTO `django_migrations` VALUES (38, 'common', '0002_auto_20200414_1638', '2020-04-14 08:49:29.006877');
INSERT INTO `django_migrations` VALUES (39, 'users', '0003_auto_20200414_2018', '2020-04-14 12:18:56.113997');
INSERT INTO `django_migrations` VALUES (40, 'geo', '0003_auto_20200414_2020', '2020-04-14 12:20:46.434742');
INSERT INTO `django_migrations` VALUES (41, 'users', '0004_auto_20200415_1009', '2020-04-15 02:09:33.998107');
INSERT INTO `django_migrations` VALUES (42, 'geo', '0004_remove_coveragemodel_area', '2020-04-15 02:11:08.832406');
INSERT INTO `django_migrations` VALUES (43, 'geo', '0005_geostoremodel_geoworkspacemodel_layermodel', '2020-04-16 02:33:50.928483');
INSERT INTO `django_migrations` VALUES (44, 'geo', '0006_auto_20200416_1038', '2020-04-16 02:39:05.786580');
INSERT INTO `django_migrations` VALUES (45, 'geo', '0007_layermodel_is_del', '2020-04-16 02:40:36.300314');
INSERT INTO `django_migrations` VALUES (46, 'geo', '0008_auto_20200416_1050', '2020-04-16 02:50:39.159994');
INSERT INTO `django_migrations` VALUES (47, 'geo', '0009_rgeoinfo_task', '2020-04-16 02:55:30.485712');
INSERT INTO `django_migrations` VALUES (48, 'geo', '0010_rgeoinfo_coverage', '2020-04-16 03:04:20.914332');
INSERT INTO `django_migrations` VALUES (49, 'users', '0005_auto_20200416_1503', '2020-04-16 07:04:23.286699');
INSERT INTO `django_migrations` VALUES (50, 'users', '0006_auto_20200416_1700', '2020-04-16 09:01:32.940448');
INSERT INTO `django_migrations` VALUES (51, 'geo', '0011_geolayermodel_style_name', '2020-04-16 12:25:40.469407');
INSERT INTO `django_migrations` VALUES (52, 'geo', '0012_geoserverbasemodel', '2020-04-16 12:51:41.474731');

SET FOREIGN_KEY_CHECKS = 1;
