# Infra API Documentation

### /infra/file/upload

```json
{
    "code": 0,
    "data": "http://127.0.0.1:48080/admin-api/infra/file/29/get/20250820/blob_1755653607653.png",
    "msg": ""
}

```

put <http://192.168.15.172:48080/admin-api/system/user/profile/update>

```json
{"avatar":"http://127.0.0.1:48080/admin-api/infra/file/29/get/20250820/blob_1755653607653.png"}

{"code":0,"data":true,"msg":""}
```

put <http://192.168.15.172:48080/admin-api/system/user/profile/update>

```json
{"nickname":"快享云","mobile":"18601650373","email":"11aoteman@126.com","sex":2,"id":1,"username":"admin","avatar":"http://test.yudao.iocoder.cn/test/20250502/avatar_1746154660449.png","loginIp":"192.168.12.3","loginDate":1754791784000,"createTime":1609837427000,"roles":[{"id":1,"name":"超级管理员"},{"id":2,"name":"普通角色"}],"dept":{"id":103,"name":"研发部门","parentId":101},"posts":[{"id":1,"name":"董事长"},{"id":2,"name":"项目经理"}]}

{"code":0,"data":true,"msg":""}
```

/system/user/profile/get

```json
{
    "code": 0,
    "data": {
        "id": 1,
        "username": "admin",
        "nickname": "快享云",
        "email": "11aoteman@126.com",
        "mobile": "18601650373",
        "sex": 2,
        "avatar": "http://test.yudao.iocoder.cn/test/20250502/avatar_1746154660449.png",
        "loginIp": "192.168.12.3",
        "loginDate": 1754791784000,
        "createTime": 1609837427000,
        "roles": [
            {
                "id": 1,
                "name": "超级管理员"
            },
            {
                "id": 2,
                "name": "普通角色"
            }
        ],
        "dept": {
            "id": 103,
            "name": "研发部门",
            "parentId": 101
        },
        "posts": [
            {
                "id": 1,
                "name": "董事长"
            },
            {
                "id": 2,
                "name": "项目经理"
            }
        ]
    },
    "msg": ""
}
```
