#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import threading
import sys
import re

import spoon_server.forward.forward as forward

from spoon_server.util.logger import log


def pid_exists(pid):
    """
    from http://stackoverflow.com/questions/568271/how-to-check-if-there-exists-a-process-with-a-given-pid
    """
    if os.name == 'posix':
        """Check whether pid exists in the current process table."""
        import errno
        if pid < 0:
            return False
        try:
            os.kill(pid, 0)
        except OSError as e:
            return e.errno == errno.EPERM
        else:
            return True
    else:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        SYNCHRONIZE = 0x100000

        process = kernel32.OpenProcess(SYNCHRONIZE, 0, pid)
        if process != 0:
            kernel32.CloseHandle(process)
            return True
        else:
            return False


def run_proxy(local_addr, local_port,
              remote_addr, remote_port):
    serv = forward.ForwardServer()
    print(local_addr, local_port,
          remote_addr, remote_port)
    serv.setListen(local_addr, local_port) \
        .setRemote(remote_addr, remote_port)
    serv.serve()


def start():
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            log.info('parent process exit')
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)

        # write pid
    pid = str(os.getpid())
    pidfile = "./proxy_daemon.pid"

    if os.path.isfile(pidfile):
        f = open(pidfile, 'r')
        file_pid = int(f.read())
        log.info('read pid file pid=%s' % file_pid)
        if pid_exists(file_pid):
            log.info("%s already exists, and pid=%s exists exiting" %
                     (pidfile, file_pid))
            sys.exit(1)
        else:
            log.info('the pid file pid=%s not exists' % file_pid)
        f.close()

    open(pidfile, 'w').write(pid)
    log.info('write pid to %s' % pidfile)

    log.info('now is child process do')

    re_ip_port = r'^(?P<addr>.+:)?(?P<port>[0-9]{1,5})$'

    listen = "127.0.0.1:12001"
    remote = "119.39.48.205:9090"

    local_addr, local_port = None, None
    remote_addr, remote_port = None, None

    x = re.match(re_ip_port, listen)
    if not x:
        log.info('listen format error!')
        sys.exit(1)
    local_addr = x.group('addr') or '0.0.0.0'
    local_addr = local_addr.rstrip(':')
    local_port = int(x.group('port'))

    x = re.match(re_ip_port, remote)
    if not x:
        log.info('listen format error!')
        sys.exit(1)
    remote_addr = x.group('addr') or '0.0.0.0'
    remote_addr = remote_addr.rstrip(':')
    remote_port = int(x.group('port'))

    threading.Thread(
        target=run_proxy,
        args=(local_addr, local_port,
              remote_addr, remote_port)
    ).start()

    log.info('start all proxy done')


def exit():
    pidfile = "./proxy_daemon.pid"
    os.remove(pidfile)
    log.info('exit')


def help():
    print('Usage: %s Command [Option]' % sys.argv[0])
    print('Command List:')
    print('start   根据配置启动worker')
    print('stop    停止所有worker')
    print('restart 重新启动所有worker')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        cmd = 'help'
    else:
        cmd = sys.argv[1]
    eval(cmd)()
