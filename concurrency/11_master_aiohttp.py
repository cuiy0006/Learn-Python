from multiprocessing.managers import BaseManager
import queue
import time
import random


task_queue = queue.Queue()
result_queue = queue.Queue()


def return_task_queue():
    return task_queue


def return_result_queue():
    return result_queue


BaseManager.register('get_task_queue', callable=return_task_queue)
BaseManager.register('get_result_queue', callable=return_result_queue)
manager = BaseManager(address=('192.168.1.100', 20000), authkey=b'abc')
manager.start()
task_queue = manager.get_task_queue()
result_queue = manager.get_result_queue()

time.sleep(5)
for i in range(100):
    task_queue.put('http://localhost:5011/{}'.format(random.randint(1, 5)))


start = time.time()
print('Try get results...')
for i in range(100):
    res = result_queue.get()
    print(res)

manager.shutdown()
print('manager shut down')
print(time.time() - start)
