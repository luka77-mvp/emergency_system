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
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # 跳过标题行
            next(reader, None)
            
            for row in reader:
                try:
                    emergency_id = int(row[0])
                    
                    # 解析紧急情况类型
                    type_str = row[1].upper()  # 转换为大写以匹配枚举
                    if type_str == "FIRE":
                        emergency_type = EmergencyType.FIRE
                    elif type_str == "MEDICAL":
                        emergency_type = EmergencyType.MEDICAL
                    elif type_str == "POLICE":
                        emergency_type = EmergencyType.POLICE
                    elif type_str == "TRAFFIC":
                        emergency_type = EmergencyType.TRAFFIC
                    elif type_str == "NATURAL":
                        emergency_type = EmergencyType.NATURAL
                    else:
                        print(f"警告: 未知的紧急情况类型 '{row[1]}', 跳过此行")
                        continue
                    
                    severity_level = int(row[2])
                    location = row[3]
                    
                    # 创建紧急情况对象
                    if len(row) >= 6:  # 有坐标信息
                        coordinate_x = float(row[4])
                        coordinate_y = float(row[5])
                        emergency = Emergency(
                            emergency_id=emergency_id,
                            emergency_type=emergency_type,
                            severity_level=severity_level,
                            location=location,
                            coordinates=(coordinate_x, coordinate_y)
                        )
                    else:  # 没有坐标信息，使用默认坐标
                        emergency = Emergency(
                            emergency_id=emergency_id,
                            emergency_type=emergency_type,
                            severity_level=severity_level,
                            location=location
                        )
                    
                    emergencies.append(emergency)
                except Exception as e:
                    print(f"警告: 处理行 {row} 时发生错误: {e}, 跳过此行")
        
        print(f"Successfully loaded {len(emergencies)} emergency records")
        return emergencies
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' does not exist")
        return []
    except Exception as e:
        print(f"Error: Exception occurred while loading data: {e}")
        return []

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
    
    print(f"Loaded {len(emergencies)} emergency records into three priority queues") 