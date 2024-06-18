import argparse
import inspect
import subprocess

class Module:
    def __init__(self, **kwargs):
        # Dynamically assign instance variables
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.process = None

    @classmethod
    def cli(cls):
        # Create argument parser
        parser = argparse.ArgumentParser(description="Dynamically generate CLI arguments for class")
        
        # Get the __init__ method signature
        init_signature = inspect.signature(cls.__init__)
        init_params = init_signature.parameters
        
        # Skip 'self' and create CLI arguments for the other parameters
        for param in list(init_params.keys())[1:]:
            parser.add_argument(f'--{param}', required=True)
        
        # Parse arguments
        args = parser.parse_args()
        
        # Convert argparse.Namespace to a dictionary
        args_dict = vars(args)
        
        # Create and return an instance of the class with the parsed arguments
        return cls(**args_dict)

    

    def command_to_execute(self):
        for attr, value in self.__dict__.items():
            if attr == "command":
                print(f"Command: {value}")


##Instructions I want you to do start here
''' here we will iterate over inputted command and construct a self.process object. Example:
       
instance = Module(command = "feroxbuster --url $target --threads 120")
        
Will result in: 

               # self.process = subprocess.Popen(['feroxbuster', '--url', '172.16.0.1', '--threads', '120'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# if "multitarget" arg passed, instead of spawning more subprocesess, pass it as the command requires, comma seperated etc.
# Otherwise, spawn up to 4 instances of the process, store info in the target list target,commandnamestatuscompletion
# Whenever started, check if target has been attacked already, if yes ,pass. Force the run if instance is spawned with "forcedd" arg
'''
##Instructions I want you to do end here. Rest is code



# If running as a script
#if __name__ == "__main__":
#    instance = Module.cli()
#    print(f"Created instance: {instance}")
#    for key in vars(instance).keys():
#        print(f"{key}: {getattr(instance, key)}")
