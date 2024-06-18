#!/usr/bin/env python3

import os
import subprocess
import importlib.util
import sys
import readline
import shlex

class C2Framework:
    def __init__(self, modules_dir):
        self.modules_dir = modules_dir
        self.shell_handler = None

    def load_module(self, module_name):
        module_path = os.path.join(self.modules_dir, f"{module_name}.py")
        if not os.path.exists(module_path):
            print(f"Module '{module_name}' not found.")
            print(f"Running '{module_name}' as zsh command.\n")
            return None

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def execute_command(self, command_line):
        args = shlex.split(command_line)
        command = args[0]
        
        module = self.load_module(command)
        if module:
            # Rebuild the command line to include 'module_name' and its arguments
            module_args = ['python3', os.path.join(self.modules_dir, f"{command}.py")] + args[1:]
            subprocess.run(module_args)
        else:
            # Try to run the command as a Zsh command
            try:
                result = subprocess.run(['zsh', '-c', command_line], capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            except FileNotFoundError:
                print(f"Command '{command}' not found.")
            except Exception as e:
                print(f"Error executing command '{command}': {e}")

    def run(self):
        while True:
            try:
                command_line = input("L2> ").strip()
                if command_line in ["quit", "qu", "exit"]:
                    break
                self.execute_command(command_line)
            except KeyboardInterrupt:
                print("\nPlease type 'qu', 'quit' or 'exit' to leave the shell.")

if __name__ == "__main__":
    modules_dir = os.path.join(os.path.dirname(__file__), 'modules')
    c2 = C2Framework(modules_dir)
    c2.run()
