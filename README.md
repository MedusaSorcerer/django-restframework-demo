# 实战讲解 Django-rest-framework JWT用户认证开发
我们用 `Django` 和 `rest-framework` 开发用户模块,
并使用 `JWT(Json Web Token)` 进行用户认证<br>
[前往我的掘金 juejin.im@MedusaSorcerer](https://juejin.im/post/5ee429826fb9a047af565027)

> 开发环境：Windows10<br>
> 开发 IDE：Pycharm<br>
> 开发框架：Django<br>
> 开发语言：Python

### requirements
```requirements.txt
python==3.8.2
django==3.0.6
django-restframework
django-restframesork-jwt
```

### 创建 Django 项目
在 `CMD` 命令行界面,
创建 `Django` 项目程序 `Medusa`：
```shell script
python3 -m django startproject Medusa
```
在 `Medusa` 根目录下创建应用总模块 `applications`：
```shell script
cd Medusa
mkdir applications
```
进入 `applications` 创建应用模块 `User`,
这儿采用傻瓜式操作,
创建层级 `Django-APP`：
```shell script
cd applications
python3 ../manage.py startapp User
```
此时项目结构如下：
![](https://user-gold-cdn.xitu.io/2020/6/13/172ab4e4e9765998)

### 修改配置
修改 `applications/User/apps.py`：
```python
from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'applications.User'
```
在项目根目录新建配置文件夹 `config`,
并添加配置文件 `config.py`：
```shell script
cd ..
mkdir config
cd config
type NUL > config.py
```
在 `config/config.py` 新增以下配置内容：
```python
#!/usr/bin/env python
# _*_ Coding: UTF_8 _*_

# MySQL 服务地址
MYSQL_SERVER_HOST = '127.0.0.1'

# MySQL 服务端口
MYSQL_SERVER_PORT = '3306'

# MySQL 数据库名称
MYSQL_DATABASE_NAME = 'medusa'

# MySQL 数据库连接用户账号
MYSQL_SERVER_USERNAME = 'root'

# MySQL 数据库连接用户密码
MYSQL_SERVER_PASSWORD = 'mysql-password'
```
修改 `Medusa/settings.py` 中配置参数 `ALLOWED_HOSTS`：
```python
ALLOWED_HOSTS = ['*']
```
添加 `Medusa/settings.py` 中应用注册参数 `INSTALLED_APPS`：
```python
INSTALLED_APPS = [
    ...,
    'applications.User',
]
```
在 `Medusa/settings.py` 顶部导入配置文件：
```python
from config import config
```
在 `Medusa/setting.py` 中修改配置数据库参数 `DATABASES`：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.MYSQL_DATABASE_NAME,
        'USER': config.MYSQL_SERVER_USERNAME,
        'PASSWORD': config.MYSQL_SERVER_PASSWORD,
        'HOST': config.MYSQL_SERVER_HOST,
        'PORT': config.MYSQL_SERVER_PORT,
    }
}
```
在 `Medusa/setting.py` 中修改配置时区参数 `TIME_ZONE`:
```python
TIME_ZONE = 'Asia/Shanghai'
```
当然你可以继续在 `Medusa/settings.py` 修改语言参数,
我们创建的项目暂不修改：
```python
LANGUAGE_CODE = 'zh-hans'
```
确保你的 `MySQL` 中已经存在了你配置的数据库名称对应的数据库,
并且可以连接成功,
就可以尝试在 `Medusa` 根目录下启动 `Django` 项目,：
```shell script
python3 manage.py runserver 0.0.0.0:8000
```
你如果执行成功你可以访问 [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 就看到以下界面：
![](https://user-gold-cdn.xitu.io/2020/6/13/172ab4ead990289c)

### 创建 User 模型
在 `applications/User/models.py` 中自定义我们的用户模型类
```python
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = 'medusa_user'
        ordering = ('-id',)
```
我们采用的是继承 `AbstractUser` 类并指定 `db_table` 的方式,
此时你可以使用 `Pycharm` 的 `Ctrl + B` 进入父类中查看 `User` 具有的属性和方法。

当然了,
在执行到这个步骤的时候其实用户的模型类并没有生效,
而需要达到生效的效果则是需要指定用户模型类的位置参数,
你只需要在 `Medusa/settings.py` 中用 `AppName.UserModelsName` 的方式指定用户模型类即可：
```python
AUTH_USER_MODEL = 'User.User'
```
有关于用户认证的模型类介绍,
推荐你查阅 [Customizing authentication in Django](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/)。

使用 Django 迁移命令迁移数据库生成数据表：
```shell script
python3 manage.py makemigrations
python3 manage.py migrate
```
你可以使用 `MySQL` 数据库连接应用查看你生成的数据表。

### 登录认证
在准备好基本环境后我们进行登录接口的开发工作,
登录的接口主要是对用户进行验证以及口令的返回,
使用 `JWT` 验证的时候先安装导入需要的包应用 `rest_framework`,
添加 `Medusa/settings.py` 中应用注册参数 `INSTALLED_APPS`：
```python
INSTALLED_APPS = [
    ...,
    'rest_framework',
]
```
在 `applications/User/` 下创建用户认证的视图文件 `userauth.py` 并撰写用户登录认证视图类：
```python
#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView


