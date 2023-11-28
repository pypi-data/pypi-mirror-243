#!/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: __main__
@time: 2023/10/24
@contact: ybyang7@iflytek.com
@site:  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛ 
"""

#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import psutil
import subprocess

pid = 1

def checkPortAlive(pid :int) -> bool:
    try:
        p = psutil.Process(pid)
        ports = [conn.laddr.port for conn in p.connections() if conn.status == psutil.CONN_LISTEN]
        if not ports:
            print("AIservice Port not up!")
            exit(-1)
        else:
            print("AIservice Port %s" % str(ports))
            port = ports[0]
            rpc_checker_cmd = f"/home/aiges/live_check -port {port}"
            ret = subprocess.call(rpc_checker_cmd, shell=True)
            exit(ret)
    except Exception as e:
        print(str(e))
        exit(-1)

if __name__ == '__main__':
    checkPortAlive(pid)