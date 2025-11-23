-- 菜单 SQL
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status, component_name,visible
)
VALUES (
    '示例联系人表管理', '', 2, 0, 5307,
    'demo01-contact', '', 'kxy/demo01contact/index', 0, 'Demo01Contact',1
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
    '展示菜单', '/', 3, 0, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '示例联系人表查询', 'kxy:demo01-contact:query', 3, 1, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '示例联系人表创建', 'kxy:demo01-contact:create', 3, 2, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '示例联系人表更新', 'kxy:demo01-contact:update', 3, 3, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '示例联系人表删除', 'kxy:demo01-contact:delete', 3, 4, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '示例联系人表导出', 'kxy:demo01-contact:export', 3, 5, @parentId,
    '', '', '', 0
);-- 菜单 SQL
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status, component_name,visible
)
VALUES (
    '示例分类表管理', '', 2, 0, 5307,
    'demo02-category', '', 'kxy/demo02category/index', 0, 'Demo02Category',1
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
    '展示菜单', '/', 3, 0, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '示例分类表查询', 'kxy:demo02-category:query', 3, 1, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '示例分类表创建', 'kxy:demo02-category:create', 3, 2, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '示例分类表更新', 'kxy:demo02-category:update', 3, 3, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '示例分类表删除', 'kxy:demo02-category:delete', 3, 4, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '示例分类表导出', 'kxy:demo02-category:export', 3, 5, @parentId,
    '', '', '', 0
);-- 菜单 SQL
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status, component_name,visible
)
VALUES (
    '学生课程表管理', '', 2, 0, 5307,
    'demo03-course', '', 'kxy/demo03course/index', 0, 'Demo03Course',0
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
    '展示菜单', '/', 3, 0, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生课程表查询', 'kxy:demo03-course:query', 3, 1, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生课程表创建', 'kxy:demo03-course:create', 3, 2, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生课程表更新', 'kxy:demo03-course:update', 3, 3, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生课程表删除', 'kxy:demo03-course:delete', 3, 4, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生课程表导出', 'kxy:demo03-course:export', 3, 5, @parentId,
    '', '', '', 0
);-- 菜单 SQL
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status, component_name,visible
)
VALUES (
    '学生班级表管理', '', 2, 0, 5307,
    'demo03-grade', '', 'kxy/demo03grade/index', 0, 'Demo03Grade',0
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
    '展示菜单', '/', 3, 0, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生班级表查询', 'kxy:demo03-grade:query', 3, 1, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生班级表创建', 'kxy:demo03-grade:create', 3, 2, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生班级表更新', 'kxy:demo03-grade:update', 3, 3, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生班级表删除', 'kxy:demo03-grade:delete', 3, 4, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生班级表导出', 'kxy:demo03-grade:export', 3, 5, @parentId,
    '', '', '', 0
);-- 菜单 SQL
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status, component_name,visible
)
VALUES (
    '学生表管理', '', 2, 0, 5307,
    'demo03-student', '', 'kxy/demo03student/index', 0, 'Demo03Student',1
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
    '展示菜单', '/', 3, 0, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生表查询', 'kxy:demo03-student:query', 3, 1, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生表创建', 'kxy:demo03-student:create', 3, 2, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生表更新', 'kxy:demo03-student:update', 3, 3, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生表删除', 'kxy:demo03-student:delete', 3, 4, @parentId,
    '', '', '', 0
);
INSERT INTO system_menu(
    name, permission, type, sort, parent_id,
    path, icon, component, status
)
VALUES (
    '学生表导出', 'kxy:demo03-student:export', 3, 5, @parentId,
    '', '', '', 0
);