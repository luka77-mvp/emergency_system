import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emergency_response.data_structures.emergency import Emergency, EmergencyType
from emergency_response.data_structures.heap import HeapPriorityQueue

class TestHeapPriorityQueue(unittest.TestCase):
    
    def setUp(self):
        """每个测试前设置测试环境"""
        self.queue = HeapPriorityQueue()
        
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
        
        # 出队顺序应该是：emergency1, emergency2, emergency3(现在优先级最低)
        self.assertEqual(self.queue.dequeue(), self.emergency1)
        self.assertEqual(self.queue.dequeue(), self.emergency2)
        
        emergency3 = self.queue.dequeue()
        self.assertEqual(emergency3.emergency_id, 3)
        self.assertEqual(emergency3.severity_level, 4)
        
        # 尝试更改不存在的紧急情况的优先级
        self.assertFalse(self.queue.change_priority(99, 5))
    
    def test_multiple_emergencies_same_priority(self):
        """测试多个相同优先级的紧急情况"""
        # 创建两个严重程度相同的紧急情况
        emergency5 = Emergency(5, EmergencyType.FIRE, 1, "东区公园", (12, 22))
        
        self.queue.enqueue(self.emergency1)  # 严重程度1
        self.queue.enqueue(emergency5)       # 严重程度1
        self.queue.enqueue(self.emergency3)  # 严重程度2
        
        # 出队前两个元素（应该是最高优先级的）
        first = self.queue.dequeue()
        second = self.queue.dequeue()
        
        # 验证最高优先级的两个元素先出队，但不检查它们的具体顺序
        # 只确保它们都是严重程度为1的紧急情况
        self.assertEqual(first.severity_level, 1)
        self.assertEqual(second.severity_level, 1)
        
        # 确保两个不同的对象都被出队了
        self.assertIn(first.emergency_id, [1, 5])
        self.assertIn(second.emergency_id, [1, 5])
        self.assertNotEqual(first.emergency_id, second.emergency_id)
        
        # 验证最后出队的是优先级较低的元素
        third = self.queue.dequeue()
        self.assertEqual(third, self.emergency3)
    
    def test_large_number_of_items(self):
        """测试大量元素的情况"""
        # 创建50个紧急情况对象
        emergencies = []
        for i in range(50):
            severity = (i % 10) + 1  # 严重程度从1到10循环
            emergency = Emergency(100 + i, EmergencyType.FIRE, severity, f"位置{i}", (i, i))
            emergencies.append(emergency)
            self.queue.enqueue(emergency)
        
        # 验证队列长度
        self.assertEqual(len(self.queue), 50)
        
        # 验证出队顺序是按照优先级
        last_severity = 0
        for i in range(50):
            emergency = self.queue.dequeue()
            self.assertIsNotNone(emergency)
            self.assertGreaterEqual(emergency.severity_level, last_severity)
            last_severity = emergency.severity_level
        
        # 队列应该为空
        self.assertTrue(self.queue.is_empty())

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