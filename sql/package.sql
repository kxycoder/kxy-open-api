CREATE TABLE `system_package_category` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '维度名称',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '描述',
  `table_model` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '表类型',
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='套餐维度模板';

CREATE TABLE `system_package_setting` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '模版编号',
  `package_id` int(20) NOT NULL COMMENT '套餐编号',
  `category_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '维度名称',
  `ids` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '配置',
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='套餐维度配置';