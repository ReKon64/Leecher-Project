import argparse
import inspect
import subprocess
import csv

class Module:
    def __init__(self, **kwargs):
        # Dynamically assign instance variables
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.process = None

    @classmethod
    def cli(cls, **kwargs):
        # Create argument parser
        parser = argparse.ArgumentParser(description="Dynamically generate CLI arguments for class")
        
        # Get the __init__ method signature
        init_signature = inspect.signature(cls.__init__)
        init_params = init_signature.parameters
        
        # Skip 'self', and create CLI arguments for the other parameters
        for param, param_info in init_params.items():
            if param != 'kwargs':  # Skip 'kwargs' parameter
                if param in kwargs and kwargs[param] is not None:
                    # If the parameter is provided through command line, use its value
                    default = kwargs[param]
                elif param_info.default != inspect.Parameter.empty:
                    # Use the default value defined in the __init__ method
                    default = param_info.default
                else:
                    # If there's no default value, require the argument
                    default = argparse.SUPPRESS
                parser.add_argument(f'--{param}', default=default)
        
        # Parse arguments
        args = parser.parse_args()
        
        # Convert argparse.Namespace to a dictionary
        args_dict = vars(args)
        
        # Create and return an instance of the class with the parsed arguments
        return cls(**args_dict)

    def command_to_execute(self):
        if 'command' in self.__dict__ and self.command:
            # Execute the provided command
            self._execute_command(self.command)
        else:
            # Read targets from the CSV file
            with open(self.csv_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    target = row['IP']
                    self._execute_command(target)

    def _execute_command(self, target):
        # Replace $target in the command with the actual target
        command = self.command.replace('$target', target)
        print(f"Executing command: {command}")
        
        # Split the command into a list for subprocess
        command_list = command.split()
        
        # Start the subprocess
        self.process = subprocess.Popen(command_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for the process to complete and get output
        stdout, stderr = self.process.communicate()
        print(f"Output for {target}:\n{stdout}")
        if stderr:
            print(f"Error for {target}:\n{stderr}")

# Example usage
if __name__ == "__main__":
    # Create an instance of Module from CLI arguments
    instance = Module.cli(command="feroxbuster --url http://10.10.11.13 --threads 120")
    
    # Execute the command for the provided target(s)
    instance.command_to_execute()
