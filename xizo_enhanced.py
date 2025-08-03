"""
Enhanced Xizo Voice Assistant
Using the new voice control module with advanced features
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import json
import os
from datetime import datetime
import threading

# Import voice control modules
from voice_control import SpeechEngine, CommandProcessor, VoiceFeedback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class XizoEnhanced:
    """Enhanced Xizo Voice Assistant with advanced voice control"""
    
    def __init__(self):
        self.is_running = True
        
        # Initialize voice control components
        self.speech_engine = SpeechEngine(callback=self._on_voice_command)
        self.command_processor = CommandProcessor()
        self.voice_feedback = VoiceFeedback(voice_enabled=True)
        
        # Setup GUI
        self.setup_gui()
        
        # Load configuration
        self.load_config()
        
        # Initialize status
        self.update_status()
        
    def setup_gui(self):
        """Setup the enhanced GUI interface"""
        self.root = tk.Tk()
        self.root.title("🧠 Xizo Enhanced Voice Assistant")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main tab
        self.setup_main_tab()
        
        # Settings tab
        self.setup_settings_tab()
        
        # History tab
        self.setup_history_tab()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_main_tab(self):
        """Setup the main control tab"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="Main")
        
        # Title
        title_label = ttk.Label(main_frame, text="🧠 Xizo Enhanced Voice Assistant", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding="10")
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.status_text = tk.Text(status_frame, height=6, width=70, wrap=tk.WORD)
        status_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Voice Control", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Voice control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        self.listen_button = ttk.Button(button_frame, text="Start Listening", 
                                       command=self.toggle_listening)
        self.listen_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.feedback_button = ttk.Button(button_frame, text="Toggle Voice Feedback", 
                                         command=self.toggle_voice_feedback)
        self.feedback_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Manual command entry
        cmd_frame = ttk.LabelFrame(main_frame, text="Manual Command Entry", padding="10")
        cmd_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.cmd_entry = ttk.Entry(cmd_frame, width=60)
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.cmd_entry.bind('<Return>', self.execute_manual_command)
        
        cmd_button = ttk.Button(cmd_frame, text="Execute", command=self.execute_manual_command)
        cmd_button.pack(side=tk.RIGHT)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Command Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.log_text = tk.Text(log_frame, height=12, width=70, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_settings_tab(self):
        """Setup the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Voice settings
        voice_frame = ttk.LabelFrame(settings_frame, text="Voice Settings", padding="10")
        voice_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Wake words
        ttk.Label(voice_frame, text="Wake Words:").pack(anchor=tk.W)
        self.wake_words_text = tk.Text(voice_frame, height=3, width=50)
        self.wake_words_text.pack(fill=tk.X, pady=(0, 10))
        
        # Voice feedback settings
        self.voice_feedback_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(voice_frame, text="Enable Voice Feedback", 
                       variable=self.voice_feedback_var).pack(anchor=tk.W)
        
        # Speech rate
        ttk.Label(voice_frame, text="Speech Rate:").pack(anchor=tk.W, pady=(10, 0))
        self.speech_rate_var = tk.IntVar(value=150)
        rate_scale = ttk.Scale(voice_frame, from_=50, to=300, variable=self.speech_rate_var, 
                              orient=tk.HORIZONTAL)
        rate_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Command settings
        cmd_frame = ttk.LabelFrame(settings_frame, text="Command Settings", padding="10")
        cmd_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Add custom command
        ttk.Label(cmd_frame, text="Add Custom Command:").pack(anchor=tk.W)
        cmd_input_frame = ttk.Frame(cmd_frame)
        cmd_input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(cmd_input_frame, text="Name:").pack(side=tk.LEFT)
        self.custom_cmd_name = ttk.Entry(cmd_input_frame, width=20)
        self.custom_cmd_name.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(cmd_input_frame, text="Program:").pack(side=tk.LEFT)
        self.custom_cmd_program = ttk.Entry(cmd_input_frame, width=30)
        self.custom_cmd_program.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(cmd_input_frame, text="Add", 
                  command=self.add_custom_program).pack(side=tk.LEFT)
        
        # Save settings button
        ttk.Button(settings_frame, text="Save Settings", 
                  command=self.save_settings).pack(pady=20)
        
    def setup_history_tab(self):
        """Setup the history tab"""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="History")
        
        # History controls
        control_frame = ttk.Frame(history_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="Refresh History", 
                  command=self.refresh_history).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="Clear History", 
                  command=self.clear_history).pack(side=tk.LEFT)
        
        # History list
        history_list_frame = ttk.LabelFrame(history_frame, text="Command History", padding="10")
        history_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create treeview for history
        columns = ('Time', 'Command', 'Result')
        self.history_tree = ttk.Treeview(history_list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=150)
        
        history_scrollbar = ttk.Scrollbar(history_list_frame, orient=tk.VERTICAL, 
                                         command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _on_voice_command(self, text: str):
        """Handle voice command from speech engine"""
        self.log_message(f"Voice command: {text}")
        
        # Process command
        result = self.command_processor.process_command(text)
        
        # Log result
        if result["success"]:
            self.log_message(f"Result: {result['result']}")
            self.voice_feedback.speak(f"Executed: {result['result']}")
        else:
            self.log_message(f"Error: {result['error']}")
            self.voice_feedback.speak(f"Error: {result['error']}")
        
        # Update history
        self.refresh_history()
    
    def toggle_listening(self):
        """Toggle voice listening"""
        if self.speech_engine.is_listening:
            self.speech_engine.stop_listening()
            self.listen_button.config(text="Start Listening")
            self.log_message("Stopped listening")
        else:
            if self.speech_engine.start_listening():
                self.listen_button.config(text="Stop Listening")
                self.log_message("Started listening")
            else:
                messagebox.showerror("Error", "Failed to start listening. Check microphone permissions.")
    
    def toggle_voice_feedback(self):
        """Toggle voice feedback"""
        if self.voice_feedback.voice_enabled:
            self.voice_feedback.disable_voice()
            self.feedback_button.config(text="Enable Voice Feedback")
            self.log_message("Voice feedback disabled")
        else:
            self.voice_feedback.enable_voice()
            self.feedback_button.config(text="Disable Voice Feedback")
            self.log_message("Voice feedback enabled")
    
    def execute_manual_command(self, event=None):
        """Execute command from manual entry"""
        command = self.cmd_entry.get().strip()
        if command:
            self._on_voice_command(command)
            self.cmd_entry.delete(0, tk.END)
    
    def update_status(self):
        """Update status display"""
        self.status_text.delete(1.0, tk.END)
        
        # Speech engine status
        speech_status = self.speech_engine.get_available_backends()
        self.status_text.insert(tk.END, "Speech Recognition:\n")
        self.status_text.insert(tk.END, f"  Google: {'✓' if speech_status['google'] else '✗'}\n")
        self.status_text.insert(tk.END, f"  Whisper: {'✓' if speech_status['whisper'] else '✗'}\n")
        self.status_text.insert(tk.END, f"  Working: {'✓' if speech_status['working'] else '✗'}\n\n")
        
        # Voice feedback status
        feedback_status = self.voice_feedback.get_status()
        self.status_text.insert(tk.END, "Voice Feedback:\n")
        self.status_text.insert(tk.END, f"  Enabled: {'✓' if feedback_status['voice_enabled'] else '✗'}\n")
        self.status_text.insert(tk.END, f"  PyTTSx3: {'✓' if feedback_status['pyttsx3_available'] else '✗'}\n")
        self.status_text.insert(tk.END, f"  gTTS: {'✓' if feedback_status['gtts_available'] else '✗'}\n")
        self.status_text.insert(tk.END, f"  Rate: {feedback_status['voice_rate']} WPM\n\n")
        
        # Listening status
        self.status_text.insert(tk.END, f"Listening: {'✓' if self.speech_engine.is_listening else '✗'}\n")
        self.status_text.insert(tk.END, f"Speaking: {'✓' if feedback_status['is_speaking'] else '✗'}\n")
    
    def log_message(self, message: str):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        print(log_entry.strip())
    
    def refresh_history(self):
        """Refresh command history display"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Get history
        history = self.command_processor.get_history(50)  # Last 50 commands
        
        # Add to treeview
        for entry in reversed(history):  # Show newest first
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M:%S')
            self.history_tree.insert('', 'end', values=(timestamp, entry['command'], ''))
    
    def clear_history(self):
        """Clear command history"""
        self.command_processor.clear_history()
        self.refresh_history()
        self.log_message("Command history cleared")
    
    def add_custom_program(self):
        """Add custom program mapping"""
        name = self.custom_cmd_name.get().strip()
        program = self.custom_cmd_program.get().strip()
        
        if name and program:
            self.command_processor.add_program(name, program)
            self.log_message(f"Added custom program: {name} -> {program}")
            self.custom_cmd_name.delete(0, tk.END)
            self.custom_cmd_program.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter both name and program path")
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                
                # Load wake words
                if 'wake_words' in config:
                    self.speech_engine.wake_words = config['wake_words']
                    self.wake_words_text.delete(1.0, tk.END)
                    self.wake_words_text.insert(1.0, '\n'.join(config['wake_words']))
                
                # Load voice feedback settings
                if 'voice_feedback' in config:
                    self.voice_feedback.voice_enabled = config['voice_feedback'].get('enabled', True)
                    self.voice_feedback_var.set(self.voice_feedback.voice_enabled)
                    
                    rate = config['voice_feedback'].get('rate', 150)
                    self.voice_feedback.set_voice_rate(rate)
                    self.speech_rate_var.set(rate)
                
                self.log_message("Configuration loaded")
        except Exception as e:
            self.log_message(f"Failed to load configuration: {e}")
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            config = {
                'wake_words': self.wake_words_text.get(1.0, tk.END).strip().split('\n'),
                'voice_feedback': {
                    'enabled': self.voice_feedback_var.get(),
                    'rate': self.speech_rate_var.get()
                }
            }
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            # Apply settings
            self.speech_engine.wake_words = config['wake_words']
            self.voice_feedback.voice_enabled = config['voice_feedback']['enabled']
            self.voice_feedback.set_voice_rate(config['voice_feedback']['rate'])
            
            self.log_message("Settings saved")
            messagebox.showinfo("Success", "Settings saved successfully!")
            
        except Exception as e:
            self.log_message(f"Failed to save settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        self.is_running = False
        self.speech_engine.cleanup()
        self.voice_feedback.cleanup()
        self.root.destroy()
    
    def run(self):
        """Run the enhanced application"""
        self.log_message("Xizo Enhanced Voice Assistant started")
        self.log_message("Voice control module initialized")
        
        # Initial status update
        self.update_status()
        
        # Start status update thread
        def status_updater():
            while self.is_running:
                try:
                    self.root.after(0, self.update_status)
                    threading.Event().wait(2)  # Update every 2 seconds
                except:
                    break
        
        status_thread = threading.Thread(target=status_updater, daemon=True)
        status_thread.start()
        
        self.root.mainloop()

if __name__ == "__main__":
    app = XizoEnhanced()
    app.run() 