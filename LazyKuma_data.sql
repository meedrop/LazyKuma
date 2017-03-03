/*
Navicat MySQL Data Transfer

Source Server         : 77python-test
Source Server Version : 50173
Source Host           : 192.168.65.77:3306
Source Database       : yw

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2017-03-03 14:16:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for Servers_Info
-- ----------------------------
DROP TABLE IF EXISTS `Servers_Info`;
CREATE TABLE `Servers_Info` (
  `sid` int(20) NOT NULL AUTO_INCREMENT COMMENT '自增服务器ID',
  `machine_room` varchar(30) DEFAULT NULL COMMENT '机房',
  `cabinet` int(10) DEFAULT NULL COMMENT '机柜号',
  `sn` varchar(100) NOT NULL COMMENT '设备序列号',
  `server_type` varchar(64) NOT NULL COMMENT '设备型号',
  `configuration` varchar(255) NOT NULL COMMENT '配置',
  PRIMARY KEY (`sid`),
  UNIQUE KEY `uni_sn` (`sn`)
) ENGINE=InnoDB AUTO_INCREMENT=805 DEFAULT CHARSET=utf8 COMMENT='设备信息表';

-- ----------------------------
-- Records of Servers_Info
-- ----------------------------
INSERT INTO `Servers_Info` VALUES ('801', '广州二区', '15', 'QWERTYUIO', 'DELL', '四核 16G');
INSERT INTO `Servers_Info` VALUES ('802', '深圳二区', '16', 'ASDFGHJKL', 'IBM', '双核 16G');
INSERT INTO `Servers_Info` VALUES ('803', '香港二区', '17', 'ZXCVBNMKL', 'HP', '双核 32G');
INSERT INTO `Servers_Info` VALUES ('804', '广州二区', '18', 'POIUYTREW', 'DELL', '双核 16G');

-- ----------------------------
-- Table structure for Servers_Status
-- ----------------------------
DROP TABLE IF EXISTS `Servers_Status`;
CREATE TABLE `Servers_Status` (
  `sid` int(20) NOT NULL AUTO_INCREMENT COMMENT '外键服务器ID',
  `server_name` varchar(50) DEFAULT NULL COMMENT '主机名 ',
  `status` int(10) DEFAULT NULL COMMENT '状态',
  `ip` varchar(255) DEFAULT NULL COMMENT 'ip地址',
  `services` varchar(64) DEFAULT NULL COMMENT '运行服务',
  PRIMARY KEY (`sid`),
  UNIQUE KEY `uni_ip` (`ip`),
  CONSTRAINT `Servers_Status_ibfk_1` FOREIGN KEY (`sid`) REFERENCES `Servers_Info` (`sid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=805 DEFAULT CHARSET=utf8 COMMENT='设备状态表';

-- ----------------------------
-- Records of Servers_Status
-- ----------------------------
INSERT INTO `Servers_Status` VALUES ('801', 'gz_2_rabbitmq_01', '0', '10.0.0.1', 'rabbitmq消息队列');
INSERT INTO `Servers_Status` VALUES ('802', 'gz_2_redis_01', '1', '10.0.0.2', 'redis缓存');
INSERT INTO `Servers_Status` VALUES ('803', 'gz_2_mysql_01', '1', '10.0.0.3', 'mysql数据库');
INSERT INTO `Servers_Status` VALUES ('804', 'gz_2_mongodb_01', '0', '10.0.0.4', 'mongodb数据库');

-- ----------------------------
-- Table structure for Users
-- ----------------------------
DROP TABLE IF EXISTS `Users`;
CREATE TABLE `Users` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT 'è‡ªå¢žid',
  `name` varchar(30) NOT NULL COMMENT 'ç”¨æˆ·å',
  `name_cn` varchar(50) NOT NULL COMMENT 'ä¸­æ–‡å',
  `password` varchar(50) NOT NULL COMMENT 'ç”¨æˆ·å¯†ç ',
  `email` varchar(80) DEFAULT NULL COMMENT 'é‚®ä»¶',
  `mobile` varchar(11) NOT NULL COMMENT 'æ‰‹æœºå·',
  `role` varchar(10) NOT NULL COMMENT 'è§’è‰²',
  `status` tinyint(4) DEFAULT NULL COMMENT 'è´¦æˆ·çŠ¶æ€',
  `create_time` datetime DEFAULT NULL COMMENT 'åˆ›å»ºæ—¶é—´',
  `last_time` datetime DEFAULT NULL COMMENT 'ä¸Šæ¬¡ç™»å½•æ—¶é—´',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uni_username` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COMMENT='ç”¨æˆ·è¡¨';

-- ----------------------------
-- Records of Users
-- ----------------------------
INSERT INTO `Users` VALUES ('8', 'William', '运维组-威廉', 'eef805fe817b333288bd7d0ea4e15b47', 'William@meedrop.com', '18888888888', 'admin', '0', null, null);
INSERT INTO `Users` VALUES ('9', 'Alex', '运维组-阿里斯 ', 'eef805fe817b333288bd7d0ea4e15b47', 'Alex@meedrop.com', '18888888888', 'admin', '0', null, null);
INSERT INTO `Users` VALUES ('10', 'Bob', '运维组-鲍勃', 'eef805fe817b333288bd7d0ea4e15b47', 'Bob@meedrop.com', '18888888888', 'admin', '1', null, null);
INSERT INTO `Users` VALUES ('11', 'Jack', '运维组-杰克', 'eef805fe817b333288bd7d0ea4e15b47', 'Jack@meedrop.com', '18888888888', 'admin', '1', null, null);
INSERT INTO `Users` VALUES ('12', 'Jeff', '应用组-杰夫', 'eef805fe817b333288bd7d0ea4e15b47', 'Jeff@bob@meedrop.com', '18888888888', 'common', '0', null, null);
INSERT INTO `Users` VALUES ('13', 'Mike', '应用组-麦克', 'eef805fe817b333288bd7d0ea4e15b47', 'Mike@bob@meedrop.com', '18888888888', 'common', '1', null, null);
