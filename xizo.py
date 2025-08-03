import speech_recognition as sr
import subprocess
import os
import sys
import threading
import time
import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import psutil

class XizoAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.is_running = True
        self.wake_word = "xizo"
        
        # Command patterns
        self.commands = {
            "open": self.open_program,
            "launch": self.open_program,
            "start": self.open_program,
            "write": self.write_text,
            "type": self.write_text,
            "search": self.search_web,
            "google": self.search_web,
            "find": self.search_web,
            "close": self.close_program,
            "exit": self.close_program,
            "quit": self.close_program
        }
        
        # Common programs mapping
        self.programs = {
            "notepad": "notepad.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "explorer": "explorer.exe",
            "control panel": "control.exe",
            "task manager": "taskmgr.exe"
        }
        
        self.setup_gui()
        self.adjust_for_ambient_noise()
        
    def adjust_for_ambient_noise(self):
        """Adjust the recognizer sensitivity to ambient noise"""
        print("Adjusting for ambient noise... Please be quiet.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ambient noise adjustment complete.")
    
    def setup_gui(self):
        """Setup the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Xizo Voice Assistant")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🧠 Xizo Voice Assistant", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Status: Ready", 
                                     font=("Arial", 12))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Listen button
        self.listen_button = ttk.Button(main_frame, text="Start Listening", 
                                       command=self.toggle_listening)
        self.listen_button.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Command Log", padding="5")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = tk.Text(log_frame, height=8, width=45, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        print(log_entry.strip())
    
    def toggle_listening(self):
        """Toggle listening state"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start listening for voice commands"""
        self.is_listening = True
        self.listen_button.config(text="Stop Listening")
        self.status_label.config(text="Status: Listening...")
        self.log_message("Started listening for voice commands")
        
        # Start listening thread
        self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listen_thread.start()
    
    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        self.listen_button.config(text="Start Listening")
        self.status_label.config(text="Status: Ready")
        self.log_message("Stopped listening")
    
    def listen_loop(self):
        """Main listening loop"""
        while self.is_listening and self.is_running:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    self.log_message(f"Heard: {text}")
                    
                    if self.wake_word in text:
                        self.process_command(text)
                    
                except sr.UnknownValueError:
                    pass  # No speech detected
                except sr.RequestError as e:
                    self.log_message(f"Speech recognition error: {e}")
                    
            except Exception as e:
                if self.is_listening:  # Only log if we're supposed to be listening
                    self.log_message(f"Listening error: {e}")
                time.sleep(0.1)
    
    def process_command(self, text):
        """Process voice command"""
        # Remove wake word
        command_text = text.replace(self.wake_word, "").strip()
        
        # Find matching command
        for cmd_keyword, cmd_function in self.commands.items():
            if cmd_keyword in command_text:
                try:
                    # Extract arguments
                    args = command_text.replace(cmd_keyword, "").strip()
                    cmd_function(args)
                    return
                except Exception as e:
                    self.log_message(f"Error executing command: {e}")
        
        # If no specific command found, treat as text to write
        self.write_text(command_text)
    
    def open_program(self, program_name):
        """Open a program or file"""
        program_name = program_name.strip()
        
        # Check if it's a known program
        if program_name in self.programs:
            program_path = self.programs[program_name]
            try:
                subprocess.Popen(program_path)
                self.log_message(f"Opened {program_name}")
            except Exception as e:
                self.log_message(f"Failed to open {program_name}: {e}")
        else:
            # Try to open as a file or program
            try:
                subprocess.Popen(program_name)
                self.log_message(f"Opened {program_name}")
            except Exception as e:
                self.log_message(f"Failed to open {program_name}: {e}")
    
    def write_text(self, text):
        """Write text to active application"""
        if not text.strip():
            return
            
        try:
            # Type the text
            pyautogui.write(text)
            self.log_message(f"Wrote text: {text}")
        except Exception as e:
            self.log_message(f"Failed to write text: {e}")
    
    def search_web(self, query):
        """Search the web"""
        if not query.strip():
            return
            
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            subprocess.Popen(["start", search_url], shell=True)
            self.log_message(f"Searched for: {query}")
        except Exception as e:
            self.log_message(f"Failed to search: {e}")
    
    def close_program(self, program_name):
        """Close a program"""
        program_name = program_name.strip()
        
        try:
            if program_name in self.programs:
                program_path = self.programs[program_name]
                # Kill process by name
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] and program_path.lower() in proc.info['name'].lower():
                        proc.terminate()
                        self.log_message(f"Closed {program_name}")
                        return
            else:
                # Try to close by name
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] and program_name.lower() in proc.info['name'].lower():
                        proc.terminate()
                        self.log_message(f"Closed {program_name}")
                        return
                        
            self.log_message(f"Could not find {program_name} to close")
        except Exception as e:
            self.log_message(f"Failed to close {program_name}: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        self.is_running = False
        self.is_listening = False
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.log_message("Xizo Voice Assistant started")
        self.log_message("Say 'Xizo' followed by your command")
        self.log_message("Examples: 'Xizo open notepad', 'Xizo write hello world'")
        self.root.mainloop()

if __name__ == "__main__":
    app = XizoAssistant()
    app.run() 