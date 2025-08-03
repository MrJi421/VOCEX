import os
import subprocess
import sys

def build_executable():
    """Build the Xizo executable using PyInstaller"""
    print("Building Xizo Voice Assistant...")
    
    # PyInstaller command for robust version
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable
        "--windowed",  # No console window
        "--name=Xizo",  # Executable name
        "--add-data=README.md;.",  # Include README
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=pyautogui",
        "--hidden-import=psutil",
        "xizo_robust.py"
    ]
    
    try:
        # Remove existing build files
        if os.path.exists("dist"):
            import shutil
            shutil.rmtree("dist")
        if os.path.exists("build"):
            import shutil
            shutil.rmtree("build")
        if os.path.exists("Xizo.spec"):
            os.remove("Xizo.spec")
        
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            print(f"Executable created: dist/Xizo.exe")
            print("\nTo run Xizo:")
            print("1. Navigate to the dist folder")
            print("2. Double-click Xizo.exe")
            print("3. Use manual command entry or voice commands if available")
        else:
            print("❌ Build failed!")
            print("Error output:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Build error: {e}")

if __name__ == "__main__":
    build_executable() 