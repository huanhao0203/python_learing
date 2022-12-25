#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:victor Li
 
#任务类
import queue
import gevent

print('sss')
 
from locust import  HttpUser, task
class TestUser(HttpUser):
    host="www.baidu"
    out_queue=queue.Queue(20)
    max_wait = 1
    min_wait = 1
    my_queue=queue.Queue(20)
    for i in range(20):
        my_queue.put(i)
    @task
    def test_001(self):
 
        if not self.my_queue.empty() and  self.out_queue.empty():
            num= self.my_queue.get()
            self.my_queue.task_done()
            if self.my_queue.empty():
               pass
            else:
                self.my_queue.join()
            print("执行了呀{}".format(num))
            self.out_queue.put(num)
 
 
 
    @task
    def test_002(self):
        if not self.out_queue.empty():
            print("test_002")
            self.my_queue.put(self.out_queue.get())
            self.out_queue.task_done()
 
if __name__ == '__main__':
    import os
    os.system("locust -f locust_id.py --headless -u 20 -r 2 --run-time 1h30m")
 