class UserLoginAPIView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer
```
简简单单的几行代码就实现了一个用户登录的接口,
你现在就需要在你的路由管理器里面注册这个登录的 API 试图即可,
在 `Medusa/urls.py` 中 `urlpatterns` 参数中注册路由：
```python
urlpatterns = [
    path('api/v1.0.0/user/login', userauth.UserLoginAPIView.as_view())
]
```
不要着急,
我们是不是还没有创建用户呢？
```shell script
python3 manage.py createsuperuser
```
依次输入：
1. Username
2. Email address
3. Password
4. Password(again)

因为我输入的密码是 `admin`,
所以在创建的时候给了三个警告信息,
需要你确认信息后再次确认：
```text
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
```
* 密码和用户名的相似度过高
* 密码长度太短, 应该至少是八个字符
* 密码属于弱密码

不管他,
上去就是一个 `y` 给他：
![](https://user-gold-cdn.xitu.io/2020/6/13/172ab4f273d51945)
是时候启动服务测试下我们的代码成果了：
![](https://user-gold-cdn.xitu.io/2020/6/13/172ab4f83b104a8e)

### 登录注销
对于已经登录的用户实现登出功能,
主要的是在于登录的一种身份判断,
那等同于一个唯一字段能实现判断登录用户登出后变化,
并且重新生成这个唯一字段。

我们在 `User` 类中加入这样一条字段配置：
```python
from uuid import uuid4

user_secret = models.UUIDField(default=uuid4())
```
注意 `user_secret` 是 `User` 类的一个属,
你可能会想那我是不是要重新实现哟用户登录的逻辑呢？
答案是不需要的,
因为我们创建的字段,
我们用函数路径的方式指定原先的函数,
我们将采用重写原本的判断函数即可实现：

在项目根目录下的 `applications/User/views.py` 中创建函数,
函数位置可自行确定,
你也可以创建一个 `.py` 文件： 
```python
#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_


def get_user_secret(user):
    return user.user_secret
```
主要的内容是在 `Medusa/settings.py` 中配置函数路径：
```python
JWT_AUTH = {
    'JWT_GET_USER_SECRET_KEY': 'applications.User.views.get_user_secret'
}
```
因为我们修改了模型类,
所以我们需要对数据库进行再次迁移：
```shell script
python3 manage.py makemigrations
python3 manage.py migrate
```
在 `applications/User/userauth.py` 中创建登出视图：
```python
import uuid

from rest_framework import status, views
from rest_framework.response import Response


class UserLogoutAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user.user_secret = uuid.uuid4()
        user.save()
        return Response({'detail': 'login out.', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
```
在路由模块 `Medusa/urls.py` 中注册：
```python
urlpatterns = [
    ... ,
    path('api/v1.0.0/user/logout', userauth.UserLogoutAPIView.as_view()),
]
```
测试一下：
```error
NotImplementedError: Django doesn't provide a DB representation for AnonymousUser.
```
What?
报错了,
因为我们访问 API 的时候没有使用认证信息,
所以访问的 User 对象是一个匿名用户对象,
所以我们需要对这个接口采取认证：
```python
from rest_framework.permissions import IsAuthenticated


class UserLogoutAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        ...
```
添加认证参数 `permission_classes` 表示需要 `IsAuthenticated` 已认证的对象才可以访问,
再次尝试接口会收到以下 `json` 提示：
```json
{
    "detail": "Authentication credentials were not provided."
}
```
认证失败？
我们在 `Medusa/settings.py` 中添加以下配置信息：
```python
import datetime


JWT_AUTH = {
    # 之前配置的用户依据判断函数路由
    'JWT_GET_USER_SECRET_KEY': 'applications.User.views.get_user_secret',
    
    # 用户认证数据的过期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1)
}
REST_FRAMEWORK = {
    # 用户认证类
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
```
![](https://user-gold-cdn.xitu.io/2020/6/13/172ab50b221ef018)
```json
{
    "detail": "login out.",
    "status": 200
}
```

### 创建用户
在创建用户的时候我们不会使用命令行来创建用户的,
使用模型类的时候创建用户一般会这样来实现,
当然了,
这儿我们省略了一些操作,
仅仅介绍创建用户的快捷方式：
```python
from applications.User.models import User


User.objects.create_user(username=username, email=email, password=password, **extra_fields)
User.objects.create_superuser(username=username, email=email, password=password, **extra_fields)
```