class Node:
    """链表节点类"""
    
    def __init__(self, data, next_node=None):
        """
        初始化链表节点
        
        参数:
            data: 节点存储的数据（Emergency对象）
            next_node: 指向下一个节点的引用
        """
        self.data = data
        self.next = next_node

class LinkedListPriorityQueue:
    """使用链表实现的优先队列"""
    
    def __init__(self):
        """初始化空的优先队列，包含头指针和尾指针"""
        self.head = None  # 指向最高优先级的元素
        self.tail = None  # 指向最低优先级的元素
        self.size = 0
    
    def is_empty(self):
        """检查队列是否为空"""
        return self.head is None
    
    def enqueue(self, item):
        """
        将项目添加到优先队列中
        
        参数:
            item: 要添加的紧急情况对象
            
        优先级规则:
            - 严重程度数值越小，优先级越高
            - 头部始终指向最高优先级的元素
        """
        self.size += 1
        new_node = Node(item)
        
        # 如果队列为空
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            return
        
        # 如果新项目优先级高于头部项目（应该成为新的头部）
        if item < self.head.data:
            new_node.next = self.head
            self.head = new_node
            return
        
        # 如果新项目优先级低于尾部项目（应该成为新的尾部）
        if self.tail.data < item:
            self.tail.next = new_node
            self.tail = new_node
            return
        
        # 否则，在链表中间找到合适的插入位置
        current = self.head
        while current.next and current.next.data < item:
            current = current.next
        
        # 插入新节点
        new_node.next = current.next
        current.next = new_node
        
        # 如果插入到了最后一个位置，更新尾指针
        if new_node.next is None:
            self.tail = new_node
    
    def dequeue(self):
        """
        移除并返回最高优先级的项目
        
        返回:
            最高优先级的紧急情况对象，如果队列为空则返回None
        """
        if self.is_empty():
            return None
        
        self.size -= 1
        highest_priority = self.head.data
        self.head = self.head.next
        
        # 如果队列变为空，也需要更新尾指针
        if self.head is None:
            self.tail = None
            
        return highest_priority
    
    def peek(self):
        """
        查看最高优先级的项目但不移除它
        
        返回:
            最高优先级的紧急情况对象，如果队列为空则返回None
        """
        if self.is_empty():
            return None
        return self.head.data
    
    def search(self, emergency_id):
        """
        搜索具有指定ID的紧急情况
        
        参数:
            emergency_id: 要搜索的紧急情况ID
            
        返回:
            找到的紧急情况对象，如果未找到则返回None
        """
        current = self.head
        while current:
            if current.data.emergency_id == emergency_id:
                return current.data
            current = current.next
        return None
    
    def change_priority(self, emergency_id, new_severity):
        """
        更改指定ID紧急情况的优先级
        
        参数:
            emergency_id: 要更改优先级的紧急情况ID
            new_severity: 新的严重程度值
            
        返回:
            布尔值，表示操作是否成功
        """
        # 首先找到并移除指定的紧急情况
        current = self.head
        previous = None
        
        # 查找节点
        while current and current.data.emergency_id != emergency_id:
            previous = current
            current = current.next
        
        # 如果未找到，返回失败
        if not current:
            return False
        
        # 保存找到的紧急情况并从链表中移除
        emergency = current.data
        
        # 如果是头节点
        if previous is None:
            self.head = current.next
        else:
            previous.next = current.next
        
        # 如果是尾节点，更新尾指针
        if current == self.tail:
            self.tail = previous
        
        self.size -= 1
        
        # 更新严重程度
        emergency.severity_level = new_severity
        
        # 重新入队
        self.enqueue(emergency)
        return True
    
    def __len__(self):
        """返回队列中的元素数量"""
        return self.size
    
    def __iter__(self):
        """使队列可迭代"""
        current = self.head
        while current:
            yield current.data
            current = current.next