import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emergency_response.data_structures.emergency import Emergency, EmergencyType
from emergency_response.data_structures.binary_tree import BinaryTreePriorityQueue

class TestBinaryTreePriorityQueue(unittest.TestCase):
    
    def setUp(self):
        """每个测试前设置测试环境"""
        self.queue = BinaryTreePriorityQueue()
        
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
    
    def test_peek(self):
        """测试查看最高优先级元素（使用get_min）"""
        self.queue.enqueue(self.emergency2)  # severity 3
        self.queue.enqueue(self.emergency3)  # severity 2
        self.queue.enqueue(self.emergency1)  # severity 1
        
        # get_min 应该返回优先级最高的 emergency1
        self.assertEqual(self.queue.get_min(), self.emergency1)
        # 确认 peek (get_min) 不移除元素
        self.assertEqual(len(self.queue), 3)

    def test_peek_empty(self):
        """测试从空队列查看（使用get_min）"""
        self.assertIsNone(self.queue.get_min())
    
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
    
    def test_iteration(self):
        """测试迭代器（中序遍历）"""
        self.queue.enqueue(self.emergency2)  # 严重程度3
        self.queue.enqueue(self.emergency3)  # 严重程度2
        self.queue.enqueue(self.emergency1)  # 严重程度1
        
        # 将迭代结果转换为列表
        items = list(self.queue)
        
        # 验证迭代顺序是按优先级排序的（中序遍历）
        # 由于BST的特性，迭代顺序可能会根据插入顺序而变化
        # 但最高优先级的元素应该是第一个
        self.assertEqual(items[0], self.emergency1)
        
        # 确保所有元素都在列表中
        self.assertIn(self.emergency1, items)
        self.assertIn(self.emergency2, items)
        self.assertIn(self.emergency3, items)

if __name__ == '__main__':
    unittest.main() 