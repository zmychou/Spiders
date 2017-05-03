
from WorkerThread import WorkerThread

tags = []
pool = set()
w = WorkerThread(tags, 'worker1')
tags = w.findAllTag('https://movie.douban.com/tag/', True) 
lists = []
for i in range(3) :
    l = []
    for j in range(12) :
        l.append(tags.pop()) 
    lists.append(l)
w1 = WorkerThread(lists[0], 'worker1')
w2 = WorkerThread(lists[1], 'worker2')
w3 = WorkerThread(lists[2], 'worker3')
print(lists[0])  
print(lists[1])  
print(lists[2])
w1.start()
w2.start()
w3.start()

