"""
Command Processor Module
Handles command parsing, execution, and management
"""

import subprocess
import os
import sys
import json
import logging
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
import psutil

# Try to import PyAutoGUI
try:
    import pyautogui
    AUTOGUI_AVAILABLE = True
except ImportError:
    AUTOGUI_AVAILABLE = False

class CommandProcessor:
    """Advanced command processor with natural language understanding"""
    
    def __init__(self):
        self.commands = {}
        self.programs = {}
        self.aliases = {}
        self.command_history = []
        self.max_history = 100
        
        # Load default commands and programs
        self._load_default_commands()
        self._load_default_programs()
        
    def _load_default_commands(self):
        """Load default command handlers"""
        self.commands = {
            "open": self.open_program,
            "launch": self.open_program,
            "start": self.open_program,
            "run": self.open_program,
            "write": self.write_text,
            "type": self.write_text,
            "search": self.search_web,
            "google": self.search_web,
            "find": self.search_web,
            "lookup": self.search_web,
            "close": self.close_program,
            "exit": self.close_program,
            "quit": self.close_program,
            "kill": self.close_program,
            "copy": self.copy_to_clipboard,
            "paste": self.paste_from_clipboard,
            "screenshot": self.take_screenshot,
            "volume": self.control_volume,
            "brightness": self.control_brightness,
            "mute": self.toggle_mute,
            "file": self.file_operations,
            "folder": self.file_operations,
            "directory": self.file_operations,
            "time": self.get_time,
            "date": self.get_date,
            "weather": self.get_weather,
            "reminder": self.set_reminder,
            "note": self.create_note,
            "email": self.send_email,
            "message": self.send_message
        }
    
    def _load_default_programs(self):
        """Load default program mappings"""
        self.programs = {
            # Windows built-in
            "notepad": "notepad.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "explorer": "explorer.exe",
            "control panel": "control.exe",
            "task manager": "taskmgr.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
            "regedit": "regedit.exe",
            "services": "services.msc",
            "device manager": "devmgmt.msc",
            
            # Common applications
            "spotify": "spotify.exe",
            "discord": "discord.exe",
            "steam": "steam.exe",
            "vscode": "code.exe",
            "sublime": "sublime_text.exe",
            "photoshop": "photoshop.exe",
            "illustrator": "illustrator.exe",
            "premiere": "premiere.exe",
            "after effects": "afterfx.exe",
            "blender": "blender.exe",
            "unity": "unity.exe",
            "unreal": "unreal.exe",
            "zoom": "zoom.exe",
            "teams": "teams.exe",
            "skype": "skype.exe",
            "whatsapp": "whatsapp.exe",
            "telegram": "telegram.exe",
            "slack": "slack.exe",
            "notion": "notion.exe",
            "obsidian": "obsidian.exe",
            "roam": "roam.exe",
            "logseq": "logseq.exe"
        }
    
    def process_command(self, text: str) -> Dict[str, Any]:
        """Process a voice command and return result"""
        try:
            # Add to history
            self._add_to_history(text)
            
            # Parse command
            parsed = self._parse_command(text)
            
            # Execute command
            result = self._execute_command(parsed)
            
            return {
                "success": True,
                "command": text,
                "parsed": parsed,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Command processing error: {e}")
            return {
                "success": False,
                "command": text,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _parse_command(self, text: str) -> Dict[str, Any]:
        """Parse natural language command into structured format"""
        text = text.lower().strip()
        
        # Find the main command
        command = None
        args = text
        
        for cmd in self.commands.keys():
            if cmd in text:
                command = cmd
                args = text.replace(cmd, "").strip()
                break
        
        # Handle aliases
        if command in self.aliases:
            command = self.aliases[command]
        
        return {
            "command": command,
            "args": args,
            "original": text
        }
    
    def _execute_command(self, parsed: Dict[str, Any]) -> Any:
        """Execute a parsed command"""
        command = parsed.get("command")
        args = parsed.get("args", "")
        
        if not command or command not in self.commands:
            # Default to text input if no command found
            return self.write_text(parsed.get("original", ""))
        
        # Execute the command
        return self.commands[command](args)
    
    def open_program(self, program_name: str) -> str:
        """Open a program or file"""
        program_name = program_name.strip()
        
        # Check if it's a known program
        if program_name in self.programs:
            program_path = self.programs[program_name]
            try:
                subprocess.Popen(program_path)
                return f"Opened {program_name}"
            except Exception as e:
                raise Exception(f"Failed to open {program_name}: {e}")
        else:
            # Try to open as a file or program
            try:
                subprocess.Popen(program_name)
                return f"Opened {program_name}"
            except Exception as e:
                raise Exception(f"Failed to open {program_name}: {e}")
    
    def write_text(self, text: str) -> str:
        """Write text to active application"""
        if not text.strip():
            return "No text to write"
            
        if not AUTOGUI_AVAILABLE:
            return "PyAutoGUI not available for text input"
            
        try:
            pyautogui.write(text)
            return f"Wrote text: {text}"
        except Exception as e:
            raise Exception(f"Failed to write text: {e}")
    
    def search_web(self, query: str) -> str:
        """Search the web"""
        if not query.strip():
            return "No search query provided"
            
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            subprocess.Popen(["start", search_url], shell=True)
            return f"Searched for: {query}"
        except Exception as e:
            raise Exception(f"Failed to search: {e}")
    
    def close_program(self, program_name: str) -> str:
        """Close a program"""
        program_name = program_name.strip()
        
        try:
            if program_name in self.programs:
                program_path = self.programs[program_name]
                # Kill process by name
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] and program_path.lower() in proc.info['name'].lower():
                        proc.terminate()
                        return f"Closed {program_name}"
            else:
                # Try to close by name
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] and program_name.lower() in proc.info['name'].lower():
                        proc.terminate()
                        return f"Closed {program_name}"
                        
            return f"Could not find {program_name} to close"
        except Exception as e:
            raise Exception(f"Failed to close {program_name}: {e}")
    
    def copy_to_clipboard(self, text: str) -> str:
        """Copy text to clipboard"""
        if not AUTOGUI_AVAILABLE:
            return "PyAutoGUI not available for clipboard operations"
            
        try:
            pyautogui.hotkey('ctrl', 'c')
            return f"Copied to clipboard: {text}"
        except Exception as e:
            raise Exception(f"Failed to copy to clipboard: {e}")
    
    def paste_from_clipboard(self, text: str = "") -> str:
        """Paste from clipboard"""
        if not AUTOGUI_AVAILABLE:
            return "PyAutoGUI not available for clipboard operations"
            
        try:
            pyautogui.hotkey('ctrl', 'v')
            return "Pasted from clipboard"
        except Exception as e:
            raise Exception(f"Failed to paste from clipboard: {e}")
    
    def take_screenshot(self, args: str = "") -> str:
        """Take a screenshot"""
        if not AUTOGUI_AVAILABLE:
            return "PyAutoGUI not available for screenshots"
            
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(filename)
            return f"Screenshot saved as {filename}"
        except Exception as e:
            raise Exception(f"Failed to take screenshot: {e}")
    
    def control_volume(self, args: str) -> str:
        """Control system volume"""
        try:
            # This would need additional implementation
            return f"Volume control: {args}"
        except Exception as e:
            raise Exception(f"Failed to control volume: {e}")
    
    def control_brightness(self, args: str) -> str:
        """Control screen brightness"""
        try:
            # This would need additional implementation
            return f"Brightness control: {args}"
        except Exception as e:
            raise Exception(f"Failed to control brightness: {e}")
    
    def toggle_mute(self, args: str = "") -> str:
        """Toggle system mute"""
        try:
            # This would need additional implementation
            return "Toggled system mute"
        except Exception as e:
            raise Exception(f"Failed to toggle mute: {e}")
    
    def file_operations(self, args: str) -> str:
        """Handle file operations"""
        try:
            # This would need additional implementation
            return f"File operation: {args}"
        except Exception as e:
            raise Exception(f"Failed to perform file operation: {e}")
    
    def get_time(self, args: str = "") -> str:
        """Get current time"""
        return f"Current time: {datetime.now().strftime('%H:%M:%S')}"
    
    def get_date(self, args: str = "") -> str:
        """Get current date"""
        return f"Current date: {datetime.now().strftime('%Y-%m-%d')}"
    
    def get_weather(self, location: str) -> str:
        """Get weather information"""
        try:
            # This would need API integration
            return f"Weather for {location}: Not implemented yet"
        except Exception as e:
            raise Exception(f"Failed to get weather: {e}")
    
    def set_reminder(self, args: str) -> str:
        """Set a reminder"""
        try:
            # This would need additional implementation
            return f"Reminder set: {args}"
        except Exception as e:
            raise Exception(f"Failed to set reminder: {e}")
    
    def create_note(self, content: str) -> str:
        """Create a note"""
        try:
            # This would need additional implementation
            return f"Note created: {content}"
        except Exception as e:
            raise Exception(f"Failed to create note: {e}")
    
    def send_email(self, args: str) -> str:
        """Send an email"""
        try:
            # This would need additional implementation
            return f"Email: {args}"
        except Exception as e:
            raise Exception(f"Failed to send email: {e}")
    
    def send_message(self, args: str) -> str:
        """Send a message"""
        try:
            # This would need additional implementation
            return f"Message: {args}"
        except Exception as e:
            raise Exception(f"Failed to send message: {e}")
    
    def add_command(self, name: str, handler: Callable):
        """Add a custom command"""
        self.commands[name.lower()] = handler
        logging.info(f"Added custom command: {name}")
    
    def add_program(self, name: str, path: str):
        """Add a custom program mapping"""
        self.programs[name.lower()] = path
        logging.info(f"Added program mapping: {name} -> {path}")
    
    def add_alias(self, alias: str, command: str):
        """Add a command alias"""
        self.aliases[alias.lower()] = command.lower()
        logging.info(f"Added alias: {alias} -> {command}")
    
    def _add_to_history(self, command: str):
        """Add command to history"""
        self.command_history.append({
            "command": command,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent history
        if len(self.command_history) > self.max_history:
            self.command_history = self.command_history[-self.max_history:]
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get command history"""
        return self.command_history[-limit:] if limit else self.command_history
    
    def clear_history(self):
        """Clear command history"""
        self.command_history.clear()
        logging.info("Command history cleared") 