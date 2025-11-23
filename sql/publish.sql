CREATE TABLE `publish_app` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '应用编号',
  `name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '应用名称',
  `gitlab_id` int(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '仓库编号',
  `model` tinyint(1) DEFAULT NULL COMMENT '发布模式（0-只发虚拟机 1-docker 5-虚拟机+k8s 10-只发k8s）',
  `docker_file` int(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Dockerfile文件',
  `ci_args` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '构建参数',
  `jenkins_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Jenkins URL',
  `mutil_version` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT '0' COMMENT '多版本控制(0-单版本 1-多版本)',
  `code_control` tinyint(1) COLLATE utf8mb4_unicode_ci DEFAULT '0' COMMENT '代码管控(0-不管控 1-管控)',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '状态（0-创建 5-上线  10-停用 20-删除）',
  `creator` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updater` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='发布应用';

CREATE TABLE `publish_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_type` varchar(100) DEFAULT NULL COMMENT '文件类型(dockerfile,k8s-deployment,)',
  `content` text NOT NULL COMMENT '模板内容',
  `from_image_id` int(11) DEFAULT NULL COMMENT '引用镜像Id',
  `from_image_name` varchar(255) DEFAULT NULL COMMENT '应用镜像名称',
  `description` varchar(255) DEFAULT NULL COMMENT '模板描述',
  `version` int(11) DEFAULT NULL COMMENT '版本号',
  `status` tinyint(1) DEFAULT NULL COMMENT '状态(1-创建 10-删除)',
  `creator` varchar(20) DEFAULT NULL COMMENT '创建用户',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(20) DEFAULT NULL COMMENT '最后修改用户',
  `update_time` datetime DEFAULT NULL COMMENT '最后修改时间',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`),
  KEY `idx_file_template` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COMMENT='文件';