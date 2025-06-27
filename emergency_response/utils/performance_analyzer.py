import time
import random
import gc
import matplotlib.pyplot as plt

from ..data_structures.emergency import Emergency, EmergencyType
from ..data_structures.linked_list import LinkedListPriorityQueue
from ..data_structures.binary_tree import BinaryTreePriorityQueue
from ..data_structures.heap import HeapPriorityQueue


class PerformanceAnalyzer:
    """A performance analyzer to compare different priority queue implementations."""

    def __init__(self):
        """Initializes the performance analyzer."""
        self.results = {}

    def generate_random_emergencies(self, count):
        """Generates a list of random emergency objects."""
        emergencies = []
        emergency_types = [EmergencyType.FIRE, EmergencyType.MEDICAL, EmergencyType.POLICE]
        locations = ["Downtown", "Suburbs", "City Center", "Industrial Area", "Residential Area"]
        
        for i in range(count):
            emergency = Emergency(
                emergency_id=i + 1,
                emergency_type=random.choice(emergency_types),
                severity_level=random.randint(1, 10),
                location=random.choice(locations)
            )
            emergencies.append(emergency)
        
        return emergencies

    def _run_test_for_operation(self, data_sizes, operation_name):
        """
        Runs a performance test for a specific operation across different data sizes.
        
        Parameters:
            data_sizes: A list of data sizes to test.
            operation_name: The name of the operation ('enqueue', 'dequeue', 'search').
        """
        results = {'Linked List': [], 'Binary Tree': [], 'Heap': []}
        queue_classes = {
            'Linked List': LinkedListPriorityQueue,
            'Binary Tree': BinaryTreePriorityQueue,
            'Heap': HeapPriorityQueue
        }

        for size in data_sizes:
            if size <= 0:
                for name in queue_classes: results[name].append(0)
                continue

            emergencies = self.generate_random_emergencies(size)
            
            for name, queue_class in queue_classes.items():
                repeat_count = 10
                total_time = 0

                for _ in range(repeat_count):
                    queue = queue_class()
                    
                    # Pre-fill queue for dequeue and search
                    if operation_name in ['dequeue', 'search']:
                        for e in emergencies:
                            queue.enqueue(e)
                    
                    # Define the operation to be timed
                    if operation_name == 'enqueue':
                        op_to_time = lambda: [queue.enqueue(e) for e in emergencies]
                    elif operation_name == 'dequeue':
                        op_to_time = lambda: [queue.dequeue() for _ in range(size)]
                    elif operation_name == 'search':
                        target = random.choice(emergencies)
                        op_to_time = lambda: queue.search(target)
                    else:
                        op_to_time = lambda: None

                    gc.disable()
                    start_time = time.perf_counter()
                    op_to_time()
                    end_time = time.perf_counter()
                    gc.enable()
                    total_time += (end_time - start_time)

                avg_time = total_time / repeat_count
                results[name].append(avg_time)
            
            print(f"Data Size: {size}, "
                  f"Linked List: {results['Linked List'][-1]:.6f}s, "
                  f"Binary Tree: {results['Binary Tree'][-1]:.6f}s, "
                  f"Heap: {results['Heap'][-1]:.6f}s")
        
        self.results[operation_name] = results

    def measure_enqueue_performance(self, data_sizes):
        """Measures the performance of the enqueue operation."""
        self._run_test_for_operation(data_sizes, "enqueue")

    def measure_dequeue_performance(self, data_sizes):
        """Measures the performance of the dequeue operation."""
        self._run_test_for_operation(data_sizes, "dequeue")

    def measure_search_performance(self, data_sizes):
        """Measures the performance of the search operation."""
        self._run_test_for_operation(data_sizes, "search")

    def plot_results(self, operation, data_sizes, figure=None, ax=None):
        """Plots the performance comparison results on a Matplotlib chart."""
        if operation not in self.results:
            print(f"Error: Results for operation '{operation}' are not available.")
            return

        if ax is None or figure is None:
            figure, ax = plt.subplots(figsize=(10, 6))
        else:
            ax.clear()

        results_for_op = self.results[operation]
        
        for queue_type, times in results_for_op.items():
            ax.plot(data_sizes, times, marker='o', linestyle='-', label=queue_type)

        ax.set_title(f'Performance Comparison for {operation.capitalize()} Operation')
        ax.set_xlabel('Number of Emergencies (Data Size)')
        ax.set_ylabel('Execution Time (seconds)')
        ax.legend()
        ax.grid(True)
        
        figure.tight_layout()

        if hasattr(figure.canvas, 'draw'):
            figure.canvas.draw()

    def get_complexity_analysis(self):
        """Returns a dictionary with theoretical complexity analysis."""
        time_complexity = {
            "Operation": ["Enqueue", "Dequeue", "Search"],
            "Linked List": ["O(n)", "O(1)", "O(n)"],
            "Binary Tree": ["O(log n)", "O(log n)", "O(n)"],
            "Heap": ["O(log n)", "O(log n)", "O(n)"]
        }
        
        space_complexity = {
            "Data Structure": ["Linked List", "Binary Tree", "Heap"],
            "Complexity": ["O(n)", "O(n)", "O(n)"]
        }
        
        return {"time": time_complexity, "space": space_complexity}

def compare_performance():
    """
    A factory function to create and return a PerformanceAnalyzer instance.
    This function is kept for backward compatibility but direct instantiation
    of PerformanceAnalyzer is now preferred.
    """
    return PerformanceAnalyzer() 