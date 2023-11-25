from sz import PriorityQueue, Stack

queue = PriorityQueue()
queue.push('a', 8)
queue.push('b', 3)
queue.push('c', 2)
queue.push('d', 1)
queue.push('e', 9)
while queue.len() != 0:
    print(queue.pop())

print('----------')

stack = Stack()
stack.push('a')
stack.push('b')
stack.push('c')
while not stack.is_empty():
    print(stack.pop())
