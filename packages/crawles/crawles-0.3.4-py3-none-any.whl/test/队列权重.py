from queue import PriorityQueue

# 创建一个空的优先级队列
queue = PriorityQueue()

# 添加元素到队列中
queue.put((-3, 'apple'))
queue.put((2, 'banana'))
queue.put((3, 'orange'))
queue.put((1, 'grape'))

# 从队列中获取具有最小权重的元素
# item = queue.get()
# print(item)  # 输出：(1, 'grape')

# 访问队列中具有最小权重的元素，但不会将其移出队列
# item = queue.queue[0]
# print(item)  # 输出：(2, 'banana')

# 遍历队列中的所有元素
while not queue.empty():
    item = queue.get()
    print(item)

# 输出：
# (2, 'banana')
# (3, 'orange')
# (5, 'apple')