import subprocess
import sys
import os
import threading
import json
from datetime import datetime

# Use a relative path for logging or a temp dir on Linux
if os.name == 'nt':
    LOG_FILE = r"C:\Users\gfood\Documents\Cloud_guardian\cloudguardian\mcp_debug.log"
else:
    LOG_FILE = "/tmp/mcp_debug.log"

def log(msg):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now()} | {msg}\n")
    except:
        pass

def main():
    log("WRAPPER STARTED")
    
    env = os.environ.copy()
    
    # Determine the command based on the environment
    if os.name == 'nt':
        # Local Windows paths
        node_cmd = r"C:\Program Files\nodejs\node.exe"
        server_js = r"C:\Users\gfood\AppData\Roaming\npm\node_modules\@dynatrace-oss\dynatrace-mcp-server\index.js"
        command = [node_cmd, server_js]
    else:
        # Linux / Cloud Run paths
        # We installed it globally via npm, so it should be in the PATH
        command = ["mcp-server-dynatrace"]

    log(f"STARTING COMMAND: {' '.join(command)}")

    try:
        proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1
        )
        log(f"PROCESS STARTED pid={proc.pid}")
    except Exception as e:
        log(f"FAILED TO START PROCESS: {e}")
        return

    def forward_stdin():
        try:
            for line in sys.stdin:
                if proc.stdin:
                    proc.stdin.write(line)
                    proc.stdin.flush()
        except Exception as e:
            log(f"STDIN ERROR: {e}")

    def read_stderr():
        try:
            for line in proc.stderr:
                log(f"NODE STDERR: {line.rstrip()}")
        except Exception as e:
            log(f"STDERR ERROR: {e}")

    threading.Thread(target=forward_stdin, daemon=True).start()
    threading.Thread(target=read_stderr, daemon=True).start()

    try:
        for line in proc.stdout:
            stripped = line.strip()
            if stripped.startswith('{') or stripped.startswith('['):
                sys.stdout.write(line)
                sys.stdout.flush()
            else:
                log(f"FILTERED OUT: {stripped[:100]}")
    except Exception as e:
        log(f"STDOUT ERROR: {e}")

    log("WRAPPER ENDED")

if __name__ == "__main__":
    main()
