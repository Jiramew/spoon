import json
import time
import random
from django.http import HttpResponse

from spoon_server.database.redis_config import RedisConfig
from spoon_server.main.manager import Manager

redis = RedisConfig("127.0.0.1", 6379, 0)


def get_keys(request):
    m = Manager(database=redis)
    return HttpResponse(json.dumps(m.get_keys()))


def fetchone_from(request):
    m = Manager(database=redis)
    target_name = request.GET.get("target", "www.baidu.com")
    filter_num = int(request.GET.get("filter", 10))
    search_name = ":".join(["spoon", target_name, "useful_proxy"])

    px_kv = m.get_all_kv_from(search_name)
    res_list = random.sample([k.decode('utf-8') for (k, v) in px_kv.items() if int(v.decode('utf-8')) > filter_num], 1)

    return HttpResponse(res_list[0])


def fetchall_from(request):
    m = Manager(database=redis)
    target_name = request.GET.get("target", "www.baidu.com")
    filter_num = int(request.GET.get("filter", 10))
    search_name = ":".join(["spoon", target_name, "useful_proxy"])

    px_kv = m.get_all_kv_from(search_name)
    res_list = [k.decode('utf-8') for (k, v) in px_kv.items() if int(v) > filter_num]

    return HttpResponse("\r\n".join(res_list))


def fetch_hundred_recent(request):
    m = Manager(database=redis)
    target_name = request.GET.get("target", "www.baidu.com")
    filter_num = int(request.GET.get("filter", 30))
    search_name = ":".join(["spoon", target_name, "hundred_proxy"])

    px_kv = m.get_all_kv_from(search_name)
    res_list = [k.decode('utf-8') for (k, v) in px_kv.items() if
                abs(float(v.decode('utf-8')) - time.time()) < filter_num]
    return HttpResponse("\r\n".join(res_list))


def fetch_stale(request):
    m = Manager(database=redis)
    num = int(request.GET.get("num", 100))
    px_kv = m.get_all_kv_from("spoon:proxy_stale")
    res_list_pre = [[k.decode('utf-8'), float(v.decode('utf-8'))] for (k, v) in px_kv.items()]
    res_list = [k for [k, _] in sorted(res_list_pre, key=lambda item: -item[1])][0:num]

    return HttpResponse("\r\n".join(res_list))


def fetch_recent(request):
    m = Manager(database=redis)
    target_name = request.GET.get("target", "www.baidu.com")
    px_list = m.get_range_from(":".join(["spoon", target_name, "current_proxy"]))
    res_list = [px.decode('utf-8') for px in px_list]

    return HttpResponse("\r\n".join(res_list))
