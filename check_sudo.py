#!/usr/bin/env python3

import os
import sys
import subprocess

def main():
    # Check if the script is running with sudo permissions
    if os.geteuid() != 0:
        print("This script needs to be run with sudo permissions.")
        sys.exit(1)

    # Run the main script with sudo permissions
    script_path = os.path.join(os.path.dirname(__file__), 'main_script.py')
    subprocess.run(['sudo', 'python3', script_path] + sys.argv[1:])

if __name__ == "__main__":
    main()