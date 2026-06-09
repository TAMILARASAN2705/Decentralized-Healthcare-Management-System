"""
Startup Script for Healthcare Management System
Runs both Python backend and web server
"""

import subprocess
import sys
import os
from pathlib import Path


def run_backend():
    """Run the Python backend"""
    print("🚀 Starting Python Backend...")
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    subprocess.run([sys.executable, "main.py"])


def run_web_server():
    """Run the web server"""
    print("🌐 Starting Web Server...")
    web_dir = Path(__file__).parent / "web"
    os.chdir(web_dir)
    subprocess.run([sys.executable, "server.py"])


def main():
    """Main function to run the system"""
    print("=== Healthcare Management System Launcher ===")
    print("Python Backend - Version 2.0.0")
    print("\nChoose an option:")
    print("1. Run Backend (Console Interface)")
    print("2. Run Web Server (Web Interface)")
    print("3. Run Both (Backend + Web Server)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        run_backend()
    elif choice == "2":
        run_web_server()
    elif choice == "3":
        print("Starting both backend and web server...")
        # Start backend in background
        backend_process = subprocess.Popen(
            [sys.executable, "backend/main.py"],
            cwd=Path(__file__).parent
        )
        
        # Start web server in background
        web_process = subprocess.Popen(
            [sys.executable, "web/server.py"],
            cwd=Path(__file__).parent
        )
        
        print("\n✅ Both servers are running!")
        print("🌐 Web Interface: http://localhost:8080")
        print("🖥️ Backend Console: Running in background")
        print("\nPress Ctrl+C to stop both servers")
        
        try:
            # Wait for both processes
            backend_process.wait()
            web_process.wait()
        except KeyboardInterrupt:
            print("\n⏹️ Stopping servers...")
            backend_process.terminate()
            web_process.terminate()
            print("✅ Servers stopped")
    elif choice == "4":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    main()
