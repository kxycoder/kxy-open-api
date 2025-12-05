ALTER TABLE `system_social_client` 
ADD COLUMN `auto_registor` tinyint(1) NULL COMMENT '是否自动注册' AFTER `agent_id`,
ADD COLUMN `default_roles` varchar(255) NULL COMMENT '默认角色' AFTER `auto_registor`;

ALTER TABLE `system_dept` 
ADD COLUMN `default_roles` varchar(255) NULL COMMENT '默认角色' AFTER `leader_user_id`;
