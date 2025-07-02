# City Emergency Response Management System Project Report

## 1. Installation Instructions

### System Requirements
- Python 3.7 or higher

### Installation Steps
1. Install dependencies:
   ```bash
   pip install matplotlib numpy pandas tk
   ```

2. Run the main program:
   ```bash
   python main.py
   ```
## Project Roles

| Name      | Main Responsibilities                                                                 |
|-----------|---------------------------------------------------------------------------------------|
| Li Boxi   | Core architecture & data structures: Responsible for all core data structure implementations (binary_tree.py, heap.py, linked_list.py, emergency.py); main program architecture design (main.py); GUI and data structure integration; drawing data structure flowcharts |
| Liu Zhihan| GUI Development (Part 1): Develop main interface (interface.py); main application (main_app.py); emergency simulation module (emergency_simulation.py) |
| Liu Zizheng| GUI Development (Part 2): Develop custom dialogs (custom_dialogs.py); statistics module (statistics.py); KNN visualization module (knn_visualization.py) |
| Li Shu    | Data Processing & Simulation: Develop data loader (data_loader.py); dataset preparation and management (emergency_dataset.csv); performance analyzer module (performance_analyzer.py) |
| Wang Wanting| Testing & Documentation: Write all unit tests; system documentation; user manual (readme.md) |

## 2. Dependencies
| Library Name | Version | Purpose |
|-------------|---------|---------|
| tkinter     | Built-in Python | GUI development |
| matplotlib  | ≥3.5.0  | Data visualization and charting |
| numpy       | ≥1.22.0 | Numerical computation and data processing |
| pandas      | ≥1.4.0  | Data analysis and processing |
| csv         | Built-in Python | CSV file read/write |
| unittest    | Built-in Python | Unit testing framework |
| random      | Built-in Python | Generate random data |
| time        | Built-in Python | Time-related operations |

## 3. Backend Code Design Description

### Emergency Class
The `Emergency` class represents an emergency instance with the following attributes:
- `emergency_id`: Unique identifier for the emergency
- `type`: Emergency type (using `EmergencyType` enum)
- `severity_level`: Severity (1-10, 1 is most severe/highest priority)
- `location`: Location description
- `coordinates`: Location coordinates (x, y)

The class implements comparison operators, allowing emergencies to be prioritized by severity and ID:
```python
def __lt__(self, other):
    if self.severity_level == other.severity_level:
        return self.emergency_id < other.emergency_id
    return self.severity_level < other.severity_level
```

### Priority Queue Data Structures

#### Linked List Implementation (LinkedListPriorityQueue)
- **Design**: Uses a sorted linked list, highest priority at the head
- **Features**:
  - Insertion requires traversal to find the correct position (O(n))
  - Deletion only needs to remove the head (O(1))
  - Supports search by ID (O(n))

#### Binary Tree Implementation (BinaryTreePriorityQueue)
- **Design**: Uses a binary search tree, nodes sorted by emergency priority
- **Features**:
  - Average O(log n) for insert and delete
  - In-order traversal for sorted list
  - Fast search and priority change

#### Heap Implementation (HeapPriorityQueue)
- **Design**: Uses a min-heap, highest priority at the top
- **Features**:
  - O(log n) for insert and delete
  - Extra mapping for fast lookup (O(1))
  - Efficient priority change

### Complexity Analysis

#### Time Complexity

| Operation | Linked List | Binary Tree | Heap |
|-----------|-------------|-------------|------|
| Enqueue   | O(n)        | O(log n)    | O(log n) |
| Dequeue   | O(1)        | O(log n)    | O(log n) |
| Search    | O(n)        | O(n)        | O(1)    |

#### Space Complexity

| Data Structure | Space Complexity |
|----------------|------------------|
| Linked List    | O(n)             |
| Binary Tree    | O(n)             |
| Heap           | O(n)             |

### Complex Implementations
- **Heap Priority Change**: When changing severity, the heap must be re-adjusted
  ```python
  def change_priority(self, emergency_id, new_severity):
      index = self.id_to_index[emergency_id]
      old_severity = self.heap[index].severity_level
      self.heap[index].severity_level = new_severity
      
      if new_severity < old_severity:  # Priority increased
          self._shift_up(index)
      else:  # Priority decreased
          self._shift_down(index)
  ```
- **Binary Tree Deletion**: For nodes with two children, find the in-order successor
- **Linked List Priority Change**: Remove the node and re-insert at the correct position

## 4. Testing and Coverage

### Testing Framework
Uses Python's `unittest` framework for unit testing

### Test Coverage
| Test File | Coverage |
|-----------|----------|
| test_emergency.py | Emergency class initialization and comparison |
| test_linked_list.py | Linked list queue basic operations and edge cases |
| test_binary_tree.py | Binary tree queue operations and balance maintenance |
| test_heap.py | Heap queue operations and performance tests |
| test_data_loader.py | Data loading and queue initialization |
| test_performance_analyzer.py | Performance analyzer functionality |

### Test Coverage Rate
Overall project test coverage is **89%**, ensuring core functionality reliability

## 5. Project Structure and File Roles

