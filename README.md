
My-Restful-API 框架
======
>基于flask 进行封装的restful-api 服务，支持打包发布，可以用此框架快速部署web & api 服务

进度
======
基本API封装已完成，各个服务之间可以用此框架编写代码，互相使用Http Api 调用，组建之间调用参考openstack调用方式，使用oslo_messaging + rabbitmq进行同步RPC调用，基本客户端功能已完成，后续需要封装集成与调试。
gunicorn 仅支持Unix服务器，Windows下无法调试，后续加上gunicron的配置文件模板


部署
======
1. pip install -r requirement
2. python setup.py install
3. gunicorn -w 2 --worker-class=eventlet --bind 0.0.0.0 --timeout 300 wind-server-script:app

认证
======
>操作接口需要用户认证,认证完成后会获取一个token，认证时候在http header里放入Auth-Token:${token}即可完成认证

```
curl -X POST http://127.0.0.1:5000/api/v1/user/gettoken -d '{"username":"zyx","password":"123"}' -H "Content-Type: application/json"
{
    "result": "SUCCESS",
    "token": "93569027659f43239605ee324ca4bca6"
}
```
>使用token认证(创建用户):

```
curl -X POST http://127.0.0.1:5000/api/v1/user/createuser -d '{"username":"zyx10","password":"123","groupid":"1"}' -H "Content-Type: application/json" -H "Auth-Token:93569027659f43239605ee324ca4bca6"
{
    "message":"create user successful",
    "result":"SUCCESS"
}
```

异常处理
======
>该框架的异常处理分为2类，分别为已知异常和未知异常，2类异常处理均利用http error code进行处理,代码块在base/__init__.py下，新增异常在里面加即可

* 500 内部错误
* 401 认证错误
* 400 参数错误


日志处理
======
>服务在启动时候会默认全局加载logging,日志格式为 日志级别 【代码文件-类-方法】 内容

```
2019-08-08 16:13:59,007 INFO [user.py=>user=>createuser]: create user zyx3
```

接口规范说明
=======
>接口返回均以为Json 格式返回，如果返回失败，则封装的异常返回为{'status':'failed','message':'XXXX'},默认使用的接口返回都会带status字段，基于该字段判断返回是否成功，成功后再判断其他字段

框架结构说明
======
>项目的安装基于pbr打包部署，配置文和打包脚本在项目根目录下的setup.py和setup.cfg实际使用中,更新之前请删除之前的egg包以及可执行的二进制可执行文件命令如下:
```
pip uninstall wind-server
```
>项目基于mvc原则，目录结构如下:
* api : 所有api路由全在该目录下编写，基于blueprint 注册是flask APP上
* base: flask 初始化代码，在服务启动中会在此初始化日志和配置文件以及对应的HTTP服务，以及request拦截处理和异常处理
* cmd: 可执行文件
* controller: 具体业务逻辑层，在此目录下进行业务逻辑的实际封装
* dao: 数据层，sql编写在该目录
* utils: 通用工具集合，放置一些基础工具，如日志封装，数据库封装，redis封装等等





