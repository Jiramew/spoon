# Spoon - A package for building specific Proxy Pool for different Sites.
Spoon is a library for building Distributed Proxy Pool for each different sites as you assign.      
Only running on python 3.

## Install
Simply run: `pip install spoonproxy` or clone the repo and set it into your PYTHONPATH.
    
## Run

### Spoon-server
Please make sure the Redis is running. Default configuration is "host:localhost, port:6379". You can also modify the Redis connection.      
Like `example.py` in `spoon_server/example`,      
You can assign many different proxy providers.
```python
from spoon_server.proxy.fetcher import Fetcher
from spoon_server.main.proxy_pipe import ProxyPipe
from spoon_server.proxy.kuai_provider import KuaiProvider
from spoon_server.proxy.xici_provider import XiciProvider
from spoon_server.database.redis_config import RedisConfig
from spoon_server.main.checker import CheckerBaidu

def main_run():
    redis = RedisConfig("127.0.0.1", 21009)
    p1 = ProxyPipe(url_prefix="https://www.baidu.com",
                   fetcher=Fetcher(use_default=False),
                   database=redis,
                   checker=CheckerBaidu()).set_fetcher([KuaiProvider()]).add_fetcher([XiciProvider()])
    p1.start()


if __name__ == '__main__':
    main_run()
```

Also, with different checker, you can validate the result precisely.
```python
class CheckerBaidu(Checker):
    def checker_func(self, html=None):
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        if re.search(r".*百度一下，你就知道.*", html):
            return True
        else:
            return False
```

Also, as the code shows in `spoon_server/example/example_multi.py`, by using multiprocess, you can get many queues to fetching & validating the proxies.       
You can also assign different Providers for different url.      
The default proxy providers are shown below, you can write your own providers.             
<table class="table table-bordered table-striped">
    <thead>
    <tr>
        <th style="width: 100px;">name</th>
        <th style="width: 100px;">description</th>
    </tr>
    </thead>
    <tbody>
        <tr>
          <td>WebProvider</td>
          <td>Get proxy from http api</td>
        </tr>
        <tr>
          <td>FileProvider</td>
          <td>Get proxy from file</td>
        </tr>
        <tr>
          <td>GouProvider</td>
          <td>http://www.goubanjia.com</td>
        </tr>
        <tr>
          <td>KuaiProvider</td>
          <td>http://www.kuaidaili.com</td>
        </tr>
        <tr>
          <td>SixProvider</td>
          <td>http://m.66ip.cn</td>
        </tr>
        <tr>
          <td>UsProvider</td>
          <td>https://www.us-proxy.org</td>
        </tr>
        <tr>
          <td>WuyouProvider</td>
          <td>http://www.data5u.com</td>
        </tr>
        <tr>
          <td>XiciProvider</td>
          <td>http://www.xicidaili.com</td>
        </tr>
        <tr>
          <td>IP181</td>
          <td>http://www.ip181.com</td>
        </tr>
        <tr>
          <td>XunProvider</td>
          <td>http://www.xdaili.cn</td>
        </tr>
        <tr>
          <td>PlpProvider</td>
          <td>https://list.proxylistplus.com</td>
        </tr>
        <tr>
          <td>IP3366Provider</td>
          <td>http://www.ip3366.net</td>
        </tr>
        <tr>
          <td>BusyProvider</td>
          <td>https://proxy.coderbusy.com</td>
        </tr>
        <tr>
          <td>NianProvider</td>
          <td>http://www.nianshao.me</td>
        </tr>
        <tr>
          <td>PdbProvider</td>
          <td>http://proxydb.net</td>
        </tr>
        <tr>
          <td>GPProvider(@NeedProxy if you're in China)</td>
          <td>http://www.gatherproxy.com</td>
        </tr>
        <tr>
          <td>FPLProvider(@NeedProxy if you're in China)</td>
          <td>https://free-proxy-list.net</td>
        </tr>
        <tr>
          <td>SSLProvider(@NeedProxy if you're in China)</td>
          <td>https://www.sslproxies.org</td>
        </tr>
        <tr>
          <td>NordProvider(@NeedProxy if you're in China)</td>
          <td>https://nordvpn.com</td>
        </tr>
        <tr>
          <td>YouProvider(@Deprecated)</td>
          <td>http://www.youdaili.net</td>
        </tr>
    </tbody>
</table>

### Spoon-web
A Simple django web api demo. You could use any web server and write your own api.           
Gently run `python manager.py runserver **.**.**.**:*****`      
The simple apis include:
<table class="table table-bordered table-striped">
    <thead>
    <tr>
        <th style="width: 100px;">name</th>
        <th style="width: 100px;">description</th>
    </tr>
    </thead>
    <tbody>
        <tr>
          <td>http://127.0.0.1:21010/api/v1/get_keys</td>
          <td>Get all keys from redis</td>
        </tr>
        <tr>
          <td>http://127.0.0.1:21010/api/v1/fetchone_from?target=www.google.com&filter=65</td>
          <td>Get one useful proxy. <br>target: the specific url<br> filter: successful-revalidate times</td>
        </tr>
        <tr>
          <td>http://127.0.0.1:21010/api/v1/fetchall_from?target=www.google.com&filter=65</td>
          <td>Get all useful proxies.</td>
        </tr>
        <tr>
          <td>http://127.0.0.1:21010/api/v1/fetch_hundred_recent?target=www.baidu.com&filter=5</td>
          <td>Get recently joined full-scored proxies. <br>target: the specific url<br> filter: time in seconds</td>
        </tr>
        <tr>
          <td>http://127.0.0.1:21010/api/v1/fetch_stale?num=100</td>
          <td>Get recently proxies without check. <br>num: the specific number of proxies you want</td>
        </tr>
        <tr>
          <td>http://127.0.0.1:21010/api/v1/fetch_recent?target=www.baidu.com</td>
          <td>Get recently proxies that successfully validated. <br>target: the specific url</td>
        </tr>
    </tbody>
</table>
