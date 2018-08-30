import re
import socks
import signal
import socket
import random
import threading

from spoon_server.util.logger import log
from spoon_server.main.manager import Manager
from spoon_server.database.redis_config import RedisConfig

is_exit = False


class ForwardServer(object):
    PAGE_SIZE = 4096

    def __init__(self, redis_):
        self.listen_host = None
        self.listen_port = None
        self.remote_host = None
        self.remote_port = None
        self.default_remote_host = None
        self.default_remote_port = None
        self.m = Manager(database=redis_)

    def set_listen(self, host, port):
        self.listen_host = host
        self.listen_port = port
        return self

    def set_default_remote(self, host, port):
        self.default_remote_host = host
        self.default_remote_port = port
        return self

    def set_remote(self, host, port):
        self.remote_host = host
        self.remote_port = port
        return self

    def _listen(self):
        sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp
        sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_server.bind((self.listen_host, self.listen_port))
        sock_server.listen(5)
        log.info('Listening at %s:%d ...' % (self.listen_host, self.listen_port))
        return sock_server

    def serve(self):
        sock_server = self._listen()

        while not is_exit:
            try:
                sock, addr = sock_server.accept()
            except (KeyboardInterrupt, SystemExit):
                log.warn('Closing...')
                sock_server.shutdown(socket.SHUT_RDWR)
                sock_server.close()
                break
            except Exception as e:
                log.error('Exception exit {0}'.format(e))
                sock_server.shutdown(socket.SHUT_RDWR)
                sock_server.close()
                break

            threading.Thread(target=self._forward, args=(sock,)).start()
            log.info('New clients from {0}'.format(addr))

        log.info('exit server')

    def _forward(self, sock_in):
        try:
            sock_out = ForwardClient()
            log.info('get the client socks done')
        except Exception as e:
            log.error('Get Remote Client error: %s' % str(e))
            raise e

        threading.Thread(target=self._do_data_forward, args=(sock_in, sock_out)).start()
        threading.Thread(target=self._do_data_forward, args=(sock_out, sock_in)).start()

    def _do_data_forward(self, sock_in, sock_out):
        if isinstance(sock_in, ForwardClient):
            sock_in = sock_in.get_client(self.default_remote_host, self.default_remote_port)

        addr_in = '%s:%d' % sock_in.getpeername()

        while True:
            try:
                data = sock_in.recv(ForwardServer.PAGE_SIZE)
                if isinstance(sock_out, ForwardClient):
                    print("sock_in", data)
                    if b'Host' in data:
                        host_match = re.match(r'.*Host:\s(.*?)\r\n.*', data.decode("utf-8"), re.S)
                        if host_match:
                            hostname = host_match[1]
                            current_proxy_list = self.m.get_range_from(":".join(["spoon", hostname, "current_proxy"]))
                            if current_proxy_list:
                                ran_num = random.randint(0, len(current_proxy_list) // 3)
                                proxy = current_proxy_list[ran_num].decode("utf-8")
                                sock_out = sock_out.get_client(proxy.split(":")[0], int(proxy.split(":")[1]))
                                log.info("Change Remote Proxy: {0}".format(proxy))
                            else:
                                log.info("Change Remote Proxy: ",
                                         self.default_remote_host + ":" + self.default_remote_port)
                                sock_out = sock_out.get_client(self.default_remote_host, self.default_remote_port)
                    sock_out = sock_out.get_client(self.default_remote_host, self.default_remote_port)
            except Exception as e:
                if isinstance(sock_out, ForwardClient):
                    sock_out = sock_out.get_client(self.default_remote_host, self.default_remote_port)
                log.error('Socket read error of %s: %s' % (addr_in, str(e)))
                break

            if not data:
                log.info('Socket closed by ' + addr_in)
                break

            addr_out = '%s:%d' % sock_out.getpeername()

            try:
                sock_out.sendall(data)
            except Exception as e:
                log.error('Socket write error of %s: %s' % (addr_out, str(e)))
                break

            log.info('%s -> %s (%d B)' % (addr_in, addr_out, len(data)))

        sock_in.close()
        sock_out.close()


class ForwardClient(object):
    @staticmethod
    def get_client(remote_host, remote_port):
        sock_out = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print('remote,=', (remote_host, remote_port))
            sock_out.connect((remote_host, remote_port))
        except socket.error as e:
            sock_out.close()
            log.error('Remote connect error: %s' % str(e))
            raise Exception('Remote connect error: %s' % str(e))

        return sock_out


def handler(signum, frame):
    print(signum, frame)
    global is_exit
    is_exit = True
    print("receive a signal %d, is_exit = %d" % (signum, is_exit))


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    listen = ("127.0.0.1", 12001)
    default_remote = ("47.93.234.57", 42251)

    redis = RedisConfig("10.1.10.10", 6379, 0, 123456)

    serv = ForwardServer(redis)
    serv.set_listen(listen[0], listen[1])
    serv.set_default_remote(default_remote[0], default_remote[1])
    serv.serve()
