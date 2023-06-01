fork自大神 [flask-restful-example](https://github.com/qzq1111/flask-restful-example)

因自己需求仅保留了部分功能模块：包含基本的项目配置、统一响应、MySQL和Redis数据库操作、项目部署、用户权限认证等模块。

添加：


### 1. 拉取代码
- 切换到`/projects`目录(没有就先新建目录`sudo mkdir /projects`)，执行命令`cd /projects`
- 执行命令`sudo git clone https://github.com/qzq1111/flask-restful-example.git`拉取代码
- 切换到`/projects/flask-restful-example`目录，执行命令`cd /projects/flask-restful-example`
       
### 2. 构建镜像
- 在当前目录`/projects/flask-restful-example`中构建镜像
- 执行命令`sudo docker build . -t=flask-restful-example:latest`构建，等待构建完成
- 执行命令`sudo docker images`，查询构建好的镜像`flask-restful-example`

### 3. 运行容器
- 在当前目录`/projects/apiwong-mini`中运行容器
- 执行命令`sudo docker-compose up -d`
- 执行命令`sudo docker ps`查询容器是否运行

### 4. 配置修改

#### 4.1 config/config.yaml配置
- SQLALCHEMY_DATABASE_URI：数据连接
- REDIS_HOST：Redis连接，此处如果使用的是docker-compose的link，修改为对应服务名称默认为`rediswong`
    
#### 4.2 docker-compose配置
- image：构建的镜像名称
- container_name：启动之后容器名称
- ports：容器端口与宿主端口映射
- volumes：容器内部文件与宿主文件映射（持久化）
- links：链接的容器，容器之间使用服务名访问

#### 4.3 gun.conf配置
- bind：flask启动端口。一般不用修改，服务在容器内启动的。
- worker_class：flask启动的模式，有许多支持启动的方式，按需取舍。

#### 4.4 nginx配置
```
server {
        listen       5000;
        server_name  localhost;

        # api代理转发
        location /api {
            proxy_redirect  off;
            proxy_set_header    Host $host;
            proxy_set_header    X-Real-IP            $remote_addr;
            proxy_set_header    X-Forwarded-For      $proxy_add_x_forwarded_for;
            proxy_set_header    X-Forwarded-Proto    $scheme;
            proxy_pass http://127.0.0.1:3010/api;
        }
    } 
```
### 5.备注
- 修改配置文件之后最好重启容器，`sudo docker-compose restart`
