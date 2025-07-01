# Emergency Response Management System

This is a system for urban emergency response management that prioritizes emergencies based on their severity, ensuring that the most critical issues are addressed first. The system implements three different priority queue data structures (linked lists, binary trees, and heaps) and compares their efficiency and complexity.

## Project Structure

```
emergency_system/
├── emergency_response/
│   ├── __init__.py
│   ├── data_structures/
│   │   ├── __init__.py
│   │   ├── emergency.py       # Emergency class
│   │   ├── linked_list.py     # Linked list implementation of priority queue
│   │   ├── binary_tree.py     # Binary tree implementation of priority queue
│   │   └── heap.py            # Heap implementation of priority queue
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── interface.py       # Basic GUI interface
│   │   ├── knn_visualization.py # K-nearest neighbor visualization interface
│   │   ├── statistics.py      # Statistical analysis interface
│   │   ├── emergency_simulation.py # Emergency dispatch simulation interface
│   │   └── main_app.py        # Main application interface
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py     # Data loading utility
│       └── performance_analyzer.py  # Performance analysis utility
├── tests/
│   ├── __init__.py
│   ├── test_emergency.py      # Emergency class tests
│   ├── test_linked_list.py    # Linked list priority queue tests
│   ├── test_binary_tree.py    # Binary tree priority queue tests
│   ├── test_heap.py           # Heap priority queue tests
│   ├── test_data_loader.py    # Data loading utility tests
│   └── test_performance_analyzer.py  # Performance analysis utility tests
├── data/
│   └── emergency_dataset.csv  # Emergency data set
├── docs/
│   ├── design_decisions.md    # Design decisions document
│   ├── algorithms.md          # Algorithm documentation
│   └── challenges.md          # Challenges and solutions document
├── main.py                    # Main program entry
└── run_gui.py                 # GUI startup script
```

## Features

1. **Emergency Representation**: A Python class representing emergencies, including attributes like ID, type (e.g., fire, medical, police), severity, and location.
2. **Three Priority Queue Implementations**:
   - **Linked List**: Each node stores the data element and its priority, with the head always pointing to the highest priority element.
   - **Binary Tree**: Utilizes binary search tree properties, with higher priority elements in the left subtree and lower priority elements in the right subtree.
   - **Heap**: Implemented as a binary heap using an array, where the parent node's priority is always higher than or equal to its children.
3. **Data Loading**: Loads emergency data from CSV files.
4. **Performance Analysis**: Compares the performance of the three priority queue implementations in terms of insertion, removal, and search operations.
5. **Graphical User Interface**: Provides an intuitive user interface supporting the following functionalities:
   - Visualizing the emergency queue
   - Adding, removing, and searching emergencies
   - K-nearest neighbor emergency response unit recommendations
   - Statistical analysis and visualization of emergencies
   - Performance comparison results
   - Emergency dispatch simulation

## Installation and Usage

### Install Dependencies

```bash
pip install matplotlib numpy tkinter
```

### Run the Main Program

```bash
python main.py
```

### Run the Graphical User Interface

```bash
# Method 1: Using dedicated startup script
python run_gui.py

# Method 2: Start through the main program
python main.py --gui
```

### Run Performance Analysis

```bash
python main.py --analyze
```

### Use Custom Data File

```bash
python main.py --data path/to/your/data.csv
```

### Run Tests

```bash
# Run all tests
python -m unittest discover -s tests

# Run specific tests
python -m tests.test_emergency
python -m tests.test_linked_list
python -m tests.test_binary_tree
python -m tests.test_heap
```

## Data Format

The emergency data file should be in CSV format, containing the following columns:

```
emergency_id,type,severity,location
1,Fire,5,Downtown
2,Medical,3,Suburbs
...
```

- `emergency_id`: Unique identifier for the emergency
- `type`: Type of emergency (Fire, Medical, Police)
- `severity`: Severity level (1-10, with 1 being the most severe/highest priority)
- `location`: Description of the location

## Complexity Analysis

### Time Complexity

| Operation | Linked List | Binary Tree | Heap |
|-----------|-------------|-------------|------|
| Enqueue   | O(n)        | O(log n)    | O(log n) |
| Dequeue   | O(1)        | O(log n)    | O(log n) |
| Search    | O(n)        | O(n)        | O(1)    |

### Space Complexity

| Data Structure | Space Complexity |
|----------------|------------------|
| Linked List    | O(n)             |
| Binary Tree    | O(n)             |
| Heap           | O(n)             |

## Graphical User Interface Features

### Main Interface

The main interface provides the following functional buttons:
- **Emergency Management**: Manage the emergency queue
- **K-Nearest Neighbor Visualization**: Visualize the K nearest emergency response units
- **Statistical Analysis**: Analyze emergency data and generate charts
- **Performance Comparison**: Compare the performance of the three priority queue implementations
- **Emergency Dispatch Simulation**: Simulate the efficiency of handling emergencies with different priority queues
- **Load Data**: Load emergency data from CSV files
- **Exit**: Exit the application

### Emergency Management Interface

This interface allows users to:
- Select the type of priority queue to use (Linked List, Binary Tree, or Heap)
- Add new emergencies
- Dequeue the highest priority emergency
- Search for emergencies
- Change the priority of emergencies
- Load sample data
- Clear the queue
- Display statistical charts

### K-Nearest Neighbor Visualization Interface

This interface allows users to:
- Add emergencies (including location coordinates)
- Randomly generate emergency response units
- Adjust the K value (number of nearest neighbors)
- Visualize emergencies and the nearest response units
- View recommendation results

### Statistical Analysis Interface

This interface provides:
- Pie chart of emergency type distribution
- Bar chart of severity distribution
- Time analysis charts (using simulated data)
- Functionality to export statistical reports

### Emergency Dispatch Simulation Interface

This interface provides:
- Simulation parameter settings (number of emergencies, number of simulation runs)
- Run simulations to test the efficiency of handling emergencies with each priority queue
- Comparison charts of processing times (enqueue, dequeue, total time)
- Throughput comparison charts (number of emergencies handled per second)
- Detailed simulation result data

## Contributors

- Li BoXi
- Liu ZiHan
- Liu ZiZheng
- Wang WanTing
- Li Shu