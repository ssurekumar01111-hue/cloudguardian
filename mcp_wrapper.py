import subprocess
import sys
import os
import threading
import shutil
import platform

def main():
    env = os.environ.copy()
    
    print(f"MCP_WRAPPER: platform={platform.system()}", 
          file=sys.stderr, flush=True)
    
    if platform.system() == "Windows":
        # On Windows, find and run the .cmd file directly via shell
        mcp_cmd = shutil.which('mcp-server-dynatrace.cmd') or \
                  shutil.which('mcp-server-dynatrace')
        print(f"MCP_WRAPPER: cmd={mcp_cmd}", 
              file=sys.stderr, flush=True)
        proc = subprocess.Popen(
            [mcp_cmd],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1,
            shell=True
        )
    else:
        # On Linux (Cloud Run), use node + binary directly
        node = shutil.which('node') or '/usr/bin/node'
        mcp = (shutil.which('mcp-server-dynatrace') or
               '/usr/local/bin/mcp-server-dynatrace')
        print(f"MCP_WRAPPER: node={node}, mcp={mcp}", 
              file=sys.stderr, flush=True)
        proc = subprocess.Popen(
            [node, mcp],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1
        )
    
    print(f"MCP_WRAPPER: spawned pid={proc.pid}", 
          file=sys.stderr, flush=True)

    def forward_stdin():
        try:
            for line in sys.stdin:
                if proc.stdin:
                    proc.stdin.write(line)
                    proc.stdin.flush()
        except: pass

    def read_stderr():
        try:
            for line in proc.stderr:
                print(f"MCP_SERVER: {line.rstrip()}", 
                      file=sys.stderr, flush=True)
        except: pass

    threading.Thread(target=forward_stdin, daemon=True).start()
    threading.Thread(target=read_stderr, daemon=True).start()

    for line in proc.stdout:
        stripped = line.strip()
        if stripped.startswith('{') or stripped.startswith('['):
            sys.stdout.write(line)
            sys.stdout.flush()

if __name__ == '__main__':
    main()