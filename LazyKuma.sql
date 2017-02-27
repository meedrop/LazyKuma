/* USER TABLE*/
CREATE TABLE Users(
  id int(20) NOT NULL AUTO_INCREMENT COMMENT "自增id",
  name varchar(30) NOT NULL COMMENT "用户名",
  name_cn varchar(50) NOT NULL COMMENT "中文名",
  password varchar(50) NOT NULL COMMENT "用户密码",
  email varchar(80) DEFAULT NULL COMMENT "邮件",
  mobile varchar(11) NOT NULL COMMENT "手机号",
  role varchar(10) NOT NULL COMMENT "角色",
  status tinyint(4) DEFAULT NULL COMMENT "账户状态",
  create_time datetime DEFAULT NULL COMMENT "创建时间",
  last_time datetime DEFAULT NULL COMMENT "上次登录时间",
  PRIMARY KEY (id),
  UNIQUE KEY uni_username (name)
) ENGINE=InnoDB AUTO_INCREMENT=300 CHARSET=utf8 COMMENT='用户表'

/*SERVER LIST TABLE*/
CREATE TABLE Servers_Info(
	sid int(20) NOT NULL AUTO_INCREMENT COMMENT "自增服务器ID",
	machine_room varchar(30) DEFAULT NULL COMMENT "机房",
	cabinet int(10) DEFAULT NULL COMMENT "机柜号",
	sn varchar(100) NOT NULL COMMENT "设备序列号",
	server_type varchar(64) NOT NULL COMMENT "设备型号",
	configuration varchar(255) NOT NULL COMMENT "配置",
	PRIMARY KEY (sid),
	UNIQUE KEY uni_sn (SN)
) ENGINE=InnoDB CHARSET=utf8 COMMENT='设备信息表'

/*SERVER LIST STATUS*/
CREATE TABLE Servers_Status(
	sid int(20) NOT NULL AUTO_INCREMENT COMMENT "外键服务器ID",
	server_name varchar(50) DEFAULT NULL COMMENT "主机名 ",
	status int(10) DEFAULT NULL COMMENT "状态",
	ip varchar(255) DEFAULT NULL COMMENT "ip地址",
	services varchar(64) DEFAULT NULL COMMENT "运行服务",
	PRIMARY KEY (sid),
	UNIQUE KEY uni_ip (ip),
	CONSTRAINT FOREIGN KEY (sid) REFERENCES Servers_Info(sid) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8 COMMENT='设备状态表'


