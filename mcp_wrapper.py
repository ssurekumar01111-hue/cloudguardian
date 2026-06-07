import subprocess
import sys
import os
import threading

def main():
    env = os.environ.copy()
    
    # Find node and mcp-server-dynatrace with explicit fallback paths
    import shutil
    node = shutil.which('node') or '/usr/bin/node' or '/usr/local/bin/node'
    mcp = (shutil.which('mcp-server-dynatrace') or 
           '/usr/local/bin/mcp-server-dynatrace' or
           '/usr/bin/mcp-server-dynatrace')
    
    # Log to stderr for debugging
    print(f"MCP_WRAPPER: node={node}, mcp={mcp}", file=sys.stderr, flush=True)
    print(f"MCP_WRAPPER: DT_ENV={env.get('DT_ENVIRONMENT','NOT SET')}", file=sys.stderr, flush=True)
    
    if not os.path.exists(mcp):
        # Try finding via npm global prefix
        try:
            npm_prefix = subprocess.check_output(['npm', 'prefix', '-g'], text=True).strip()
            mcp = os.path.join(npm_prefix, 'bin', 'mcp-server-dynatrace')
            print(f"MCP_WRAPPER: found via npm prefix: {mcp}", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"MCP_WRAPPER: npm prefix failed: {e}", file=sys.stderr, flush=True)
    
    proc = subprocess.Popen(
        [node, mcp],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
        bufsize=1
    )
    print(f"MCP_WRAPPER: spawned pid={proc.pid}", file=sys.stderr, flush=True)

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
                print(f"MCP_SERVER: {line.rstrip()}", file=sys.stderr, flush=True)
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