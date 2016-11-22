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