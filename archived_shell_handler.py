import os
import signal
import subprocess
import argparse
import threading

class ShellHandler:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.shell_active = False
        self.process = None

    def start_listener(self):
        print(f"Starting netcat listener on {self.host}:{self.port}...")
        self.shell_active = True
        self.process = subprocess.Popen(['nc', '-lvp', str(self.port)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.listen_to_shell()

    def listen_to_shell(self):
        def read_output():
            while self.shell_active:
                output = self.process.stdout.read(1)
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    print(output, end='', flush=True)

        threading.Thread(target=read_output).start()

        while self.shell_active:
            try:
                command = input().strip()
                if command.lower() in ['quit', 'exit']:
                    self.shell_active = False
                    break
                self.process.stdin.write(command + '\n')
                self.process.stdin.flush()
            except EOFError:
                break

        self.cleanup()

    def cleanup(self):
        if self.process:
            self.process.terminate()
        self.shell_active = False
        print("Shell handler closed.")

def run(args):
    handler = ShellHandler(host=args.host, port=args.port)
    handler.start_listener()

def main():
    parser = argparse.ArgumentParser(description='Shell handler module.')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the listener to')
    parser.add_argument('--port', type=int, default=1337, help='Port to bind the listener to')
    args = parser.parse_args()

    run(args)

if __name__ == "__main__":
    main()
