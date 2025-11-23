CREATE TABLE `infra_template` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '模版编号',
  `name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模版名称',
  `variable` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模版变量',
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='模版表';

CREATE TABLE `infra_template_file` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `template_id` int(20) NOT NULL COMMENT '模版编号',
  `name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件名称',
  `file_path` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件保存路径',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文件内容',
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='模版文件表';


CREATE TABLE `infra_table` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT 'Id',
  `primary_key` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '主键',
  `database_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '数据库名',
  `table_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '表名',
  `table_des` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '表描述',
  `page_model` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '页面模式',
  `template_id` int(20) DEFAULT NULL COMMENT '模板编号',
  `template_param` varchar(1000) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '页面模式',
  `user_id` int(11) DEFAULT NULL COMMENT '用户编号',
  `apifox_admin` varchar(30) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'apifox管理端项目',
  `apifox_api` varchar(30) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'apifox用户端项目',
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='表列表';


CREATE TABLE `infra_table_fields` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Id',
  `table_id` int(11) DEFAULT NULL COMMENT '表Id',
  `field_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '字段名',
  `is_primary_key` int(11) DEFAULT NULL COMMENT '是否主键',
  `is_auto_increment` int(11) DEFAULT NULL COMMENT '自增',
  `can_null` int(11) DEFAULT NULL COMMENT '可空',
  `data_type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '类型',
  `description` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '描述',
  `length` int(11) DEFAULT NULL COMMENT '长度',
  `show_in_table` int(11) DEFAULT NULL COMMENT '在表格展示',
  `show_in_form` int(11) DEFAULT NULL COMMENT '编辑展示',
  `show_detail` int(11) DEFAULT NULL COMMENT '详情展示',
  `show_in_serch` int(11) DEFAULT NULL COMMENT '搜索条件',
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='表字段';