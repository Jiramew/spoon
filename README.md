# Spoon - A package for building specific Proxy Pool for different URLs.
Spoon is a library for building Proxy Pool for each different URLs as you assign.      
Only running on python 3.

## Run

### Spoon-server
Please make sure the Redis is running. Default configuration is "host:localhost, port:6379"      
Like `example.py` in `spoon_server/example`,      
You can assign many different proxy provider.
```python
from spoon_server.proxy.fetcher import Fetcher
from spoon_server.main.proxy_pipe import ProxyPipe
from spoon_server.proxy.us_provider import UsProvider


def main_run():
    p1 = ProxyPipe(url_prefix="https://www.google.com", fetcher=Fetcher(use_default=False)).set_fetcher([UsProvider()])
    p1.start()

if __name__ == '__main__':
    main_run()
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
          <td>KuaiPayProvider</td>
          <td>Get proxy from http api</td>
        </tr>
        <tr>
          <td>FileProvider</td>
          <td>Get proxy from file</td>
        </tr>
        <tr>
          <td>GouProvider</td>
          <td>www.goubanjia.com</td>
        </tr>
        <tr>
          <td>KuaiProvider</td>
          <td>www.kuaidaili.com</td>
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
          <td>YouProvider</td>
          <td>http://www.youdaili.net</td>
        </tr>
    </tbody>
</table>

### Spoon-web
A Simple django web api.          
Gently run `python manager.py runserver ******:******`      
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
          <td>http://127.0.0.1:21010/api/v1/fetchall_from?target=www.google.com&filter=65</td>
          <td>Get one useful proxy. <br>target: the specific url<br> filter: successful-revalidate times</td>
        </tr>
        <tr>
          <td>http://127.0.0.1:21010/api/v1/fetchall_from?target=www.google.com&filter=65</td>
          <td>Get all useful proxy.</td>
        </tr>
    </tbody>
</table>
