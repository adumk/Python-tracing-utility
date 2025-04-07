import threading
import time
import inspect
from importlib import import_module
from collections import defaultdict
from functools import wraps

console_lock = threading.Lock()

class Profiler:
    def __init__(self):
        self.enabled = False
        self.tracked = {}
        self.data = defaultdict(lambda: {'total_time': 0.0, 'calls': 0})
        self.listener_thread = None

    def enable(self, func_list):
        if self.enabled:
            self.disable()
        self.enabled = True
        if func_list:
            for func in func_list:
                self._wrap_function(func)

    def start_cli(self, initial_func_list=None):
        if not self.listener_thread or not self.listener_thread.is_alive():
            self.listener_thread = threading.Thread(
                target=self._listen_loop, args=(initial_func_list,), daemon=True
            )
            self.listener_thread.start()

    def _start_listener(self, func_list):
        if not self.listener_thread or not self.listener_thread.is_alive():
            self.listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.listener_thread.start()

    def _listen_loop(self, func_list):
        if func_list:
            self.disable()
            print("\nProfiler loaded. Type 'start' to enable it.\n")
        while True:
            with console_lock:
                command = input("\n>>> Profiler commands [results / start / stop]: \n\n")

            if command == "results":
                if self.enabled:
                    self.print_results()
                else:
                    print("Profiling disabled. Type 'start' to enable\n\n")


            elif command == "stop":
                self.disable()
                self.print_results()
                print("Profiling disabled. Type 'start' to enable\n\n")

            elif command == "start":
                self.enable(func_list)
                #self.from_config('config.txt')
                print("Profiling enabled. Type 'stop' to disable\n\n")

    def disable(self):
        if not self.enabled:
            return
        for func, (original, module, name) in self.tracked.items():
            setattr(module, name, original)
        self.tracked.clear()
        self.enabled = False

    def _wrap_function(self, func):
        module = inspect.getmodule(func)
        if not module:
            return
        name = func.__name__
        if getattr(module, name, None) is not func:
            return  # Cannot wrap
        original = func

        @wraps(original)
        def wrapper(*args, **kwargs):
            print(f"Calling {original.__name__}")
            start = time.perf_counter()
            result = original(*args, **kwargs)
            duration = time.perf_counter() - start
            self.data[func]['total_time'] += duration
            self.data[func]['calls'] += 1
            return result

        setattr(module, name, wrapper)
        self.tracked[func] = (original, module, name)
        #print(f"Wrapped function: {name}")  # Debug statement

    def add_function(self, func):
        if self.enabled and func not in self.tracked:
            self._wrap_function(func)

    def remove_function(self, func):
        if func in self.tracked:
            original, module, name = self.tracked[func]
            setattr(module, name, original)
            del self.tracked[func]

    def get_results(self):
        return self.data

    def print_results(self):
        print("\n")
        print("-" * 130)
        print("{:<24} | {:<36} | {:<18} | {:<36}".format(
            "Function", "Total (ms)", "Calls", "Avg (ms)"))
        print("-" * 130)
        for func, stats in self.data.items():
            avg = stats['total_time'] / stats['calls'] if stats['calls'] else 0
            print("{:<24} | {:<36.3f} | {:<18} | {:<36.3f}".format(
                func.__name__, stats['total_time'] * 10 ** 3,
                stats['calls'], avg * 10 ** 3))
        print("-" * 130)
        print("\n")

    def load_config(self, config_path):
        try:
            with open(config_path, 'r') as file:
                config = file.read().splitlines()
                func_list = []
                for line in config:
                    try:
                        module_name, func_name = line.split('.')
                        module = import_module(module_name)
                        func = getattr(module, func_name)
                        func_list.append(func)
                    except Exception as e:
                        print(f"Error loading function from config: {line}. Error: {e}")
                #print(func_list)
                return func_list
        except Exception as e:
            print(f"Error reading config: {e}")
            return []

    def update_from_config(self, config_path):
        func_list = self.load_config(config_path)
        self.disable()
        self.enable(func_list)
        self.start_cli(func_list)

    @classmethod
    def from_config(cls, config_path):
        profiler = cls()
        profiler.update_from_config(config_path)
        return profiler

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disable()

def profile(profiler):
    """Decorator to dynamically add functions to profiler."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if profiler.enabled and func not in profiler.tracked:
                profiler.add_function(func)
            return func(*args, **kwargs)
        return wrapper
    return decorator

#
