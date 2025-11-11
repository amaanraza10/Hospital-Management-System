import subprocess
import time
import sys
import os
import threading
import tkinter as tk
from tkinter import messagebox

def start_flask_server():
    """Start Flask server in background"""
    try:
        print("🚀 Starting Flask API server...")
        # Set environment variable to disable Flask debug mode for subprocess
        env = os.environ.copy()
        env['FLASK_ENV'] = 'production'
        
        # Start Flask server
        flask_process = subprocess.Popen([
            sys.executable, "flask_app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        
        return flask_process
    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        return None

def start_tkinter_gui():
    """Start Tkinter GUI"""
    try:
        print("🖥️ Starting Tkinter GUI...")
        print("⏳ Waiting for Flask server to start...")
        
        # Wait for Flask to be ready (check connection)
        import urllib.request
        import urllib.error
        
        max_retries = 15
        retry_count = 0
        flask_ready = False
        
        while retry_count < max_retries and not flask_ready:
            try:
                time.sleep(1)
                urllib.request.urlopen('http://localhost:5000/api/test', timeout=1)
                flask_ready = True
                print("✅ Flask server is ready!")
            except (urllib.error.URLError, Exception):
                retry_count += 1
                print(f"⏳ Waiting for Flask... ({retry_count}/{max_retries})")
        
        if not flask_ready:
            raise Exception("Flask server failed to start after 15 seconds")
        
        # Import and run GUI
        from tkinter_flask_gui import HospitalFlaskGUI
        
        root = tk.Tk()
        app = HospitalFlaskGUI(root)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        messagebox.showerror("Error", f"Failed to start GUI: {e}")

def main():
    """Main function to start both Flask and Tkinter"""
    print("🏥 Hospital Management System - Flask + Tkinter")
    print("=" * 50)
    
    # Start Flask server in background
    flask_process = start_flask_server()
    
    if flask_process:
        try:
            # Start Tkinter GUI in main thread
            start_tkinter_gui()
        finally:
            # Clean up Flask process when GUI closes
            print("🛑 Shutting down Flask server...")
            flask_process.terminate()
            flask_process.wait()
            print("✅ System shutdown complete")
    else:
        print("❌ Cannot start system without Flask server")

if __name__ == "__main__":
    main()