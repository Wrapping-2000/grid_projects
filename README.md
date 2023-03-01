# grid_projects

## 0 说明
本项目是组内老师接的横向项目，主要是整理一些数据并对其进行编辑。这是我第一次前端和后端一起写，捋清了一些流程，让我学到不少东西。

## 1 介绍
- `js-jyy-hpj-page-client`是前端，主要是antd+react+typescript实现。
- `js-jyy-hpj-service`是后端，主要是flask+python。
- MongoDB数据库导出文件，是一些使用mongodump导出的数据库文件。

## 配置
主要是在windows上跑代码，没有在其他平台跑。

### 数据库
- 下载配置好mangodb，使用Navicat Premium进行数据库的管理，导入MongoDB数据库导出文件。

### 前端
在config文件夹下
- config.dev.ts第19行将shemePath中的ip替换为自己电脑的ip；
- config.ts第80行将shemePath中的ip替换为自己电脑ip；
- constant.ts第1行将`DEVELOPMENT_HOST`替换为自己电脑ip；
- 打开`README.md`运行`npm install`、`yarn`等命令。

### 后端
- 打开项目后，在项目的虚拟环境中安装`requirements.txt`和`requirement_1.txt`中的依赖。

## 运行
- 打开Navicat Premium运行起来`post_project`；
- 后端运行`post_project_evaluation.py`中的main函数；
- 前端运行`README.md`中的`npm start`

打开`http://localhost:8000`，用户名admin，密码#BlinkDagger!2250
