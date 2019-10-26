import time
from hashlib import md5
import requests
import json
import get_cookie
sess = requests.Session()


class TaoPiaoPiao:
    def __init__(self, Cookie):
        """
        :param Cookie
        """
        self.Cookie = Cookie
        self.get_data_url = 'https://acs.m.taobao.com/h5/mtop.film.mtopshowapi.getwatchedshow/6.8/'
        self.jsv = '2.5.1'
        self.appKey = '12574478'
        self.api = 'mtop.film.mtopshowapi.getwatchedshow'
        self.v = '6.8'
        self.timeout = 10000
        self.forceAntiCreep = 'true'
        self.AntiCreep = 'true'
        self.type = 'jsonp'
        self.dataType = 'jsonp'
        self.callback = 'mtojsonp2'
        # pageSize用来表示单次请求的电影数量, 为了尽量一次获取完,设置尽可能高
        self.data = '{"ecode":1,"pageSize":100,"currentPage":1,"lastId":0,"platform":"8"}'
        # 获取时间戳
        self.t = self.get_time()
        # 计算sign
        self.sign = self.get_sign()

    def get_time(self):
        """
        获取时间戳
        :return: 当前时间的时间戳
        """
        now = time.time()
        t = int(round(now * 1000))  # 毫秒
        return str(t)

    def get_sign(self):
        """
        计算sign
        :return: sign
        """
        # 获取Cookie中的token
        cookie_list = self.Cookie.split(';')
        _m_h5_tk = ""
        for item in cookie_list:
            item = item.strip()
            kv = item.split('=')
            if kv[0] == '_m_h5_tk':
                _m_h5_tk = kv[1]
        token = _m_h5_tk.split('_')[0]
        # 计算sign
        s = token+'&'+self.t+'&'+self.appKey+'&'+self.data
        sign = self.encrypt_md5(s)
        return sign

    def encrypt_md5(self, s):
        """
        md5加密字符串
        :return: md5码
        """
        # 创建md5对象
        new_md5 = md5()
        # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
        new_md5.update(s.encode(encoding='utf-8'))
        # 加密
        return new_md5.hexdigest()

    def get_data(self):
        """
        发送请求获取数据
        :return: data
        """
        get_data_headers = {
            'Host': 'acs.m.taobao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Connection': 'keep-alive',
            'Cookie': self.Cookie,
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        get_data_params = {
            'jsv': self.jsv,
            'appKey': self.appKey,
            't': self.t,
            'sign': self.sign,
            'api': self.api,
            'v': self.v,
            'timeout': self.timeout,
            'forceAntiCreep': self.forceAntiCreep,
            'AntiCreep': self.AntiCreep,
            'type': self.type,
            'dataType': self.dataType,
            'callback': self.callback,
            'data': self.data
        }
        try:
            response = sess.get(self.get_data_url, headers=get_data_headers, params=get_data_params,
                                timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print('请求失败：')
            raise e
        return response.text


class Cookie:
    def __init__(self):
        self.cookie = ""
        self.load_cookie()
        self.add_token()

    def load_cookie(self):
        """
        加载Cookie
        :return: cookie
        """
        get_cookie.get_init_cookie()
        with open(r'taobao_login_cookies.txt', 'r') as f:
            cookie_str = f.read()
            cookie_to_dict = json.loads(cookie_str)
            items = cookie_to_dict.items()
            for k, v in items:
                self.cookie += k+'='+v+';'

    def add_token(self):
        """
        为Cookie添加_m_h5_th字段
        :return: cookie
        """
        get_data_headers = {
            'Host': 'acs.m.taobao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Connection': 'keep-alive',
            'Cookie': self.cookie,
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        response = sess.get('https://acs.m.taobao.com/h5/mtop.alimama.union.hsf.mama.coupon.get/1.0/?appKey=12574478&v=1', headers=get_data_headers,
                            timeout=10000)
        new_cookie = response.cookies.get_dict()
        for k, v in new_cookie.items():
            self.cookie += k+'='+v+';'

    def get_cookie(self):
        """
        获取cookie
        """
        return self.cookie


def refresh_data():
    cookie = Cookie().get_cookie()
    TPP = TaoPiaoPiao(cookie)
    raw_data = TPP.get_data()
    print("更新数据成功！")
    return raw_data[11:-1]