### Project Structure
```
emergency_system/
├── emergency_response/
│   ├── __init__.py
│   ├── data_structures/
│   │   ├── __init__.py
│   │   ├── emergency.py       # Emergency class
│   │   ├── linked_list.py     # Linked list priority queue
│   │   ├── binary_tree.py     # Binary tree priority queue
│   │   └── heap.py            # Heap priority queue
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── interface.py       # Main GUI interface
│   │   ├── knn_visualization.py # KNN visualization interface
│   │   ├── statistics.py      # Statistics analysis interface
│   │   ├── emergency_simulation.py # Emergency dispatch simulation interface
│   │   └── main_app.py        # Main application interface
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_loader.py     # Data loader utility
│   │   └── performance_analyzer.py  # Performance analyzer utility
├── tests/
│   ├── __init__.py
│   ├── test_emergency.py      # Emergency class tests
│   ├── test_linked_list.py    # Linked list priority queue tests
│   ├── test_binary_tree.py    # Binary tree priority queue tests
│   ├── test_heap.py           # Heap priority queue tests
│   ├── test_data_loader.py    # Data loader utility tests
│   └── test_performance_analyzer.py  # Performance analyzer utility tests
├── data/
│   └── emergency_dataset.csv   # Emergency dataset
├── pics/
│   ├── binary_tree.png     # Binary tree flowchart
│   ├── linked_list.png     # Linked list flowchart
│   ├── heap.png            # Min-heap flowchart
│   ├── binary_tree2.jpg    # Binary tree structure diagram
│   ├── linked_list2.jpg    # Linked list structure diagram
│   └── heap2.jpg           # Min-heap structure diagram
└── main.py                     # Main program entry

```

## 6. Project Features and Application Scenarios

### Main Features
1. **Emergency Management**:
   - Add, process, and search emergencies
   - Change emergency priority
   - Three different data structure implementations for priority queues

2. **KNN Visualization**:
   - Visualize emergencies and response units on a map
   - Recommend nearest response units based on distance

3. **Statistical Analysis**:
   - Analyze emergency type distribution
   - Analyze severity distribution
   - Data structure complexity analysis

4. **Performance Comparison**:
   - Compare operation performance of three data structures
   - Visualize processing time for different data scales

5. **Emergency Dispatch Simulation**:
   - Simulate large-scale emergency handling process
   - Compare performance of different data structures in real scenarios

### Application Scenarios
1. City emergency response center managing incidents
2. Hospitals or emergency centers optimizing resource allocation
3. Fire departments handling fire alarms and resource dispatch
4. Police departments managing emergency police requests
5. Urban planning departments analyzing emergency event distribution

## 7. Challenges and Lessons Learned

### Main Challenges
1. **Data Structure Selection**:
   - Balancing performance among linked list, binary tree, and heap for priority queues
   - Special handling for emergencies with the same ID

2. **Data Consistency**:
   - Keeping data synchronized across all three data structures
   - Updating all queues when priority changes

3. **Performance Optimization**:
   - Tree balancing issues with large data in binary tree
   - Heap operation optimization and fast lookup

4. **GUI Performance**:
   - Visualization performance with large data
   - Dynamic drawing of tree structures

### Lessons Learned
1. **Consider edge cases in design**: Especially for same priority and ID
2. **Importance of test-driven development**: High coverage ensures code quality
3. **Balance between performance and maintainability**: Choose the right implementation for different scenarios
4. **Modular design**: Clear module separation makes the project easy to extend and maintain
5. **User experience first**: Complex backend logic needs intuitive frontend presentation

## 8. GUI Interface Description and Improvement Suggestions

### Interface Description
The GUI is developed with `tkinter` and includes the following main interfaces:

1. **Main Interface**:
   - Simple card-style layout
   - Five main function entries
   - Bottom status bar displays queue info

2. **Emergency Management Interface**:
   - Left control panel to select queue type
   - Center area displays queue content (list or tree)
   - Right area shows emergency statistics charts
   - Supports adding, processing, and searching emergencies

3. **KNN Visualization Interface**:
   - Map shows emergency and response unit locations
   - Control panel to adjust K value and generate random units
   - Result area displays recommended response units

4. **Statistical Analysis Interface**:
   - Pie chart for emergency type distribution
   - Bar chart for severity distribution
   - Shows time and space complexity info

5. **Performance Comparison Interface**:
   - Line chart compares performance of different data structures
   - Table shows time complexity comparison
   - Supports custom data size and operation type

### Improvement Suggestions
1. **Add more visualization elements**:
   - Use heatmaps to show emergency density
   - Add response unit movement animation

2. **Enhance user guidance**:
   - Add operation tutorial
   - Implement context-sensitive tips system

## Daily Work Schedule

- **Day 1**: Project planning and requirement gathering. We discussed the project scope and divided tasks among team members.
- **Day 2**: Designing the system architecture and data structures. We created diagrams to visualize the relationships.
- **Day 3**: Implementing the main application and GUI. Each member focused on their assigned modules, ensuring a cohesive design.
- **Day 4**: Developing the KNN algorithm and visualization. We iteratively tested the algorithm to ensure accuracy in distance calculations.
- **Day 5**: Testing and debugging the system. We conducted unit tests on each module and integrated them into the main application.
- **Day 6**: Debugging the system, find and fix bugs in the system.
- **Day 7**: Almost finish the task, start making the PPT and the 'readme.md'.
- **Day 8**: Continue making the PPT and the 'readme.md'.
- **Day 9**: Finish the PPT and the and the 'readme.md'.

## Conclusion
This city emergency response management system provides an efficient emergency management solution by implementing three different priority queue data structures (linked list, binary tree, and heap). The system combines an intuitive visual interface and powerful analysis tools to help emergency response departments optimize resource allocation and improve response efficiency.