import unittest
import sys
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for tests

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from emergency_response.utils.performance_analyzer import PerformanceAnalyzer
from emergency_response.data_structures.emergency import Emergency

class TestPerformanceAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up the test environment before each test."""
        self.analyzer = PerformanceAnalyzer()
    
    def test_generate_random_emergencies(self):
        """Test the generation of random emergency data."""
        count = 20
        emergencies = self.analyzer.generate_random_emergencies(count)
        
        # Verify the number of generated emergencies
        self.assertEqual(len(emergencies), count)
        
        # Verify that each item is an Emergency instance
        for emergency in emergencies:
            self.assertIsInstance(emergency, Emergency)
            self.assertIn(emergency.severity_level, range(1, 11))
    
    def test_measure_performance_populates_results(self):
        """Test that measurement methods correctly populate the results dictionary."""
        data_sizes = [10, 20]
        operation = "enqueue"
        
        # Run the measurement
        self.analyzer.measure_enqueue_performance(data_sizes)
        
        # Check if the results dictionary is populated correctly
        self.assertIn(operation, self.analyzer.results)
        results_for_op = self.analyzer.results[operation]
        
        self.assertIn('Linked List', results_for_op)
        self.assertIn('Binary Tree', results_for_op)
        self.assertIn('Heap', results_for_op)
        
        # Check if the number of results matches the number of data sizes
        self.assertEqual(len(results_for_op['Linked List']), len(data_sizes))
        self.assertEqual(len(results_for_op['Binary Tree']), len(data_sizes))
        self.assertEqual(len(results_for_op['Heap']), len(data_sizes))

if __name__ == '__main__':
    unittest.main() 