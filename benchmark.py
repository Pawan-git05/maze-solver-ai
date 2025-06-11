"""
Performance benchmarking system for maze solving algorithms.
"""
import time
import json
import statistics
from typing import Dict, List, Any, Tuple
from pathlib import Path

from astar import AStarAlgorithm
from bfs import BFSAlgorithm
from dfs import DFSAlgorithm
from bidirectional import BidirectionalAlgorithm
from config import setup_logging
from utils import save_maze_image

logger = setup_logging()

class MazeBenchmark:
    """Benchmark system for comparing maze solving algorithms."""
    
    def __init__(self):
        self.algorithms = {
            'A*': AStarAlgorithm,
            'BFS': BFSAlgorithm,
            'DFS': DFSAlgorithm,
            'Bidirectional': BidirectionalAlgorithm
        }
        self.results = {}
    
    def run_single_benchmark(self, algorithm_name: str, maze_file: str, runs: int = 5) -> Dict[str, Any]:
        """
        Run benchmark for a single algorithm on a maze.
        
        Args:
            algorithm_name: Name of the algorithm
            maze_file: Path to maze file
            runs: Number of runs for averaging
            
        Returns:
            Benchmark results dictionary
        """
        if algorithm_name not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
        
        algorithm_class = self.algorithms[algorithm_name]
        results = {
            'algorithm': algorithm_name,
            'maze_file': maze_file,
            'runs': runs,
            'execution_times': [],
            'nodes_explored': [],
            'path_lengths': [],
            'success_rate': 0,
            'memory_usage': []
        }
        
        successful_runs = 0
        
        for run in range(runs):
            try:
                logger.info(f"Running {algorithm_name} benchmark {run + 1}/{runs}")
                
                # Run algorithm without animation for speed
                algorithm = algorithm_class(maze_file, animate=False)
                start_time = time.time()
                path, stats = algorithm.run()
                end_time = time.time()
                
                if path:
                    successful_runs += 1
                    results['execution_times'].append(stats['execution_time'])
                    results['nodes_explored'].append(stats['nodes_explored'])
                    results['path_lengths'].append(len(path))
                    
                    # Estimate memory usage based on data structures
                    memory_estimate = len(algorithm.visited) + len(algorithm.came_from)
                    if hasattr(algorithm, 'g_score'):
                        memory_estimate += len(algorithm.g_score)
                    if hasattr(algorithm, 'f_score'):
                        memory_estimate += len(algorithm.f_score)
                    results['memory_usage'].append(memory_estimate)
                
            except Exception as e:
                logger.error(f"Error in benchmark run {run + 1}: {e}")
        
        # Calculate statistics
        results['success_rate'] = successful_runs / runs
        
        if results['execution_times']:
            results['avg_execution_time'] = statistics.mean(results['execution_times'])
            results['std_execution_time'] = statistics.stdev(results['execution_times']) if len(results['execution_times']) > 1 else 0
            results['avg_nodes_explored'] = statistics.mean(results['nodes_explored'])
            results['avg_path_length'] = statistics.mean(results['path_lengths'])
            results['avg_memory_usage'] = statistics.mean(results['memory_usage'])
        
        return results
    
    def run_comprehensive_benchmark(self, maze_files: List[str], runs: int = 5) -> Dict[str, Any]:
        """
        Run comprehensive benchmark across multiple algorithms and mazes.
        
        Args:
            maze_files: List of maze file paths
            runs: Number of runs per algorithm per maze
            
        Returns:
            Complete benchmark results
        """
        comprehensive_results = {
            'timestamp': time.time(),
            'maze_files': maze_files,
            'runs_per_test': runs,
            'algorithms': {},
            'comparisons': {}
        }
        
        # Run benchmarks for each algorithm on each maze
        for algorithm_name in self.algorithms:
            comprehensive_results['algorithms'][algorithm_name] = {}
            
            for maze_file in maze_files:
                logger.info(f"Benchmarking {algorithm_name} on {maze_file}")
                try:
                    results = self.run_single_benchmark(algorithm_name, maze_file, runs)
                    comprehensive_results['algorithms'][algorithm_name][maze_file] = results
                except Exception as e:
                    logger.error(f"Failed to benchmark {algorithm_name} on {maze_file}: {e}")
        
        # Generate comparisons
        comprehensive_results['comparisons'] = self.generate_comparisons(comprehensive_results)
        
        return comprehensive_results
    
    def generate_comparisons(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comparison statistics between algorithms.
        
        Args:
            results: Comprehensive benchmark results
            
        Returns:
            Comparison statistics
        """
        comparisons = {
            'fastest_algorithm': {},
            'most_efficient_algorithm': {},
            'shortest_path_algorithm': {},
            'most_reliable_algorithm': {}
        }
        
        for maze_file in results['maze_files']:
            maze_comparisons = {
                'execution_time': {},
                'nodes_explored': {},
                'path_length': {},
                'success_rate': {}
            }
            
            for algorithm_name in results['algorithms']:
                if maze_file in results['algorithms'][algorithm_name]:
                    algo_results = results['algorithms'][algorithm_name][maze_file]
                    
                    if algo_results.get('avg_execution_time'):
                        maze_comparisons['execution_time'][algorithm_name] = algo_results['avg_execution_time']
                        maze_comparisons['nodes_explored'][algorithm_name] = algo_results['avg_nodes_explored']
                        maze_comparisons['path_length'][algorithm_name] = algo_results['avg_path_length']
                        maze_comparisons['success_rate'][algorithm_name] = algo_results['success_rate']
            
            # Find best performers
            if maze_comparisons['execution_time']:
                comparisons['fastest_algorithm'][maze_file] = min(
                    maze_comparisons['execution_time'], 
                    key=maze_comparisons['execution_time'].get
                )
                
                comparisons['most_efficient_algorithm'][maze_file] = min(
                    maze_comparisons['nodes_explored'], 
                    key=maze_comparisons['nodes_explored'].get
                )
                
                comparisons['shortest_path_algorithm'][maze_file] = min(
                    maze_comparisons['path_length'], 
                    key=maze_comparisons['path_length'].get
                )
                
                comparisons['most_reliable_algorithm'][maze_file] = max(
                    maze_comparisons['success_rate'], 
                    key=maze_comparisons['success_rate'].get
                )
        
        return comparisons
    
    def save_results(self, results: Dict[str, Any], filename: str = "benchmark_results.json"):
        """Save benchmark results to JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Benchmark results saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a human-readable benchmark report.
        
        Args:
            results: Benchmark results
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("MAZE SOLVING ALGORITHM BENCHMARK REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {time.ctime(results['timestamp'])}")
        report.append(f"Mazes tested: {len(results['maze_files'])}")
        report.append(f"Runs per test: {results['runs_per_test']}")
        report.append("")
        
        # Algorithm performance summary
        report.append("ALGORITHM PERFORMANCE SUMMARY")
        report.append("-" * 40)
        
        for algorithm_name in results['algorithms']:
            report.append(f"\n{algorithm_name}:")
            
            total_tests = 0
            total_successes = 0
            avg_times = []
            avg_nodes = []
            
            for maze_file in results['algorithms'][algorithm_name]:
                maze_results = results['algorithms'][algorithm_name][maze_file]
                total_tests += maze_results['runs']
                total_successes += int(maze_results['success_rate'] * maze_results['runs'])
                
                if maze_results.get('avg_execution_time'):
                    avg_times.append(maze_results['avg_execution_time'])
                    avg_nodes.append(maze_results['avg_nodes_explored'])
            
            if avg_times:
                report.append(f"  Overall Success Rate: {total_successes/total_tests:.1%}")
                report.append(f"  Average Execution Time: {statistics.mean(avg_times):.4f}s")
                report.append(f"  Average Nodes Explored: {statistics.mean(avg_nodes):.0f}")
        
        # Best performers
        report.append("\n\nBEST PERFORMERS BY CATEGORY")
        report.append("-" * 40)
        
        categories = {
            'fastest_algorithm': 'Fastest Algorithm',
            'most_efficient_algorithm': 'Most Efficient (Fewest Nodes)',
            'shortest_path_algorithm': 'Shortest Path',
            'most_reliable_algorithm': 'Most Reliable'
        }
        
        for category, title in categories.items():
            report.append(f"\n{title}:")
            for maze_file, algorithm in results['comparisons'][category].items():
                report.append(f"  {Path(maze_file).name}: {algorithm}")
        
        return "\n".join(report)

def main():
    """Main function to run benchmarks."""
    import sys
    
    # Default maze files to test
    maze_files = ["manual_maze.txt", "random_maze.txt"]
    
    # Check if specific maze files were provided
    if len(sys.argv) > 1:
        maze_files = sys.argv[1:]
    
    # Create benchmark instance
    benchmark = MazeBenchmark()
    
    # Run comprehensive benchmark
    logger.info("Starting comprehensive benchmark...")
    results = benchmark.run_comprehensive_benchmark(maze_files, runs=3)
    
    # Save results
    benchmark.save_results(results)
    
    # Generate and print report
    report = benchmark.generate_report(results)
    print(report)
    
    # Save report to file
    with open("benchmark_report.txt", "w") as f:
        f.write(report)
    
    logger.info("Benchmark completed successfully!")

if __name__ == "__main__":
    main()
