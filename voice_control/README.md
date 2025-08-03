# Voice Control Module

The Voice Control module provides advanced speech recognition, command processing, and voice feedback capabilities for the Xizo Voice Assistant.

## 🎤 Components

### 1. SpeechEngine (`speech_engine.py`)
- **Multi-backend speech recognition** (Google Speech Recognition, Whisper)
- **Wake word detection** with customizable wake words
- **Ambient noise adjustment**
- **Fallback mechanisms** for reliability

### 2. CommandProcessor (`command_processor.py`)
- **Natural language command parsing**
- **Extensive program mapping** (100+ applications)
- **Command history tracking**
- **Custom command and alias support**
- **Advanced system operations**

### 3. VoiceFeedback (`voice_feedback.py`)
- **Text-to-speech feedback** with multiple engines
- **Priority-based speech queue**
- **Voice customization** (rate, volume, voice selection)
- **Real-time speech status**

## 🚀 Features

### Speech Recognition
- **Google Speech Recognition API** (online)
- **OpenAI Whisper** (offline, planned)
- **Multiple wake words** support
- **Automatic noise adjustment**

### Command Processing
- **Natural language understanding**
- **Program launching** (100+ applications)
- **System control** (volume, brightness, etc.)
- **File operations** (planned)
- **Web search integration**
- **Text input automation**

### Voice Feedback
- **PyTTSx3** (offline, Windows)
- **gTTS** (online, Google)
- **Priority-based queue**
- **Voice customization**

## 📋 Supported Commands

### Basic Commands
- `open [program]` - Launch applications
- `write [text]` - Type text in active application
- `search [query]` - Web search
- `close [program]` - Close applications

### Advanced Commands
- `screenshot` - Take screenshot
- `copy/paste` - Clipboard operations
- `volume [up/down/mute]` - Audio control
- `brightness [up/down]` - Screen brightness
- `time/date` - Get current time/date
- `weather [location]` - Weather information (planned)

### System Programs
- **Windows Built-in**: Notepad, Word, Excel, Chrome, Calculator, etc.
- **Development**: VSCode, Sublime, Unity, Blender
- **Communication**: Discord, Teams, Zoom, WhatsApp
- **Productivity**: Notion, Obsidian, Slack

## 🔧 Usage

### Basic Usage
```python
from voice_control import SpeechEngine, CommandProcessor, VoiceFeedback

# Initialize components
speech_engine = SpeechEngine(callback=handle_command)
command_processor = CommandProcessor()
voice_feedback = VoiceFeedback()

# Start listening
speech_engine.start_listening()
```

### Custom Commands
```python
# Add custom program
command_processor.add_program("myapp", "C:\\Path\\To\\MyApp.exe")

# Add custom command
def my_custom_command(args):
    return f"Custom command executed: {args}"

command_processor.add_command("custom", my_custom_command)
```

### Voice Feedback
```python
# Speak with feedback
voice_feedback.speak("Command executed successfully")

# Immediate speech (interrupts current)
voice_feedback.speak_immediate("Important message")

# Customize voice
voice_feedback.set_voice_rate(200)  # Words per minute
voice_feedback.set_voice_volume(0.8)  # Volume level
```

## ⚙️ Configuration

### Wake Words
```python
speech_engine.wake_words = ["xizo", "hey xizo", "listen xizo"]
speech_engine.add_wake_word("computer")
```

### Voice Settings
```python
voice_feedback.voice_enabled = True
voice_feedback.set_voice_rate(150)  # WPM
voice_feedback.set_voice_volume(0.7)  # 0.0 to 1.0
```

## 🔌 Dependencies

### Required
- `pyautogui` - GUI automation
- `psutil` - Process management
- `tkinter` - GUI framework

### Optional (for full functionality)
- `SpeechRecognition` + `pyaudio` - Speech recognition
- `pyttsx3` - Offline text-to-speech
- `gtts` + `pygame` - Online text-to-speech
- `openai-whisper` - Offline speech recognition

## 🛠️ Installation

### Basic Installation
```bash
pip install pyautogui psutil
```

### Full Installation (with voice features)
```bash
pip install pyautogui psutil SpeechRecognition pyaudio pyttsx3 gtts pygame
```

### Windows PyAudio Fix
```bash
pip install pipwin
pipwin install pyaudio
```

## 📁 File Structure
```
voice_control/
├── __init__.py           # Package initialization
├── speech_engine.py      # Speech recognition engine
├── command_processor.py  # Command processing system
├── voice_feedback.py     # Text-to-speech feedback
└── README.md            # This file
```

## 🔮 Future Enhancements

### Planned Features
- **Offline Whisper integration** for privacy
- **File operations** (copy, move, delete, search)
- **Email and messaging** integration
- **Calendar and reminder** system
- **Weather API** integration
- **System monitoring** and alerts
- **Custom workflow** automation
- **Voice training** for better accuracy

### Advanced Features
- **Context awareness** (remember previous commands)
- **Natural language processing** (NLP)
- **Machine learning** for command prediction
- **Multi-language** support
- **Voice biometrics** for user identification
- **Conversation mode** for extended interactions

## 🐛 Troubleshooting

### Speech Recognition Issues
1. **Check microphone permissions** in Windows settings
2. **Verify internet connection** for Google Speech Recognition
3. **Test microphone** in Windows sound settings
4. **Install PyAudio** using pipwin on Windows

### Voice Feedback Issues
1. **Install PyTTSx3** for offline speech
2. **Check audio output** settings
3. **Verify gTTS** installation for online speech
4. **Test with simple text** first

### Command Execution Issues
1. **Check program paths** in custom mappings
2. **Verify administrator permissions** for system commands
3. **Test commands manually** first
4. **Check antivirus** blocking

## 📄 License
This module is part of the Xizo Voice Assistant project and is available under the MIT License. 