import sys
import uvicorn


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000

    try :
        port = int(sys.argv[1])
    except (IndexError, ValueError) :
        print("Usage: python backend_launcher.py <port>")

    print(f"[INFO] Starting backend on {host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port)