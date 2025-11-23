-- 菜单 SQL
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status, component_name,visible
)
VALUES (
    '发布版本管理', '', 2, 0, 2,
    'publish-version', '', 'infra/publishversion/index', 0, 'PublishVersion',1
);

-- 按钮父菜单ID
-- 暂时只支持 MySQL。如果你是 Oracle、PostgreSQL、SQLServer 的话，需要手动修改 @parentId 的部分的代码
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '发布版本管理查询', 'infra:publish-version:query', 3, 1, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '发布版本管理创建', 'infra:publish-version:create', 3, 2, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '发布版本管理更新', 'infra:publish-version:update', 3, 3, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '发布版本管理删除', 'infra:publish-version:delete', 3, 4, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '发布版本管理导出', 'infra:publish-version:export', 3, 5, @parentId,
    '', '', '', 0
);