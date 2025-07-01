import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emergency_response.data_structures.emergency import Emergency, EmergencyType
from emergency_response.data_structures.linked_list import LinkedListPriorityQueue

class TestLinkedListPriorityQueue(unittest.TestCase):
    
    def setUp(self):
        """每个测试前设置测试环境"""
        self.queue = LinkedListPriorityQueue()
        
        # 创建测试用的紧急情况对象
        self.emergency1 = Emergency(1, EmergencyType.FIRE, 1, "市中心", (10, 20))
        self.emergency2 = Emergency(2, EmergencyType.MEDICAL, 3, "北区医院", (15, 25))
        self.emergency3 = Emergency(3, EmergencyType.POLICE, 2, "南区商场", (5, 15))
        self.emergency4 = Emergency(4, EmergencyType.FIRE, 1, "西区住宅", (8, 18))
    
    def test_is_empty(self):
        """测试队列是否为空"""
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue(self.emergency1)
        self.assertFalse(self.queue.is_empty())
    
    def test_enqueue(self):
        """测试入队操作"""
        self.queue.enqueue(self.emergency2)  # 严重程度3
        self.queue.enqueue(self.emergency3)  # 严重程度2
        self.queue.enqueue(self.emergency1)  # 严重程度1
        
        # 队列长度应该是3
        self.assertEqual(len(self.queue), 3)
        
        # 出队顺序应该按照优先级（严重程度从小到大）
        self.assertEqual(self.queue.dequeue(), self.emergency1)
        self.assertEqual(self.queue.dequeue(), self.emergency3)
        self.assertEqual(self.queue.dequeue(), self.emergency2)
    
    def test_dequeue_empty(self):
        """测试从空队列出队"""
        self.assertIsNone(self.queue.dequeue())
    
    def test_search(self):
        """测试搜索操作"""
        self.queue.enqueue(self.emergency1)
        self.queue.enqueue(self.emergency2)
        self.queue.enqueue(self.emergency3)
        
        # 搜索存在的紧急情况
        found = self.queue.search(2)
        self.assertEqual(found, self.emergency2)
        
        # 搜索不存在的紧急情况
        not_found = self.queue.search(99)
        self.assertIsNone(not_found)
    
    def test_change_priority(self):
        """测试更改优先级操作"""
        self.queue.enqueue(self.emergency1)  # 严重程度1
        self.queue.enqueue(self.emergency2)  # 严重程度3
        self.queue.enqueue(self.emergency3)  # 严重程度2
        
        # 更改emergency3的严重程度为4（降低优先级）
        success = self.queue.change_priority(3, 4)
        self.assertTrue(success)
        
        # 出队顺序应该是：emergency1, emergency2, emergency3
        self.assertEqual(self.queue.dequeue(), self.emergency1)
        self.assertEqual(self.queue.dequeue(), self.emergency2)
        
        # emergency3现在的严重程度应该是4
        emergency3 = self.queue.dequeue()
        self.assertEqual(emergency3.severity_level, 4)
        
        # 尝试更改不存在的紧急情况的优先级
        self.assertFalse(self.queue.change_priority(99, 5))
    
    def test_iteration(self):
        """测试迭代器"""
        self.queue.enqueue(self.emergency2)  # 严重程度3
        self.queue.enqueue(self.emergency3)  # 严重程度2
        self.queue.enqueue(self.emergency1)  # 严重程度1
        
        items = list(self.queue)
        # 迭代顺序应该是按照链表顺序（即按优先级排序）
        self.assertEqual(items[0], self.emergency1)
        self.assertEqual(items[1], self.emergency3)
        self.assertEqual(items[2], self.emergency2)

    def test_enqueue_empty_queue(self):
        """
        测试在空队列中入队和出队的情况
        """
        self.assertIsNone(self.queue.dequeue())  # 确保出队返回None
        self.queue.enqueue(self.emergency1)
        self.assertEqual(self.queue.dequeue(), self.emergency1)  # 确保入队后可以出队

    def test_enqueue_same_id(self):
        """
        测试插入两个具有相同ID的紧急情况
        """
        emergency5 = Emergency(1, EmergencyType.FIRE, 1, "Duplicate Location", (10, 20))
        self.queue.enqueue(self.emergency1)  # ID为1
        self.queue.enqueue(emergency5)  # ID也为1
        self.assertEqual(len(self.queue), 2)  # 确保队列长度为2
        self.assertEqual(self.queue.dequeue(), self.emergency1)  # 确保第一个出队的是emergency1
        self.assertEqual(self.queue.dequeue(), emergency5)  # 确保第二个出队的是emergency5

if __name__ == '__main__':
    unittest.main() 