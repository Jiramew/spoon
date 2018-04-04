import base64
import requests

from spoon_server.util.logger import log
from spoon_server.util.constant import HEADERS


class Captcha(object):
    def __init__(self, crack_url):
        self.crack_url = crack_url

    def get_image_result(self, image_url):
        try:
            ir = requests.get(image_url, headers=HEADERS, timeout=10)
        except Exception as e:
            log.error("Error fetching captcha {0}".format(e))
            raise Exception(e)

        if ir.status_code == 200:
            post_data = {"image": base64.b64encode(ir.content)}
            res = requests.post(self.crack_url, data=post_data)
            answer = str(res.content, encoding="utf-8")
            return answer
        else:
            log.error("Error cracking captcha {0}".format(ir.status_code))
            raise Exception("Error cracking captcha {0}".format(ir.status_code))
