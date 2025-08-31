# Coding By BenyVK t.me/i36VK

import os
import subprocess
import sys
import time
import signal

def clear_console():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def find_and_run_samp_server():
    desktop_paths = [
        os.path.join(os.environ['USERPROFILE'], 'Desktop'),
        os.path.join(os.environ['PUBLIC'], 'Desktop')
    ]
    
    target_file = "samp-server.exe"
    
    folder_name = input("Enter the folder name on desktop that contains samp-server.exe: ").strip()
    
    if not folder_name:
        print("No folder name entered. Exiting...")
        return None, None
    
    print(f"Searching for folder '{folder_name}' on desktop...")
    
    target_folder = None
    
    for desktop_path in desktop_paths:
        if os.path.exists(desktop_path):
            print(f"Searching in: {desktop_path}")
            
            folder_path = os.path.join(desktop_path, folder_name)
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                potential_file = os.path.join(folder_path, target_file)
                if os.path.exists(potential_file):
                    target_folder = folder_path
                    print(f"Found {target_file} in: {folder_path}")
                    break
                else:
                    print(f"Folder found, but {target_file} not found inside it")
            else:
                print(f"Folder '{folder_name}' not found in this desktop path")
    
    if target_folder:
        try:
            print(f"Changing directory to: {target_folder}")
            os.chdir(target_folder)
            
            print("Running samp-server.exe...")
            process = subprocess.Popen([target_file], cwd=target_folder)
            print("samp-server.exe started successfully!")
            print("\nCommands:")
            print("- Type 'exit' to stop the server and close")
            print("- Type 'restart' to restart the server")
            
            return process, target_folder
            
        except Exception as e:
            print(f"Error running {target_file}: {e}")
            return None, None
    else:
        print(f"Could not find folder '{folder_name}' with {target_file} on desktop")
        return None, None

def stop_server(process):
    """Stop the server process gracefully"""
    print("Stopping server...")
    process.terminate()
    
    try:
        process.wait(timeout=5)
        print("Server stopped gracefully.")
    except subprocess.TimeoutExpired:
        print("Server not responding, forcing shutdown...")
        process.kill()
        process.wait()
        print("Server force stopped.")

def restart_server(process, target_folder):
    """Restart the server with clean console"""
    stop_server(process)
    
    time.sleep(2)
    clear_console()
    
    print("🔄 Restarting server...")
    print("Clearing previous messages...")
    time.sleep(1)
    clear_console()
    
    try:
        new_process = subprocess.Popen(["samp-server.exe"], cwd=target_folder)
        print("✅ Server restarted successfully!")
        print("\nCommands:")
        print("- Type 'exit' to stop the server and close")
        print("- Type 'restart' to restart the server")
        
        return new_process
        
    except Exception as e:
        print(f"❌ Error restarting server: {e}")
        return None

def monitor_server(process, target_folder):
    """Monitor the server process and handle user input"""
    try:
        while True:
            user_input = input().strip().lower()
            
            if user_input == "exit":
                stop_server(process)
                print("Closing console...")
                time.sleep(1)
                break
                
            elif user_input == "restart":
                new_process = restart_server(process, target_folder)
                if new_process:
                    process = new_process
                else:
                    print("Failed to restart server. Exiting...")
                    break
                
            else:
                print("Unknown command. Available commands:")
                print("'exit' - stop server and close")
                print("'restart' - restart server")
                
    except KeyboardInterrupt:
        print("\nStopping server...")
        stop_server(process)
        print("Server stopped.")

if __name__ == "__main__":
    while True:
        clear_console()
        print("=== SA-MP Server Launcher ===")
        server_process, target_folder = find_and_run_samp_server()
        
        if server_process and target_folder:
            monitor_server(server_process, target_folder)
            
            restart_choice = input("\nWould you like to start the launcher again? (y/n): ").strip().lower()
            if restart_choice not in ['y', 'yes']:
                break
        else:
            retry = input("Would you like to try again? (y/n): ").strip().lower()
            if retry not in ['y', 'yes']:
                break
