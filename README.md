<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version" style="margin-right:8px;">
  <img src="https://img.shields.io/badge/FastAPI-0.115.8-blue.svg" alt="FastAPI Version" style="margin-right:8px;">
  <img src="https://img.shields.io/badge/Vue-3.2-blue.svg" alt="Vue Version" style="margin-right:8px;">
  <img src="https://img.shields.io/github/license/YunaiV/ruoyi-vue-pro" alt="License">
</p>

<h1 align="center">快享云 Mall 商城系统</h1>

<p align="center">
  <b>基于 Python + FastAPI + Vue3 的开源商城系统</b>
</p>

<p align="center">
  <a href="#项目介绍">项目介绍</a> •
  <a href="#内置功能">内置功能</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#版本说明">版本说明</a>
</p>

---

## 🎯 项目介绍

这是一个使用 **Python + FastAPI** 开发的开源 Mall 商城后端项目，基于 [RuoYi-Vue-Plus](https://gitee.com/zhijiantianya/ruoyi-vue-plus) 构建。

> **郑重声明：现在及未来都不会有商业版本，所有代码全部开源！**

如果本项目对你有帮助，欢迎 Star ⭐️，这将是对我们最大的鼓励！

---

## 🐶 新手必读

- **演示地址（Vue3 + Element Plus）：**  
  [http://open-code.forwework.com](http://open-code.forwework.com)

---

## 🐰 版本说明

**当前已实现功能：**

1. 短信对接阿里云
2. 企微授权登录
3. 微信授权登录
4. 简单服务器日志查询
5. 日志调用链
6. 配置文件支持环境变量优先

---

## 🚀 快速开始

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# 需要先调整 config.py 中的数据库、redis 配置，其他配置可自行修改
uvicorn app.main:app --host 0.0.0.0 --port 5001
```
前端项目地址：https://github.com/kxycoder/kxy-open-code-ui
---

## 🐯 平台简介

**快享云**，以开发者为中心，打造一流 Python 快速开发平台，全部开源，个人与企业可 100% 免费使用。

> 有任何问题或建议，欢迎在 Issues 提出，我们会及时处理。  
> 😜 给项目点个 Star 吧，这对我们真的很重要！

- **后端：** Python 3.10 + FastAPI
- **前端：** Vue3 + Element Plus（基于芋道前端优化）

### 为什么推荐使用本项目？

- **MIT License**：比 Apache 2.0 更宽松，个人与企业可 100% 免费使用，无需保留作者信息。
- **全量开源**：不会像其他项目只开源部分代码，架构设计一览无余。

---

## 🤝 项目外包

我们也承接外包项目，如有需求请微信联系：**qin2872006617**

---

## 🐼 内置功能

系统内置多种业务功能，助力快速搭建你的业务系统：

### 系统功能

|      | 功能         | 描述                                               |
|:----:|:------------|:--------------------------------------------------|
|      | 用户管理     | 系统用户配置                                       |
| ⭐️   | 在线用户     | 活跃用户状态监控，支持手动踢下线                   |
|      | 角色管理     | 角色菜单权限分配，支持按机构划分数据范围            |
|      | 菜单管理     | 菜单、操作、按钮权限配置，本地缓存提升性能           |
|      | 部门管理     | 组织机构树结构，支持数据权限                       |
|      | 岗位管理     | 用户职务配置                                       |
| 🚀   | 租户管理     | 多租户功能，支持 SaaS 场景                         |
| 🚀   | 租户套餐     | 租户套餐配置，灵活分配权限                         |
|      | 字典管理     | 常用固定数据维护                                   |
| 🚀   | 短信管理     | 支持阿里云、腾讯云等主流短信平台                   |
| 🚀   | 邮件管理     | 邮箱账号、模版、日志，支持所有邮件平台              |
| 🚀   | 站内信       | 站内消息通知，模版与消息管理                       |
| 🚀   | 操作日志     | 操作日志记录与查询，集成 Swagger 生成日志内容        |
| ⭐️   | 登录日志     | 登录日志记录与查询，包含异常                        |
| 🚀   | 错误码管理   | 错误码在线管理，无需重启服务                        |
|      | 通知公告     | 通知公告信息发布与维护                             |
| 🚀   | 应用管理     | SSO 单点登录应用管理，支持多种 OAuth2 授权方式      |
| 🚀   | 地区管理     | 省市区信息展示，支持 IP 定位                        |

### 基础设施

|      | 功能         | 描述                                               |
|:----:|:------------|:--------------------------------------------------|
| 🚀   | 代码生成     | 前后端代码生成（Java、Vue、SQL、单元测试），支持 CRUD 下载 |

---

## 📈 迭代与规划

我们还在持续迭代中，敬请关注！

**知识星球开发中，讲如下功能：**

1. 从零开始
   1. 运行项目（Windows环境）
   2. 运行项目（Linux环境）
   4. 如何开发一个新页面
2. 用户认证
   1. 如何实现管理后台和微信小程序登录
   2. 如何实现用户的创建
   3. 如何实现用户的账号密码登录
   4. 如何实现用户的退出
   5. 如何生成用户的token
3. 功能权限
   1. 如何设计一套权限系统
   2. 如何实现菜单的创建
   3. 后端如何实现接口鉴权
   4. 如何实现角色的创建
   5. 如何给用户角色分配权限
   6. 如何给用户分配角色
   7. 前端如何实现菜单的动态加载
   8. 前端如何实现按钮的权限校验
4. 数据权限
   1. 如何实现数据权限（内核）
   2. 如何基于数据规则生成where条件
   3. 如何实现部门级别的数据权限
5. 多租户
6. ORM
   1. 如何封装ORM
   2. 数据库事务
7. 日志及日志链路
8. 日常开发难题
   1. 如何避免循环引用
   2. 
9. 发布部署

---

加入我的知识星球，一起学习、一起进步
![alt text](image.png)