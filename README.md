# taopiaopiao-spider

自动爬取淘票票<已看电影和自己写的影评>(其中包括自己购过票的和未购票但进行过评分的电影)并更新至Hexo博客

效果预览：[Tangerinew.](https://tangerinew.com/keep/index.html)

![1572141255208](https://raw.githubusercontent.com/kevin4t/taopiaopiao-spider/master/README/1572142341234.png)

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

修改index.html中Ajax请求的地址，换成自己的服务器。

```js
function loadMoviesWatched() {
	$.ajax({
		url: 'YourUrl',//替换成你自己的请求地址
		dataType:'json',//服务器返回json格式数据
		type:'get',//HTTP请求类型
		timeout:10000,//超时时间设置为10秒；
		success:function(data){
			...
		}
	})
}
```

`注意：在服务器端需要使用Nginx将443端口反向代理到此进程运行的5000端口。因为与GitPage绑定的Hexo为https协议，其只能向https请求信息，若服务器未绑定域名且未申请证书，则请求失败。`

### 更新Hexo博客

```bash
$ hexo g
$ hexo d
```

