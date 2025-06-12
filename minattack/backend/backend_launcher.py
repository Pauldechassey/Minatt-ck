import os
import sys
from uvicorn import Config, Server
from minattack.backend.app.main import app


def run_backend(port: int):
    print(f"[BACKEND] Running in PID: {os.getpid()} on port {port}")
    config = Config(app=app, host="127.0.0.1", port=port, log_level="debug")
    server = Server(config)

    server.run()
    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    #loop.run_until_complete(server.serve())


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000

    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Usage: python backend_launcher.py <port>")

    print(f"[INFO] Starting backend on {host}:{port}")
    run_backend(port)
