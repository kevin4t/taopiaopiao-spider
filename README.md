# taopiaopiao-spider

自动爬取淘票票<已看电影和自己写的影评>(其中包括自己购过票的和未购票但进行过评分的电影)并更新至Hexo博客

效果预览：[Tangerinew.](https://tangerinew.com/keep/index.html)

![1572141255208](https://github.com/kevin4t/taopiaopiao-spider/blob/master/README/1572141255208.png?raw=true)

### Server

运行于服务器端:

修改get_cookie.py中的账号密码：

```python
def get_init_cookie():
    # 淘宝用户名
    username = 'YourUsername'
    # 淘宝重要参数，从浏览器或抓包工具中复制，可重复使用
    ua = ua = 'YourUa'
    # 加密后的密码，从浏览器或抓包工具中复制，可重复使用
    TPL_password2 = 'YourPassword'
    ul = UsernameLogin(username, ua, TPL_password2)
    ul.login()
```

*登录地址:https://login.taobao.com/member/login.jhtml,可以用于抓包。*

在终端运行app.py:

```bash
$ python app.py
```

### Client

在Hexo项目文件夹下Source文件夹下新建一个文件夹，名称自定，并将Client内的文件全部放置于其中。

### 更新Hexo博客

```bash
$ hexo g
$ hexo d
```

