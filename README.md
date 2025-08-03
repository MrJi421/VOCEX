# 🧠 Xizo – Your Voice. Your Command.

Xizo is a voice-activated virtual assistant that turns natural speech into system-level actions. Designed for hands-free control and intelligent automation, Xizo listens, understands, and executes — allowing you to interact with your device through simple, intuitive voice commands. Whether it's opening applications, running scripts, searching the web, or controlling custom workflows, Xizo transforms your voice into powerful, real-time actions.

## 🎯 Vision
To build an open, customizable, and intelligent voice interface that bridges the gap between human language and machine execution — making computing truly conversational.

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Python 3.8 or higher
- Microphone access
- Internet connection (for speech recognition)

### Installation

1. **Clone or download this repository**
2. **Run the setup script:**
   ```bash
   python setup.py
   ```

3. **Run Xizo:**
   ```bash
   python xizo.py
   ```

4. **Build executable (optional):**
   ```bash
   python build.py
   ```
   The executable will be created in the `dist/` folder.

## 🎤 Voice Commands

### Basic Commands
- **"Xizo open notepad"** - Opens Notepad
- **"Xizo open chrome"** - Opens Google Chrome
- **"Xizo write hello world"** - Types "hello world" in the active application
- **"Xizo search weather today"** - Searches Google for "weather today"
- **"Xizo close notepad"** - Closes Notepad

### Supported Programs
- Notepad, Word, Excel
- Chrome, Firefox, Edge
- Calculator, Paint
- File Explorer, Control Panel
- Task Manager

### Command Patterns
- **Open/Launch/Start** - Launch applications
- **Write/Type** - Type text in active application
- **Search/Google/Find** - Web search
- **Close/Exit/Quit** - Close applications

## 🛠️ Features

### Voice Recognition
- Uses Google Speech Recognition API
- Wake word: "Xizo"
- Real-time command processing
- Ambient noise adjustment

### System Integration
- Launch Windows applications
- Control running processes
- Web search integration
- Text input automation

### User Interface
- Clean, modern GUI
- Real-time command log
- Status indicators
- Easy start/stop controls

## 🔧 Technical Details

### Dependencies
- `SpeechRecognition` - Voice recognition
- `PyAudio` - Audio input/output
- `PyAutoGUI` - GUI automation
- `psutil` - Process management
- `tkinter` - GUI framework

### Architecture
- Multi-threaded design
- Non-blocking UI
- Error handling and logging
- Modular command system

## 🚨 Troubleshooting

### PyAudio Issues
If you encounter PyAudio installation problems on Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

### Microphone Access
- Ensure microphone permissions are enabled
- Check Windows privacy settings
- Test microphone in Windows settings

### Speech Recognition
- Requires internet connection
- May have slight delay on first use
- Works best with clear speech

## 📝 Development

### Project Structure
```
Xizo/
├── xizo.py          # Main application
├── setup.py         # Installation script
├── build.py         # Build script
├── requirements.txt # Dependencies
└── README.md        # This file
```

### Adding New Commands
1. Add command keyword to `self.commands` dictionary
2. Create corresponding function
3. Update this README

## 📄 License
This project is open source and available under the MIT License.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
