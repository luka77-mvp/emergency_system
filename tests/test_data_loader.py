import unittest
import sys
import os
import tempfile

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emergency_response.utils.data_loader import load_emergency_data, initialize_priority_queues
from emergency_response.data_structures.emergency import Emergency, EmergencyType
from emergency_response.data_structures.linked_list import LinkedListPriorityQueue
from emergency_response.data_structures.binary_tree import BinaryTreePriorityQueue
from emergency_response.data_structures.heap import HeapPriorityQueue

class TestDataLoader(unittest.TestCase):
    
    def setUp(self):
        """每个测试前设置测试环境"""
        # 创建一个临时CSV文件用于测试
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv', encoding='utf-8')
        self.temp_file.write("emergency_id,type,severity,location,coordinate_x,coordinate_y\n")
        self.temp_file.write("1,Fire,5,Downtown,35.2,67.8\n")
        self.temp_file.write("2,Medical,3,Suburbs,78.4,23.1\n")
        self.temp_file.write("3,Police,4,City Center,45.6,52.3\n")
        self.temp_file.close()
        
        # 创建实际数据文件的路径
        self.actual_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'emergency_dataset.csv')
    
    def tearDown(self):
        """每个测试后清理环境"""
        os.unlink(self.temp_file.name)
    
    def test_load_emergency_data_from_temp(self):
        """测试从临时文件加载紧急情况数据"""
        emergencies = load_emergency_data(self.temp_file.name)
        
        # 验证加载的数据数量
        self.assertEqual(len(emergencies), 3)
        
        # 验证第一个紧急情况的属性
        self.assertEqual(emergencies[0].emergency_id, 1)
        self.assertEqual(emergencies[0].type, EmergencyType.FIRE)
        self.assertEqual(emergencies[0].severity_level, 5)
        self.assertEqual(emergencies[0].location, "Downtown")
        
        # 验证第二个紧急情况的属性
        self.assertEqual(emergencies[1].emergency_id, 2)
        self.assertEqual(emergencies[1].type, EmergencyType.MEDICAL)
        self.assertEqual(emergencies[1].severity_level, 3)
        self.assertEqual(emergencies[1].location, "Suburbs")
    
    def test_load_emergency_data_from_actual(self):
        """测试从实际数据文件加载紧急情况数据"""
        # 确保实际数据文件存在
        if os.path.exists(self.actual_data_path):
            emergencies = load_emergency_data(self.actual_data_path)
            
            # 验证数据被正确加载
            self.assertGreater(len(emergencies), 0)
            
            # 验证第一个紧急情况的属性
            self.assertEqual(emergencies[0].emergency_id, 1)
            self.assertEqual(emergencies[0].type, EmergencyType.FIRE)
            self.assertEqual(emergencies[0].severity_level, 5)
            self.assertEqual(emergencies[0].location, "Downtown")
        else:
            self.skipTest(f"实际数据文件 {self.actual_data_path} 不存在")
    
    def test_initialize_priority_queues(self):
        """测试初始化三种优先队列"""
        emergencies = load_emergency_data(self.temp_file.name)
        
        # 创建三种优先队列
        linked_list_queue = LinkedListPriorityQueue()
        binary_tree_queue = BinaryTreePriorityQueue()
        heap_queue = HeapPriorityQueue()
        
        # 初始化队列
        initialize_priority_queues(emergencies, linked_list_queue, binary_tree_queue, heap_queue)
        
        # 验证队列长度
        self.assertEqual(len(linked_list_queue), 3)
        self.assertEqual(len(binary_tree_queue), 3)
        self.assertEqual(len(heap_queue), 3)
        
        # 验证出队顺序（应该按照严重程度从低到高）
        # 严重程度：1最高优先级，10最低优先级
        
        # 医疗(3) -> 警察(4) -> 火灾(5)
        self.assertEqual(linked_list_queue.dequeue().emergency_id, 2)  # Medical, severity 3
        self.assertEqual(linked_list_queue.dequeue().emergency_id, 3)  # Police, severity 4
        self.assertEqual(linked_list_queue.dequeue().emergency_id, 1)  # Fire, severity 5
        
        # 二叉树队列
        self.assertEqual(binary_tree_queue.dequeue().emergency_id, 2)  # Medical, severity 3
        self.assertEqual(binary_tree_queue.dequeue().emergency_id, 3)  # Police, severity 4
        self.assertEqual(binary_tree_queue.dequeue().emergency_id, 1)  # Fire, severity 5
        
        # 堆队列
        self.assertEqual(heap_queue.dequeue().emergency_id, 2)  # Medical, severity 3
        self.assertEqual(heap_queue.dequeue().emergency_id, 3)  # Police, severity 4
        self.assertEqual(heap_queue.dequeue().emergency_id, 1)  # Fire, severity 5

    def test_load_emergency_data_from_empty_file(self):
        """
        测试从空文件加载紧急情况数据
        """
        empty_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv', encoding='utf-8')
        empty_file.close()
        emergencies = load_emergency_data(empty_file.name)
        self.assertEqual(len(emergencies), 0)  # 确保返回空列表
        os.unlink(empty_file.name)  # 清理文件

if __name__ == '__main__':
    unittest.main() 