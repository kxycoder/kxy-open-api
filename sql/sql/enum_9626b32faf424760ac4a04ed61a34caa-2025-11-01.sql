-- 字典类型 SQL

INSERT INTO `system_dict_type`
(`id`, `name`, `type`, `status`, `remark`, 
`creator`, `create_time`, `updater`, 
`update_time`, `deleted`, `deleted_time`) 
VALUES (null, '性别', 'kxy_sex', 0, NULL, 'admin', '2025-11-01', '1', '2025-11-01', 0, NULL);


-- 字典内容 SQL

INSERT INTO `system_dict_data`(
    `id`, `sort`, `label`, `value`, `dict_type`, `status`, `color_type`, `css_class`, `remark`, `creator`, 
    `create_time`, `updater`, `update_time`, `deleted`) 
    VALUES (null, 0, '男', '1', 'kxy_sex', 0, 'primary', '', '', '', '2025-11-01 17:03:48', '1', '2025-11-01 16:36:39', 0);

INSERT INTO `system_dict_data`(
    `id`, `sort`, `label`, `value`, `dict_type`, `status`, `color_type`, `css_class`, `remark`, `creator`, 
    `create_time`, `updater`, `update_time`, `deleted`) 
    VALUES (null, 0, '女', '0', 'kxy_sex', 0, 'success', '', '', '', '2025-11-01 17:03:48', '1', '2025-11-01 16:36:39', 0);
