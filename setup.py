import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing Xizo dependencies...")
    
    try:
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False
    
    return True

def check_pyaudio():
    """Check if PyAudio is properly installed"""
    try:
        import pyaudio
        print("PyAudio is installed")
        return True
    except ImportError:
        print("PyAudio not found. This is required for microphone access.")
        print("Try installing it manually: pip install pyaudio")
        return False

def main():
    """Main setup function"""
    print("🧠 Xizo Voice Assistant Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Check PyAudio
    if not check_pyaudio():
        print("\nPyAudio installation may require additional steps on Windows.")
        print("If you encounter issues, try:")
        print("1. pip install pipwin")
        print("2. pipwin install pyaudio")
    
    print("\nSetup complete!")
    print("\nTo run Xizo:")
    print("1. python xizo.py")
    print("\nTo build executable:")
    print("1. python build.py")
    print("2. Run dist/Xizo.exe")

if __name__ == "__main__":
    main() 