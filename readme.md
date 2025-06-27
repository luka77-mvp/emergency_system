# 应急响应管理系统

这是一个用于城市应急响应管理的系统，可以根据紧急情况的严重程度对其进行优先级排序，确保最关键的问题首先得到解决。该系统实现了三种不同的优先队列数据结构（链表、二叉树和堆），并比较它们的效率和复杂度。

## 项目结构

```
emergency_system/
├── emergency_response/
│   ├── __init__.py
│   ├── data_structures/
│   │   ├── __init__.py
│   │   ├── emergency.py       # 紧急情况类
│   │   ├── linked_list.py     # 链表实现的优先队列
│   │   ├── binary_tree.py     # 二叉树实现的优先队列
│   │   └── heap.py            # 堆实现的优先队列
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── interface.py       # 基本GUI界面
│   │   ├── knn_visualization.py # K最近邻可视化界面
│   │   ├── statistics.py      # 统计分析界面
│   │   ├── emergency_simulation.py # 应急调度模拟界面
│   │   └── main_app.py        # 主应用程序界面
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py     # 数据加载工具
│       └── performance_analyzer.py  # 性能分析工具
├── tests/
│   ├── __init__.py
│   ├── test_emergency.py      # 紧急情况类测试
│   ├── test_linked_list.py    # 链表优先队列测试
│   ├── test_binary_tree.py    # 二叉树优先队列测试
│   ├── test_heap.py           # 堆优先队列测试
│   ├── test_data_loader.py    # 数据加载工具测试
│   └── test_performance_analyzer.py  # 性能分析工具测试
├── data/
│   └── emergency_dataset.csv  # 紧急情况数据集
├── docs/
│   ├── design_decisions.md    # 设计决策文档
│   ├── algorithms.md          # 算法说明文档
│   └── challenges.md          # 挑战与解决方案文档
├── main.py                    # 主程序入口
└── run_gui.py                 # GUI启动脚本
```

## 功能特点

1. **紧急情况表示**：使用Python类表示紧急情况，包含ID、类型（如火灾、医疗、警察）、严重程度和位置等属性。
2. **三种优先队列实现**：
   - **链表**：每个节点保存数据元素及其优先级，链表头始终指向优先级最高的元素。
   - **二叉树**：利用二叉搜索树性质，优先级高的元素放在左子树，优先级低的放在右子树。
   - **堆**：使用数组实现二叉堆，父节点的优先级始终高于或等于其子节点。
3. **数据加载**：从CSV文件加载紧急情况数据。
4. **性能分析**：比较三种优先队列实现在入队、出队和搜索操作上的性能。
5. **图形用户界面**：提供直观的用户界面，支持以下功能：
   - 可视化紧急情况队列
   - 添加、移除和搜索紧急情况
   - K最近邻紧急响应单位推荐
   - 紧急情况统计分析和可视化
   - 性能比较结果展示
   - 应急调度模拟展示

## 安装与使用

### 安装依赖

```bash
pip install matplotlib numpy tkinter
```

### 运行主程序

```bash
python main.py
```

### 运行图形用户界面

```bash
# 方法1：使用专用启动脚本
python run_gui.py

# 方法2：通过主程序启动
python main.py --gui
```

### 运行性能分析

```bash
python main.py --analyze
```

### 使用自定义数据文件

```bash
python main.py --data path/to/your/data.csv
```

### 运行测试

```bash
# 运行所有测试
python -m unittest discover -s tests

# 运行特定测试
python -m tests.test_emergency
python -m tests.test_linked_list
python -m tests.test_binary_tree
python -m tests.test_heap
```

## 数据格式

紧急情况数据文件应为CSV格式，包含以下列：

```
emergency_id,type,severity,location
1,Fire,5,Downtown
2,Medical,3,Suburbs
...
```

- `emergency_id`: 紧急情况的唯一标识符
- `type`: 紧急情况类型 (Fire, Medical, Police)
- `severity`: 严重程度 (1-10，1表示最严重/最高优先级)
- `location`: 位置描述

## 复杂度分析

### 时间复杂度

| 操作    | 链表         | 二叉树       | 堆           |
|---------|-------------|-------------|-------------|
| 入队    | O(n)        | O(log n)    | O(log n)    |
| 出队    | O(1)        | O(log n)    | O(log n)    |
| 搜索    | O(n)        | O(n)        | O(1)        |

### 空间复杂度

| 数据结构 | 空间复杂度   |
|---------|-------------|
| 链表    | O(n)        |
| 二叉树  | O(n)        |
| 堆      | O(n)        |

## 图形用户界面功能

### 主界面

主界面提供以下功能按钮：
- **紧急情况管理**：管理紧急情况队列
- **K最近邻可视化**：可视化K个最近的紧急响应单位
- **统计分析**：分析紧急情况数据并生成图表
- **性能比较**：比较三种优先队列实现的性能
- **应急调度模拟**：模拟不同优先队列处理紧急情况的效率对比
- **加载数据**：从CSV文件加载紧急情况数据
- **退出**：退出应用程序

### 紧急情况管理界面

该界面允许用户：
- 选择使用的优先队列类型（链表、二叉树或堆）
- 添加新的紧急情况
- 出队最高优先级的紧急情况
- 搜索紧急情况
- 更改紧急情况的优先级
- 加载示例数据
- 清空队列
- 显示统计图表

### K最近邻可视化界面

该界面允许用户：
- 添加紧急情况（包括位置坐标）
- 随机生成紧急响应单位
- 调整K值（最近邻数量）
- 可视化紧急情况和最近的响应单位
- 查看推荐结果

### 统计分析界面

该界面提供：
- 紧急情况类型分布饼图
- 严重程度分布柱状图
- 时间分析图表（使用模拟数据）
- 导出统计报告功能

### 应急调度模拟界面

该界面提供：
- 模拟参数设置（紧急情况数量、模拟运行次数）
- 运行模拟测试三种优先队列处理紧急情况的效率
- 处理时间对比图表（入队、出队、总时间）
- 吞吐量对比图表（每秒处理的紧急情况数）
- 详细模拟结果数据

## 贡献者

- Li BoXi
- Liu ZiHan
- Liu ZiZheng
- Wang WanTing
- Li Shu
