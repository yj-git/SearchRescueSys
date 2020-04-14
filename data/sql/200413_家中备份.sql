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

 Date: 13/04/2020 18:51:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 81 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add Token', 7, 'add_token');
INSERT INTO `auth_permission` VALUES (26, 'Can change Token', 7, 'change_token');
INSERT INTO `auth_permission` VALUES (27, 'Can delete Token', 7, 'delete_token');
INSERT INTO `auth_permission` VALUES (28, 'Can view Token', 7, 'view_token');
INSERT INTO `auth_permission` VALUES (29, 'Can add job info', 8, 'add_jobinfo');
INSERT INTO `auth_permission` VALUES (30, 'Can change job info', 8, 'change_jobinfo');
INSERT INTO `auth_permission` VALUES (31, 'Can delete job info', 8, 'delete_jobinfo');
INSERT INTO `auth_permission` VALUES (32, 'Can view job info', 8, 'view_jobinfo');
INSERT INTO `auth_permission` VALUES (33, 'Can add auth user dir', 9, 'add_authuserdir');
INSERT INTO `auth_permission` VALUES (34, 'Can change auth user dir', 9, 'change_authuserdir');
INSERT INTO `auth_permission` VALUES (35, 'Can delete auth user dir', 9, 'delete_authuserdir');
INSERT INTO `auth_permission` VALUES (36, 'Can view auth user dir', 9, 'view_authuserdir');
INSERT INTO `auth_permission` VALUES (37, 'Can add case info', 10, 'add_caseinfo');
INSERT INTO `auth_permission` VALUES (38, 'Can change case info', 10, 'change_caseinfo');
INSERT INTO `auth_permission` VALUES (39, 'Can delete case info', 10, 'delete_caseinfo');
INSERT INTO `auth_permission` VALUES (40, 'Can view case info', 10, 'view_caseinfo');
INSERT INTO `auth_permission` VALUES (41, 'Can add job user rate', 11, 'add_jobuserrate');
INSERT INTO `auth_permission` VALUES (42, 'Can change job user rate', 11, 'change_jobuserrate');
INSERT INTO `auth_permission` VALUES (43, 'Can delete job user rate', 11, 'delete_jobuserrate');
INSERT INTO `auth_permission` VALUES (44, 'Can view job user rate', 11, 'view_jobuserrate');
INSERT INTO `auth_permission` VALUES (45, 'Can add case oil info', 12, 'add_caseoilinfo');
INSERT INTO `auth_permission` VALUES (46, 'Can change case oil info', 12, 'change_caseoilinfo');
INSERT INTO `auth_permission` VALUES (47, 'Can delete case oil info', 12, 'delete_caseoilinfo');
INSERT INTO `auth_permission` VALUES (48, 'Can view case oil info', 12, 'view_caseoilinfo');
INSERT INTO `auth_permission` VALUES (49, 'Can add job user rate', 13, 'add_jobuserrate');
INSERT INTO `auth_permission` VALUES (50, 'Can change job user rate', 13, 'change_jobuserrate');
INSERT INTO `auth_permission` VALUES (51, 'Can delete job user rate', 13, 'delete_jobuserrate');
INSERT INTO `auth_permission` VALUES (52, 'Can view job user rate', 13, 'view_jobuserrate');
INSERT INTO `auth_permission` VALUES (53, 'Can add auth rescue rela', 14, 'add_authrescuerela');
INSERT INTO `auth_permission` VALUES (54, 'Can change auth rescue rela', 14, 'change_authrescuerela');
INSERT INTO `auth_permission` VALUES (55, 'Can delete auth rescue rela', 14, 'delete_authrescuerela');
INSERT INTO `auth_permission` VALUES (56, 'Can view auth rescue rela', 14, 'view_authrescuerela');
INSERT INTO `auth_permission` VALUES (57, 'Can add auth oil rela', 15, 'add_authoilrela');
INSERT INTO `auth_permission` VALUES (58, 'Can change auth oil rela', 15, 'change_authoilrela');
INSERT INTO `auth_permission` VALUES (59, 'Can delete auth oil rela', 15, 'delete_authoilrela');
INSERT INTO `auth_permission` VALUES (60, 'Can view auth oil rela', 15, 'view_authoilrela');
INSERT INTO `auth_permission` VALUES (61, 'Can add case rescue info', 16, 'add_caserescueinfo');
INSERT INTO `auth_permission` VALUES (62, 'Can change case rescue info', 16, 'change_caserescueinfo');
INSERT INTO `auth_permission` VALUES (63, 'Can delete case rescue info', 16, 'delete_caserescueinfo');
INSERT INTO `auth_permission` VALUES (64, 'Can view case rescue info', 16, 'view_caserescueinfo');
INSERT INTO `auth_permission` VALUES (65, 'Can add job info', 17, 'add_jobinfo');
INSERT INTO `auth_permission` VALUES (66, 'Can change job info', 17, 'change_jobinfo');
INSERT INTO `auth_permission` VALUES (67, 'Can delete job info', 17, 'delete_jobinfo');
INSERT INTO `auth_permission` VALUES (68, 'Can view job info', 17, 'view_jobinfo');
INSERT INTO `auth_permission` VALUES (69, 'Can add select model', 18, 'add_selectmodel');
INSERT INTO `auth_permission` VALUES (70, 'Can change select model', 18, 'change_selectmodel');
INSERT INTO `auth_permission` VALUES (71, 'Can delete select model', 18, 'delete_selectmodel');
INSERT INTO `auth_permission` VALUES (72, 'Can view select model', 18, 'view_selectmodel');
INSERT INTO `auth_permission` VALUES (73, 'Can add coverage model', 19, 'add_coveragemodel');
INSERT INTO `auth_permission` VALUES (74, 'Can change coverage model', 19, 'change_coveragemodel');
INSERT INTO `auth_permission` VALUES (75, 'Can delete coverage model', 19, 'delete_coveragemodel');
INSERT INTO `auth_permission` VALUES (76, 'Can view coverage model', 19, 'view_coveragemodel');
INSERT INTO `auth_permission` VALUES (77, 'Can add task user model', 20, 'add_taskusermodel');
INSERT INTO `auth_permission` VALUES (78, 'Can change task user model', 20, 'change_taskusermodel');
INSERT INTO `auth_permission` VALUES (79, 'Can delete task user model', 20, 'delete_taskusermodel');
INSERT INTO `auth_permission` VALUES (80, 'Can view task user model', 20, 'view_taskusermodel');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `email` varchar(254) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$180000$Vra3jpIyceev$hTLkzj0DGfC8BnlqOPhjlFlrXGE8Arew0nruSfqRidI=', NULL, 1, 'admin', '', '', 'evaseemely@126.com', 1, 1, '2020-01-07 12:41:56.151488');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for authtoken_token
-- ----------------------------
DROP TABLE IF EXISTS `authtoken_token`;
CREATE TABLE `authtoken_token`  (
  `key` varchar(40) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `created` datetime(6) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of authtoken_token
-- ----------------------------
INSERT INTO `authtoken_token` VALUES ('6c6148e8d71b48cc420cc62018e29e823bbd75f5', '2020-01-08 12:05:09.992962', 1);

-- ----------------------------
-- Table structure for common_select
-- ----------------------------
DROP TABLE IF EXISTS `common_select`;
CREATE TABLE `common_select`  (
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `val` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `parent` int(11) NOT NULL,
  `type_select` int(11) NOT NULL,
  `menu_title` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `menu_content` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `menu_level` int(11) NULL DEFAULT NULL,
  `menu_url` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `menu_sort` int(11) NULL DEFAULT NULL,
  `menu_class` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of common_select
-- ----------------------------
INSERT INTO `common_select` VALUES ('wreck', 'wreck', 1, 'xx_1', 0, 1, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('xx_1', 'wreck', 2, 'xx_1', 1, 1, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('xx_2', 'wreck', 3, 'xx_2', 1, 1, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('func', 'EQUATION', 4, 'func', 0, 2, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('Euler', 'Euler', 5, 'Euler', 4, 2, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('Runge', 'Runge', 6, 'Runge', 4, 2, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('4Runge', '4Runge', 7, '4Runge', 4, 2, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('current', 'current', 8, 'current', 0, 4, 'current', 'current', NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('wind', 'wind', 9, 'wind', 0, 4, 'wind', 'wind', NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('bhs', '渤海', 10, '渤海', 8, 5, '渤海', '渤海', NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('ecs', '东中国海', 11, '东中国海', 8, 5, '东中国海', '东中国海', NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('ind', '印度洋', 12, '印度洋', 8, 5, '印度洋', '印度洋', NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('scs', '南海', 13, '南海', 8, 5, '南海', '南海', NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('nwp', '西北太', 14, '西北太', 8, 5, '西北太', '西北太', NULL, NULL, NULL, NULL);
INSERT INTO `common_select` VALUES ('nwp', '西北太', 15, '西北太', 9, 5, '西北太', '西北太', NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for common_select_bakup
-- ----------------------------
DROP TABLE IF EXISTS `common_select_bakup`;
CREATE TABLE `common_select_bakup`  (
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `val` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `parent` int(11) NOT NULL,
  `type_select` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of common_select_bakup
-- ----------------------------
INSERT INTO `common_select_bakup` VALUES ('wreck', 'wreck', 1, 'xx_1', 0, 1);
INSERT INTO `common_select_bakup` VALUES ('xx_1', 'wreck', 2, 'xx_1', 1, 1);
INSERT INTO `common_select_bakup` VALUES ('xx_2', 'wreck', 3, 'xx_2', 1, 1);
INSERT INTO `common_select_bakup` VALUES ('func', 'EQUATION', 4, 'func', 0, 2);
INSERT INTO `common_select_bakup` VALUES ('Euler', 'Euler', 5, 'Euler', 4, 2);
INSERT INTO `common_select_bakup` VALUES ('Runge', 'Runge', 6, 'Runge', 4, 2);
INSERT INTO `common_select_bakup` VALUES ('4Runge', '4Runge', 7, '4Runge', 4, 2);
INSERT INTO `common_select_bakup` VALUES ('current', 'current', 8, 'current', 0, 5);
INSERT INTO `common_select_bakup` VALUES ('wind', 'wind', 9, 'wind', 0, 4);
INSERT INTO `common_select_bakup` VALUES ('bhs', '渤海', 10, '渤海', 8, 5);
INSERT INTO `common_select_bakup` VALUES ('ecs', '东中国海', 11, '东中国海', 8, 5);
INSERT INTO `common_select_bakup` VALUES ('ind', '印度洋', 12, '印度洋', 8, 5);
INSERT INTO `common_select_bakup` VALUES ('scs', '南海', 13, '南海', 8, 5);
INSERT INTO `common_select_bakup` VALUES ('nwp', '西北太', 14, '西北太', 8, 5);
INSERT INTO `common_select_bakup` VALUES ('nwp', '西北太', 15, '西北太', 9, 4);

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NULL DEFAULT NULL,
  `object_id` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `object_repr` varchar(200) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `model` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (7, 'authtoken', 'token');
INSERT INTO `django_content_type` VALUES (18, 'common', 'selectmodel');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (19, 'geo', 'coveragemodel');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (9, 'user', 'authuserdir');
INSERT INTO `django_content_type` VALUES (10, 'user', 'caseinfo');
INSERT INTO `django_content_type` VALUES (8, 'user', 'jobinfo');
INSERT INTO `django_content_type` VALUES (11, 'user', 'jobuserrate');
INSERT INTO `django_content_type` VALUES (15, 'users', 'authoilrela');
INSERT INTO `django_content_type` VALUES (14, 'users', 'authrescuerela');
INSERT INTO `django_content_type` VALUES (12, 'users', 'caseoilinfo');
INSERT INTO `django_content_type` VALUES (16, 'users', 'caserescueinfo');
INSERT INTO `django_content_type` VALUES (17, 'users', 'jobinfo');
INSERT INTO `django_content_type` VALUES (13, 'users', 'jobuserrate');
INSERT INTO `django_content_type` VALUES (20, 'users', 'taskusermodel');

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
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

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

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `session_data` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `expire_date` datetime(6) NULL DEFAULT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for geo_coverageinfo
-- ----------------------------
DROP TABLE IF EXISTS `geo_coverageinfo`;
CREATE TABLE `geo_coverageinfo`  (
  `is_del` tinyint(1) NOT NULL,
  `area` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `root_path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `relative_path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_size` double NOT NULL,
  `create_date` datetime(6) NULL,
  `dimessions` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `variables` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `desc` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_original` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_authoil_rela
-- ----------------------------
DROP TABLE IF EXISTS `user_authoil_rela`;
CREATE TABLE `user_authoil_rela`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `did_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_authoil_rela_did_id_f2e44ff8_fk_user_caseoilinfo_id`(`did_id`) USING BTREE,
  INDEX `user_authoil_rela_uid_id_2821d30a_fk_auth_user_id`(`uid_id`) USING BTREE,
  CONSTRAINT `user_authoil_rela_did_id_f2e44ff8_fk_user_caseoilinfo_id` FOREIGN KEY (`did_id`) REFERENCES `user_caseoilinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_authoil_rela_uid_id_2821d30a_fk_auth_user_id` FOREIGN KEY (`uid_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of user_authoil_rela
-- ----------------------------
INSERT INTO `user_authoil_rela` VALUES (1, 1, 1);
INSERT INTO `user_authoil_rela` VALUES (2, 2, 1);
INSERT INTO `user_authoil_rela` VALUES (3, 3, 1);
INSERT INTO `user_authoil_rela` VALUES (4, 4, 1);

-- ----------------------------
-- Table structure for user_authrescue_rela
-- ----------------------------
DROP TABLE IF EXISTS `user_authrescue_rela`;
CREATE TABLE `user_authrescue_rela`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `did_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_authrescue_rela_uid_id_f280e118_fk_auth_user_id`(`uid_id`) USING BTREE,
  INDEX `user_authrescue_rela_did_id_6602b369_fk_user_caserescueinfo_id`(`did_id`) USING BTREE,
  CONSTRAINT `user_authrescue_rela_did_id_6602b369_fk_user_caserescueinfo_id` FOREIGN KEY (`did_id`) REFERENCES `user_caserescueinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_authrescue_rela_uid_id_f280e118_fk_auth_user_id` FOREIGN KEY (`uid_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for user_caseoilinfo
-- ----------------------------
DROP TABLE IF EXISTS `user_caseoilinfo`;
CREATE TABLE `user_caseoilinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_del` tinyint(1) NOT NULL,
  `root_path` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `case_path` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `create_date` datetime(6) NULL DEFAULT NULL,
  `forecast_date` datetime(6) NULL DEFAULT NULL,
  `case_name` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `case_desc` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `case_code` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `lat` double NULL DEFAULT NULL,
  `lon` double NULL DEFAULT NULL,
  `radius` double NULL DEFAULT NULL,
  `nums` int(11) NULL DEFAULT NULL,
  `simulation_duration` double NULL DEFAULT NULL,
  `simulation_step` double NULL DEFAULT NULL,
  `console_step` double NULL DEFAULT NULL,
  `current_nondeterminacy` double NULL DEFAULT NULL,
  `equation` int(11) NULL DEFAULT NULL,
  `wind_coefficient` double NULL DEFAULT NULL,
  `wind_dir` double NULL DEFAULT NULL,
  `area` int(11) NOT NULL,
  `wind_nondeterminacy` double NULL DEFAULT NULL,
  `ext` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_caseoilinfo_case_code_d2b8ad2a_uniq`(`case_code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of user_caseoilinfo
-- ----------------------------
INSERT INTO `user_caseoilinfo` VALUES (1, 0, '123', '123', '2020-02-12 15:05:01.000000', '2020-02-12 15:05:03.000000', '123', '123', '123', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, NULL);
INSERT INTO `user_caseoilinfo` VALUES (2, 0, '123', '123', '2020-02-13 15:24:43.000000', '2020-02-13 15:24:46.000000', '1234', '1234', '1234', 1, 1, 1, 11, 1, 1, 1, 1, 1, 1, 1, 1, 0, NULL);
INSERT INTO `user_caseoilinfo` VALUES (3, 0, '123', '123', '2020-02-14 14:58:47.000000', '2020-02-14 14:58:52.000000', '12345', '12345', '12345', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, NULL);
INSERT INTO `user_caseoilinfo` VALUES (4, 0, '123', '2020\\02', '2020-02-14 14:59:28.000000', '2020-02-14 14:59:30.000000', 'test_case', 'test_case', 'test_case', 120, 95, 1, 1, 1, 120, 130, 80, 1, 22, 33, 1, 90, '.nc');

-- ----------------------------
-- Table structure for user_caserescueinfo
-- ----------------------------
DROP TABLE IF EXISTS `user_caserescueinfo`;
CREATE TABLE `user_caserescueinfo`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_del` tinyint(1) NOT NULL,
  `root_path` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `case_path` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `create_date` datetime(6) NULL DEFAULT NULL,
  `forecast_date` datetime(6) NULL DEFAULT NULL,
  `case_name` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `case_desc` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `case_code` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `lat` double NULL DEFAULT NULL,
  `lon` double NULL DEFAULT NULL,
  `radius` double NULL DEFAULT NULL,
  `nums` int(11) NULL DEFAULT NULL,
  `simulation_duration` double NULL DEFAULT NULL,
  `simulation_step` double NULL DEFAULT NULL,
  `console_step` double NULL DEFAULT NULL,
  `current_nondeterminacy` double NULL DEFAULT NULL,
  `equation` int(11) NULL DEFAULT NULL,
  `goods_type` int(11) NULL DEFAULT NULL,
  `area` int(11) NOT NULL,
  `wind_nondeterminacy` double NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_caserescueinfo_case_code_fa55ec80_uniq`(`case_code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for user_jobinfo
-- ----------------------------
DROP TABLE IF EXISTS `user_jobinfo`;
CREATE TABLE `user_jobinfo`  (
  `is_del` tinyint(1) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_celery_id` varchar(200) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `case_code` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `gmt_create` datetime(6) NULL DEFAULT NULL,
  `gmt_modified` datetime(6) NULL DEFAULT NULL,
  `type` int(11) NOT NULL,
  `area` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_jobinfo_case_code_6c7efae8_uniq`(`case_code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of user_jobinfo
-- ----------------------------
INSERT INTO `user_jobinfo` VALUES (0, 1, '123', '123', '2020-02-13 14:42:02.000000', '2020-02-13 14:42:06.000000', 0, 1);
INSERT INTO `user_jobinfo` VALUES (0, 2, '1234', '1234', '2020-02-13 15:25:43.000000', '2020-02-13 15:25:47.000000', 0, 1);
INSERT INTO `user_jobinfo` VALUES (0, 3, '12345', '12345', '2020-02-14 14:54:35.000000', '2020-02-14 14:54:40.000000', 0, 1);
INSERT INTO `user_jobinfo` VALUES (0, 4, '123456', 'test_case', '2020-02-14 14:56:02.000000', '2020-02-14 14:56:05.000000', 0, 1);
INSERT INTO `user_jobinfo` VALUES (0, 5, '2', '1', '2020-02-25 13:44:11.829857', '2020-02-25 13:44:11.829857', 0, 0);

-- ----------------------------
-- Table structure for user_jobuserrate
-- ----------------------------
DROP TABLE IF EXISTS `user_jobuserrate`;
CREATE TABLE `user_jobuserrate`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rate` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `gmt_create` datetime(6) NULL DEFAULT NULL,
  `gmt_modified` datetime(6) NULL DEFAULT NULL,
  `jid_id` int(11) NOT NULL,
  `uid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_jobuserrate_jid_id_db64a98d_fk_user_jobinfo_id`(`jid_id`) USING BTREE,
  INDEX `user_jobuserrate_uid_id_2e56541a_fk_auth_user_id`(`uid_id`) USING BTREE,
  CONSTRAINT `user_jobuserrate_jid_id_db64a98d_fk_user_jobinfo_id` FOREIGN KEY (`jid_id`) REFERENCES `user_jobinfo` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_jobuserrate_uid_id_2e56541a_fk_auth_user_id` FOREIGN KEY (`uid_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of user_jobuserrate
-- ----------------------------
INSERT INTO `user_jobuserrate` VALUES (1, 20, 1, '2020-02-13 14:44:07.000000', '2020-02-13 14:44:09.000000', 1, 1);
INSERT INTO `user_jobuserrate` VALUES (2, 60, 1, '2020-02-13 14:44:42.000000', '2020-02-13 14:44:45.000000', 1, 1);
INSERT INTO `user_jobuserrate` VALUES (3, 90, 1, '2020-02-13 15:24:07.000000', '2020-02-13 15:24:09.000000', 1, 1);
INSERT INTO `user_jobuserrate` VALUES (4, 100, 2, '2020-02-13 15:26:09.000000', '2020-02-13 15:26:12.000000', 2, 1);
INSERT INTO `user_jobuserrate` VALUES (5, 0, 3, '2020-02-14 14:55:22.000000', '2020-02-14 14:55:20.000000', 3, 1);
INSERT INTO `user_jobuserrate` VALUES (6, 100, 2, '2020-02-14 14:56:21.000000', '2020-02-14 14:56:24.000000', 4, 1);
INSERT INTO `user_jobuserrate` VALUES (7, 35, 2, '2020-02-23 07:00:00.000000', '2020-02-23 08:00:00.000000', 5, 1);

-- ----------------------------
-- Table structure for user_taskinfo
-- ----------------------------
DROP TABLE IF EXISTS `user_taskinfo`;
CREATE TABLE `user_taskinfo`  (
  `root_path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `case_path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `create_date` datetime(6) NULL,
  `forecast_date` datetime(6) NULL,
  `ext` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_type` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
