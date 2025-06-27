import csv
import os
from ..data_structures.emergency import Emergency, EmergencyType

def load_emergency_data(file_path):
    """
    从CSV文件加载紧急情况数据
    
    参数:
        file_path: CSV文件的路径
        
    返回:
        加载的紧急情况对象列表
    
    CSV文件格式:
        emergency_id,type,severity,location,coordinate_x,coordinate_y
        1,Fire,5,Downtown,35.2,67.8
        ...
    """
    emergencies = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, 1):
            try:
                emergency_id = int(row['emergency_id'])
                # 将类型字符串转换为EmergencyType枚举（不区分大小写）
                emergency_type_str = row['type'].strip().upper()
                emergency_type = EmergencyType[emergency_type_str]
                severity_level = int(row['severity'])
                location = row['location'].strip()
                
                # 坐标是可选的
                coordinate_x = float(row.get('coordinate_x', 0))
                coordinate_y = float(row.get('coordinate_y', 0))
                
                emergency = Emergency(
                    emergency_id=emergency_id,
                    emergency_type=emergency_type,
                    severity_level=severity_level,
                    location=location,
                    coordinates=(coordinate_x, coordinate_y)
                )
                emergencies.append(emergency)
            except (KeyError, ValueError, TypeError) as e:
                print(f"警告: 无法解析CSV文件第 {row_num + 1} 行。错误: {e}. 跳过此行。")
                continue
    
    print(f"成功加载了 {len(emergencies)} 条紧急情况记录")
    return emergencies

def initialize_priority_queues(emergencies, linked_list_queue, binary_tree_queue, heap_queue):
    """
    使用紧急情况数据初始化三种优先队列
    
    参数:
        emergencies: 紧急情况对象列表
        linked_list_queue: 链表优先队列实例
        binary_tree_queue: 二叉树优先队列实例
        heap_queue: 堆优先队列实例
    """
    for emergency in emergencies:
        linked_list_queue.enqueue(emergency)
        binary_tree_queue.enqueue(emergency)
        heap_queue.enqueue(emergency)
    
    print(f"已将 {len(emergencies)} 条紧急情况记录加载到三个优先队列中") 