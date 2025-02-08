#!/usr/bin/env python3
import subprocess
import os
import sys
import time
import signal
import atexit

class NodeRunner:
    def __init__(self):
        self.processes = []
        self.quickstart_path = os.path.expanduser("~/quickstart")
        atexit.register(self.cleanup)

    def build_config(self):
        """Build the configuration and messages for the bot."""
        build_cmd = f"cd {self.quickstart_path} && CONFIG=bot_quickstart CONFIG_MSGS=bot_quickstart_msgs make build"
        try:
            subprocess.run(build_cmd, shell=True, check=True)
            print("Configuration built successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error building configuration: {e}")
            sys.exit(1)

    def start_node(self, node_name):
        """Start a single node process."""
        cmd = f"python3 nodes/node_{node_name}.py"
        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                cwd=self.quickstart_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            self.processes.append(process)
            print(f"Started node_{node_name}.py")
            return process
        except Exception as e:
            print(f"Error starting node_{node_name}.py: {e}")
            return None

    def start_http_server(self):
        """Start the HTTP server in the examples directory."""
        cmd = "python3 -m http.server 8080"
        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                cwd=os.path.join(self.quickstart_path, "examples"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            self.processes.append(process)
            print("Started HTTP server on port 8080")
            return process
        except Exception as e:
            print(f"Error starting HTTP server: {e}")
            return None

    def cleanup(self):
        """Clean up all running processes."""
        print("\nStopping all processes...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        print("All processes stopped")

    def run(self):
        """Start all nodes and the HTTP server."""
        # Build configuration first
        self.build_config()

        # List of nodes to start
        nodes = ['imu', 'control', 'localization']

        # Start all nodes
        for node in nodes:
            self.start_node(node)

        # Start HTTP server
        self.start_http_server()

        print("\nAll nodes are running. Press Ctrl+C to stop all processes.")
        
        try:
            # Keep the main process running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nReceived interrupt signal")

def main():
    runner = NodeRunner()
    runner.run()

if __name__ == "__main__":
    main() 